from odoo import fields, models, api

class menu_makanan(models.Model):
    _name = 'restaurant.menu_makanan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char(string='Nama',
                       tracking=True)

    tipe = fields.Selection(string='Tipe',
                            selection=[('pizza', 'Pizza'),
                                       ('minuman', 'Minuman'),
                                       ('dessert', 'Dessert'),
                                       ('pasta', 'Pasta'),
                                       ('appetizer', 'Appetizer'), ],
                            required=False,
                            tracking=True,
                            default='pizza')

    harga_menu = fields.Integer(string='Harga',
                                required=False,
                                tracking=True)
    deskripsi = fields.Text(string='Deskripsi',
                            required=False,
                            tracking=True)
    img_makanan = fields.Binary(string="Gambar Makanan",
                                tracking=True)