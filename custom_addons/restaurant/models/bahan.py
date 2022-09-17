from odoo import fields, models, api


class bahan(models.Model):
    _name = 'restaurant.bahan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char('Nama Bahan', tracking=True)
    tipe = fields.Selection(
        string='Tipe',
        selection=[('daging', 'Daging'),
                   ('seafood', 'Seafood'),
                   ('bumbu', 'Bumbu'),
                   ('sayuran','Sayuran'),
                   ('lain', 'Lain-Lain'),
                   ],
        required=False, tracking=True, default='daging')
    qty = fields.Integer(string='Qty',
                         required=False, tracking=True)
    deskripsi = fields.Text(
        string="Deskripsi",
        required=False, tracking=True)
    tgl_datang = fields.Date(
        string='Tgl Datang',
        required=False, tracking=True)
    kadaluarsa = fields.Date(
        string='Kadaluarsa',
        required=False, tracking=True)

    supplier_id = fields.Many2one(
        comodel_name='restaurant.supplier',
        string='Supplier_id',
        domain=[('keterangan', '=', 'supplier_bahan_makanan')],
        required=False, tracking=True)

    harga = fields.Integer(
        string='Harga',
        required=False)
