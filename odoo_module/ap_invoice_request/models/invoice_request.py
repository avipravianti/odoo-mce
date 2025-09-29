from odoo import models, fields, api, _
from odoo.exceptions import UserError
import uuid


class InvoiceRequest(models.Model):
    _name = 'invoice.request'
    _description = 'Invoice Request from External Partners'
    _rec_name = 'partner_id'
    _order = 'create_date desc'

    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    sale_id = fields.Many2one('sale.order', string='Sales Order', required=False,
                              domain="[('partner_id', '=', partner_id), ('state', '=', 'sale'), ('invoice_status', '=', 'to invoice')]")
    invoice_id = fields.Many2one('account.move', string='Generated Invoice')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ], string='Status', default='pending', required=True)
    external_token = fields.Char('External Access Token', default=lambda self: str(
        uuid.uuid4()), readonly=True, copy=False)
    request_date = fields.Datetime('Request Date', default=fields.Datetime.now)
    processing_date = fields.Datetime('Processing Date')

    @api.model
    def create_from_external_request(self, partner_id, sale_id):
        """
        Create invoice request from external form
        """
        request = self.create({
            'partner_id': partner_id,
            'sale_id': sale_id,
            'state': 'pending',
        })

        return request.id

    def approve_request(self):
        """
        Approve the invoice request and create the invoice
        """
        for request in self:
            if request.state != 'pending' or not request.sale_id:
                continue

            # Create and post invoice
            invoice = request.sale_id._create_invoices()
            if invoice:
                invoice.action_post()
                request.write({
                    'invoice_id': invoice.id,
                    'state': 'approved',
                    'processing_date': fields.Datetime.now(),
                })

    @api.model
    def get_partner_token(self, partner_id):
        """
        Get or create a token for a partner
        """
        request = self.search([('partner_id', '=', partner_id)], limit=1)
        if not request:
            request = self.create({
                'partner_id': partner_id,
                'state': 'pending',
            })
        return request.external_token
