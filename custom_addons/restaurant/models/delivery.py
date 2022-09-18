from odoo import fields, models, api, _


class delivery(models.Model):
    _name = 'restaurant.delivery'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char('Nama Pemesan')
    driver_id = fields.Many2one(comodel_name='restaurant.karyawan',
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

    deliverydetail_id = fields.One2many(comodel_name='restaurant.deliverydetail',
                                        inverse_name='delivery_id',
                                        string='Delivery Detail ID',
                                        required=False)

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

    total = fields.Integer(
        string='Subtotal',
        required=False,
        compute='_compute_total')

    pajak = fields.Integer(string='PPN 10%',
                           compute='_compute_pajak',
                           required=False)

    subtotal = fields.Integer(string='Grand Total',
                              compute='_compute_subtotal',
                              required=False)

    sesudah_pajak = fields.Integer(compute='_compute_sesudah_pajak',
                                   required=False)

    # ongkos_kirim = fields.Integer('Ongkos Kirim', compute='_compute_ongkir',
    #                         required=False)

    # sequence ID Order
    @api.model
    def create(self, vals):
        if vals.get('reference', _('Order ID :')) == _('Order ID :'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('restaurant.delivery') or _('Order ID :')
        res = super(delivery, self).create(vals)
        return res

    @api.depends('total', 'pajak')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.total + rec.pajak

    # @api.depends('sesudah_pajak', 'ongkos_kirim')
    # def _compute_ongkir(self):
    #     for rec in self:
    #         rec.ongkos_kirim = rec.sesudah_pajak * 10000

    # menghitung pajak
    @api.depends('total', 'pajak')
    def _compute_sesudah_pajak(self):
        for rec in self:
            rec.sesudah_pajak = rec.total + rec.pajak

    @api.depends('total', 'pajak')
    def _compute_pajak(self):
        for rec in self:
            rec.pajak = rec.total * 0.10

    @api.depends('deliverydetail_id')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['restaurant.deliverydetail'].search(
                [('delivery_id', '=', record.id)]).mapped('jumlah'))
            record.total = a

    # membuat sequence nomor delivery
    @api.model
    def create(self, vals):
        if vals.get('reference', _('Order ID :')) == _('Order ID :'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('restaurant.delivery') or _('Order ID :')
        res = super(delivery, self).create(vals)
        return res

    def action_diantar(self):
        for rec in self:
            rec.state = 'diantar'

    def action_selesai(self):
        for rec in self:
            rec.state = 'selesai'


class deliverydetail(models.Model):
    _name = 'restaurant.deliverydetail'
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
