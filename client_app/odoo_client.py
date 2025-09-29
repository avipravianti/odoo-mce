# client_app/odoo_client.py
import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class OdooClient:
    def __init__(self):
        # Configuration from environment variables
        self.url = os.getenv("ODOO_URL", "http://localhost:8069")
        self.db = os.getenv("ODOO_DB", "odoo-mce")
        self.username = os.getenv("ODOO_USERNAME", "admin")
        self.password = os.getenv("ODOO_PASSWORD", "admin123")

        # XML-RPC endpoints
        self.common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")

        # Authenticate and get user ID
        self.uid = self._authenticate()

    def _authenticate(self):
        """Authenticate with Odoo and return user ID"""
        try:
            uid = self.common.authenticate(
                self.db, self.username, self.password, {})
            if not uid:
                raise Exception("Authentication failed")
            return uid
        except Exception as e:
            raise Exception(f"Failed to connect to Odoo: {str(e)}")

    def _execute(self, model, method, *args, **kwargs):
        """Execute a method on an Odoo model"""
        try:
            return self.models.execute_kw(
                self.db, self.uid, self.password, model, method, args, kwargs
            )
        except xmlrpc.client.Fault as error:
            raise Exception(f"Odoo error: {error.faultString}")

    # Sale Order operations
    def create_sale_order(self, values):
        """Create a new sale order"""
        return self._execute('sale.order', 'create', [values])

    def update_sale_order(self, order_id, values):
        """Update an existing sale order"""
        return self._execute('sale.order', 'write', [[order_id], values])

    def get_sale_orders(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """Get a list of sale orders"""
        domain = domain or []
        fields = fields or ['name', 'partner_id',
                            'date_order', 'amount_total', 'state']
        kwargs = {
            'offset': offset,
            'limit': limit,
            'order': order,
        }
        return self._execute('sale.order', 'search_read', domain, fields=fields, **{k: v for k, v in kwargs.items() if v is not None})

    def get_sale_order(self, order_id, fields=None):
        """Get a specific sale order"""
        fields = fields or ['name', 'partner_id',
                            'date_order', 'amount_total', 'state', 'order_line']
        # Fix: pass fields as a keyword argument, not as a dictionary
        return self._execute('sale.order', 'read', [order_id], fields=fields)

    def confirm_sale_order(self, order_id):
        """Confirm a sale order"""
        return self._execute('sale.order', 'action_confirm', [order_id])

    def cancel_sale_order(self, order_id):
        """Cancel a sale order"""
        return self._execute('sale.order', 'action_cancel', [order_id])

    def reset_sale_order_to_draft(self, order_id):
        """Reset a sale order to draft"""
        return self._execute('sale.order', 'action_draft', [order_id])
