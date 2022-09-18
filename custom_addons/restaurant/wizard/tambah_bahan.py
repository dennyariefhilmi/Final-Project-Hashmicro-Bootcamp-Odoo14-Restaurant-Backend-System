from odoo import fields, models, api


class tambah_bahan(models.TransientModel):
    _name = 'restaurant.tambah_bahan'
    _description = 'Description'

    bahan_id = fields.Many2one(
        comodel_name='restaurant.bahan',
        string='Nama Bahan Makanan',
        required=True)

    qty = fields.Integer(
        string='Qty',
        required=False)

    def button_tambah_bahan(self):
        for rec in self:
            self.env['restaurant.bahan'] \
                .search([('id', '=', rec.bahan_id.id)]) \
                .write({'qty': rec.bahan_id.qty + rec.qty})
