from odoo import fields, models, api, _


class Delivery(models.Model):
    _name = 'restaurant.delivery'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char('Nama Pemesan')
    driver_id = fields.Many2one(comodel_name='restaurant.pekerja',
                                string='Driver_id',
                                domain=[('role', '=', 'driver')],
                                required=False,
                                tracking=True)

    state = fields.Selection(string='Status',
                             selection=[('pesanan', 'Pesanan'),
                                        ('diantar', 'Diantar'),
                                        ('selesai', 'Selesai'),
                                        ('batal', 'Batal'), ],
                             required=True, default='pesanan',
                             tracking=True)

    reference = fields.Char(string='Order ID', required=True, copy=False, readonly=True,
                            default=lambda self: _('Order ID :'),
                            tracking=True)

    alamat = fields.Text(
        string="Alamat",
        required=False, tracking=True)

    tipe_pembayaran = fields.Selection(string='Tipe Pembayaran',
                                       selection=[('tunai', 'Tunai'),
                                                  ('emoney', 'E-Money'),
                                                  ('debit', 'Kartu Debit'),
                                                  ('kredit', 'Kartu Kredit')],
                                       required=False,
                                       tracking=True)
    jam_berangkat = fields.Datetime(
        string='Jam Berangkat',
        required=False,
        tracking=True)

    # membuat sequence nomor delivery
    @api.model
    def create(self, vals):
        if vals.get('reference', _('Order ID :')) == _('Order ID :'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('restaurant.delivery') or _('Order ID :')
        res = super(Delivery, self).create(vals)
        return res

    def action_diantar(self):
        for rec in self:
            rec.state = 'diantar'

    def action_selesai(self):
        for rec in self:
            rec.state = 'selesai'


class deliverydetail(models.Model):
    _name = 'restauran.deliverydetail'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'deliverydetail'

    name = fields.Char()

    delivery_id = fields.Many2one(comodel_name='restaurant.delivery',
                                  string='Order ID',
                                  required=False)

    menu_id = fields.Many2one(comodel_name='restaurant.menu_makanan',
                              string='Daftar Menu',
                              required=False)

    harga_menu = fields.Integer(string='Harga',
                                required=False)

    jumlah = fields.Integer(string='Total',
                            compute="_compute_jumlah",
                            required=False)

    qty = fields.Integer(string='Qty',
                         required=False,
                         tracking=True)

    @api.onchange('menu_id')
    def _onchange_menu_id(self):
        if (self.menu_id.harga_menu):
            self.harga_menu = self.menu_id.harga_menu

    @api.depends('harga_menu', 'qty')
    def _compute_jumlah(self):
        for rec in self:
            rec.jumlah = rec.qty * rec.harga_menu
