from odoo import fields, models, api


class tambah_inventory(models.TransientModel):
    _name = 'restaurant.tambah_inventory'
    _description = 'Description'

    inventory_id = fields.Many2one(
        comodel_name='restaurant.inventory',
        string='Nama Barang',
        required=True)

    qty = fields.Integer(
        string='Qty',
        required=False)

    def button_tambah_bahan(self):
        for rec in self:
            self.env['restaurant.inventory'] \
                .search([('id', '=', rec.inventory_id.id)]) \
                .write({'qty': rec.inventory_id.qty + rec.qty})