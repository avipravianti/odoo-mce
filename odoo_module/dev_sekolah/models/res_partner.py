from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_guru = fields.Boolean(string='Guru')

    bidang_studi = fields.Selection(
        selection=[
            ('matematika', 'Matematika'),
            ('bahasa', 'Bahasa'),
            ('ipa', 'IPA'),
            ('ips', 'IPS'),
            ('olahraga', 'Olahraga'),
        ],
        string='Bidang Studi',
    )
