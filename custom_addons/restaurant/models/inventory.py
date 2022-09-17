from odoo import fields, models, api


class inventory(models.Model):
    _name = 'restaurant.inventory'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Inventory'

    name = fields.Char('Nama Barang',
                       required=False, tracking=True)

    merk = fields.Char(string='Merk',
                       required=False, tracking= True)

    tipe = fields.Selection(
        string='Tipe',
        selection=[('alat_masak', 'Alat Masak'),
                   ('alat_makan', 'Alat Makan'),
                   ('alat_elektronik', 'Alat Elektronik')],
        required=False, tracking = True, default='alat_masak')

    qty = fields.Integer(
        string='Qty',
        required=False, tracking = True)

    deskripsi = fields.Text(
        string='Deskripsi',
        required=False, tracking = True)

    supplier_id = fields.Many2one(
        comodel_name='restaurant.supplier',
        string='Supplier_id',
        domain=[('keterangan', '=', 'supplier_inventory')],
        required=False)
    harga = fields.Integer(
        string='Harga', 
        required=False)


