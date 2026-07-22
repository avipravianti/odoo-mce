#!/bin/bash
# Render entrypoint for Odoo 17.
# - Binds Odoo to Render's $PORT (Render health-checks this port).
# - Reads DB connection from ODOO_DB_* env vars (NOT PORT: Render owns PORT).
# - First boot: initializes DB with base + your module. Later boots: just run.
set -e

: "${PORT:=8069}"
: "${ODOO_DB_NAME:=odoo}"
: "${ODOO_ADMIN_PASSWD:=changeme}"
: "${MODULES_TO_INSTALL:=dev_sekolah}"

cat > /etc/odoo/odoo.conf <<EOF
[options]
admin_passwd = ${ODOO_ADMIN_PASSWD}
db_host = ${ODOO_DB_HOST}
db_port = ${ODOO_DB_PORT:-5432}
db_user = ${ODOO_DB_USER}
db_password = ${ODOO_DB_PASSWORD}
db_name = ${ODOO_DB_NAME}
dbfilter = ^${ODOO_DB_NAME}\$
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
http_port = ${PORT}
proxy_mode = True
list_db = False
workers = ${ODOO_WORKERS:-0}
EOF

# One-time init: install modules if the DB has no Odoo schema yet.
ALREADY_INIT=$(PGPASSWORD="${ODOO_DB_PASSWORD}" psql -h "${ODOO_DB_HOST}" -p "${ODOO_DB_PORT:-5432}" \
  -U "${ODOO_DB_USER}" -d "${ODOO_DB_NAME}" -tAc \
  "SELECT to_regclass('public.ir_module_module');" 2>/dev/null || echo "")

if [ -z "${ALREADY_INIT}" ]; then
  echo "[entrypoint] Fresh database — initializing ${MODULES_TO_INSTALL}"
  odoo -c /etc/odoo/odoo.conf -d "${ODOO_DB_NAME}" -i "base,${MODULES_TO_INSTALL}" --stop-after-init
fi

echo "[entrypoint] Starting Odoo on port ${PORT}"
exec odoo -c /etc/odoo/odoo.conf
