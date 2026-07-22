from odoo import fields, models


class DevSekolahKelas(models.Model):
    _name = 'dev.sekolah.kelas'
    _description = 'Kelas'

    name = fields.Char(string='Nama Kelas', required=True)

    sekolah_id = fields.Many2one(
        comodel_name='dev.sekolah',
        string='Sekolah',
        ondelete='cascade',
    )

    wali_kelas_id = fields.Many2one(
        comodel_name='res.partner',
        string='Wali Kelas',
        domain=[('is_guru', '=', True)],
    )

    # Soal 4.3: computed jumlah_kelas dari Sekolah terhubung, diekspos ke widget OWL
    sekolah_jumlah_kelas = fields.Integer(
        string='Total Kelas di Sekolah',
        related='sekolah_id.jumlah_kelas',
        readonly=True,
    )
