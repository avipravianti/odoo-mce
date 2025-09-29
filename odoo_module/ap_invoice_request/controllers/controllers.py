from odoo import http, _
from odoo.http import request
import json


class ExternalInvoiceController(http.Controller):
    @http.route(['/sale-orders/to-invoice'], type='http', auth='public', website=True)
    def list_to_invoice_orders(self, **kwargs):
        """
        Display a list of all sales orders with invoice_status = 'to invoice'
        """
        # Get all sales orders with 'to invoice' status
        orders = request.env['sale.order'].sudo().search([
            ('state', '=', 'sale'),
            ('invoice_status', '=', 'to invoice')
        ])

        orders_data = []
        for order in orders:
            # Format the date as a string
            date_order = order.date_order.strftime(
                '%Y-%m-%d %H:%M:%S') if order.date_order else False

            orders_data.append({
                'id': order.id,
                'name': order.name,
                'partner_id': order.partner_id.id,
                'partner_name': order.partner_id.name,
                'date_order': date_order,
                'amount_total': order.amount_total,
                'currency': order.currency_id.symbol,
                'order_line_count': len(order.order_line)
            })

        values = {
            'orders': orders_data
        }

        return request.render('ap_invoice_request.list_to_invoice_orders', values)

    @http.route(['/external/sale-invoice', '/external/sale-invoice/<string:token>'], type='http', auth='public', website=True)
    def external_invoice_form(self, token=None, sale_id=None, partner_id=None, **kwargs):
        """
        Renders the external invoice request form
        """
        partner = None
        invoice_request = None

        # If token is provided, try to get the specific partner
        if token:
            invoice_request = request.env['invoice.request'].sudo().search(
                [('external_token', '=', token)], limit=1)
            if invoice_request:
                partner = invoice_request.partner_id

        # If partner_id is provided in URL, use that instead
        elif partner_id:
            partner = request.env['res.partner'].sudo().browse(int(partner_id))

        # Get eligible sales orders
        domain = [('state', '=', 'sale'),
                  ('invoice_status', '=', 'to invoice')]
        if partner:
            domain.append(('partner_id', '=', partner.id))

        # If sale_id is provided, preselect that sale order
        preselected_sale_id = int(sale_id) if sale_id else False

        sales = request.env['sale.order'].sudo().search(domain)

        sales_data = []
        for sale in sales:
            # Format the date as a string to ensure JSON compatibility
            date_order = sale.date_order.strftime(
                '%Y-%m-%d %H:%M:%S') if sale.date_order else False

            sales_data.append({
                'id': sale.id,
                'name': sale.name,
                'date_order': date_order,
                'amount_total': sale.amount_total,
                'partner': {
                    'id': sale.partner_id.id,
                    'name': sale.partner_id.name
                }
            })

        # Prepare data for the OWL component
        data = {
            'token': token or '',
            'partner': {
                'id': partner.id if partner else False,
                'name': partner.name if partner else '',
                'email': partner.email if partner else '',
                'phone': partner.phone if partner else '',
            },
            'sales': sales_data,
            'has_partner': bool(partner),
            'preselected_sale_id': preselected_sale_id,
            'invoice': {
                'id': invoice_request.invoice_id.id if invoice_request and invoice_request.invoice_id else False,
                'state': invoice_request.state if invoice_request else '',
            }
        }

        # Use safe_json to avoid escaping issues
        values = {
            'data': data,  # Python dictionary for use in template
            'data_json': json.dumps(data),  # JSON string for JavaScript
            'partner_ids': {}
        }

        return request.render('ap_invoice_request.external_invoice_request_page', values)

    @http.route(['/external/sale-invoice/submit'], type='json', auth='public', website=True)
    def submit_invoice_request(self, token, partner_id, sale_id, **kwargs):
        """
        Handles the submission of the invoice request
        """
        partner = request.env['res.partner'].sudo().browse(int(partner_id))
        if not partner:
            return {'error': _('Invalid partner')}

        # Get or create a token for this partner if needed
        if not token:
            token = request.env['invoice.request'].sudo(
            ).get_partner_token(partner.id)

        # Check if the sale order is valid
        sale = request.env['sale.order'].sudo().browse(int(sale_id))
        if not sale or sale.state != 'sale' or sale.invoice_status != 'to invoice':
            return {'error': _('Invalid sales order')}

        # Create the invoice request
        try:
            request_id = request.env['invoice.request'].sudo(
            ).create_from_external_request(partner.id, sale.id)
            invoice_request = request.env['invoice.request'].sudo().browse(
                request_id)

            return {
                'success': True,
                'message': _('Invoice request submitted successfully'),
                'invoice_id': invoice_request.invoice_id.id if invoice_request.invoice_id else False,
                'state': invoice_request.state,
                'token': token,
            }
        except Exception as e:
            return {'error': str(e)}
