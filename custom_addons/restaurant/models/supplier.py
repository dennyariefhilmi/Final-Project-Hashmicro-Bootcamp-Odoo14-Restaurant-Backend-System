from odoo import fields, models, api


class supplier(models.Model):
    _name = 'restaurant.supplier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char('Nama Supplier', tracking=True)
    keterangan = fields.Selection(string='Keterangan',
                                  selection=[('supplier_inventory', 'Supplier Inventory'),
                                             ('supplier_bahan_makanan', 'Supplier Bahan Makanan'),],
                                  required=False, tracking=True,
                                  default='supplier_inventory')

    alamat = fields.Char(string='Alamat', required=False, tracking=True)
    negara = fields.Many2one('res.country', string="Negara", tracking=True)
    provinsi = fields.Many2one('res.country.state', string="Provinsi", store=True, tracking=True)
    # kota = fields.Many2one('res.city', string="Kota", store=True)
    kota = fields.Char(
        string='Kota',
        required=False, tracking=True)
    deskripsi = fields.Text(
        string="Deskripsi",
        required=False, tracking=True)
    bahan_id = fields.One2many(
        comodel_name='restaurant.bahan',
        inverse_name='supplier_id',
        string='Bahan ID',
        required=False, tracking=True)

    inventory_id = fields.One2many(
        comodel_name='restaurant.inventory',
        inverse_name='supplier_id',
        string='Inventory ID',
        required=False)

    @api.onchange('negara', 'provinsi')
    def set_values_to(self):
        if self.negara:
            ids = self.env['res.country.state'].search([('country_id', '=', self.negara.id)])
            return {
                'domain': {'provinsi': [('id', 'in', ids.ids)], }
            }
