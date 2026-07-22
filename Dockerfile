FROM odoo:17.0

USER root

# Custom addons from both source dirs land in /mnt/extra-addons (COPY merges).
COPY ./odoo_module /mnt/extra-addons
COPY ./addons /mnt/extra-addons

# Extra Python deps for custom modules (uncomment if needed):
# COPY requirements-extra.txt /tmp/requirements-extra.txt
# RUN pip3 install --no-cache-dir -r /tmp/requirements-extra.txt

COPY render/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER odoo
ENTRYPOINT ["/entrypoint.sh"]
