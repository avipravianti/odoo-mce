from odoo import api, fields, models


class DevSekolah(models.Model):
    _name = 'dev.sekolah'
    _description = 'Sekolah'

    name = fields.Char(string='Nama Sekolah', required=True)
    alamat = fields.Char(string='Alamat')

    kelas_ids = fields.One2many(
        comodel_name='dev.sekolah.kelas',
        inverse_name='sekolah_id',
        string='Daftar Kelas',
    )

    jumlah_kelas = fields.Integer(
        string='Jumlah Kelas',
        compute='_compute_jumlah_kelas',
        store=True,
        readonly=True,
    )

    @api.depends('kelas_ids')
    def _compute_jumlah_kelas(self):
        for sekolah in self:
            sekolah.jumlah_kelas = len(sekolah.kelas_ids)
