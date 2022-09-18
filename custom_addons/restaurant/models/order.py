from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class order(models.Model):
    _name = 'restaurant.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Selection(
        string='Meja',
        selection=[('table_1', 'Table 1'),
                   ('table_2', 'Table 2'),
                   ('table_3', 'Table 3'),
                   ('table_4', 'Table 4'),
                   ('table_5', 'Table 5'),
                   ('table_6', 'Table 6'),
                   ('table_7', 'Table 7'),
                   ('table_8', 'Table 8'),
                   ('table_9', 'Table 9'),
                   ('table_10', 'Table 10'),
                   ],
        required=False,
        tracking=True)

    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('Order ID :'), tracking=True)

    jumlah_orang = fields.Selection(string='Jumlah Orang',
                                    selection=[('1', '1'),
                                               ('2', '2'),
                                               ('3', '3'),
                                               ('4', '4'),
                                               ('5', '5'),
                                               ('8', '8'),
                                               ('7', '7'),
                                               ('8', '8'), ],
                                    required=False,
                                    tracking=True)
    state = fields.Selection(
        string='Status',
        selection=[('kosong', 'Kosong'),
                   ('full', 'Full'),
                   ('selesai', 'Selesai')],
        required=True,
        default='kosong',
        tracking=True)

    jam_mulai = fields.Datetime(string='Jam Mulai',
                                required=False,
                                default=fields.Datetime.now(), tracking=True)

    orderdetail_id = fields.One2many(comodel_name='restaurant.orderdetail',
                                     inverse_name='order_id',
                                     string='orderdetail_id',
                                     required=False)

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
    member = fields.Boolean(string='Member',
                            required=False)

    member_ids = fields.Many2one(
        comodel_name='restaurant.member',
        string='Member_ids',
        required=False)

    id_member = fields.Char(
        compute="_compute_id_member",
        string='Id Member',
        required=False)

    tipe_pembayaran = fields.Selection(string='Tipe Pembayaran',
                                       selection=[('tunai', 'Tunai'),
                                                  ('emoney', 'E-Money'),
                                                  ('debit', 'Kartu Debit'),
                                                  ('kredit', 'Kartu Kredit')],
                                       required=False, )

    sesudah_pajak = fields.Integer(compute='_compute_sesudah_pajak',
                                   required=False)
    diskon = fields.Integer('Diskon 5%', compute='_compute_diskon',
                            required=False)

    @api.depends('id_member')
    def _compute_id_member(self):
        for rec in self:
            rec.id_member = rec.member_ids.id_member

    @api.depends('total', 'pajak', 'diskon')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.total + rec.pajak - rec.diskon

    @api.depends('sesudah_pajak', 'diskon')
    def _compute_diskon(self):
        for rec in self:
            rec.diskon = rec.sesudah_pajak * 0.05

    # menghitung pajak
    @api.depends('total', 'pajak')
    def _compute_sesudah_pajak(self):
        for rec in self:
            rec.sesudah_pajak = rec.total + rec.pajak

    @api.depends('total', 'pajak')
    def _compute_pajak(self):
        for rec in self:
            rec.pajak = rec.total * 0.10

    # action state
    def action_full(self):
        for rec in self:
            rec.state = 'full'

    def action_selesai(self):
        for rec in self:
            rec.state = 'selesai'

    # def write(self, vals):
    #     if any(state == 'selesai' for state in set(self.mapped('state'))):
    #         raise UserError(_("Tidak bisa diubah"))
    #     else:
    #         return super().write(vals)

    # membuat sequence nomor order
    @api.model
    def create(self, vals):
        if vals.get('reference', _('Order ID :')) == _('Order ID :'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('restaurant.order') or _('Order ID :')
        res = super(order, self).create(vals)
        return res

    @api.depends('orderdetail_id')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['restaurant.orderdetail'].search(
                [('order_id', '=', record.id)]).mapped('jumlah'))
            record.total = a


class orderdetail(models.Model):
    _name = 'restaurant.orderdetail'
    _description = 'Order Detail'

    name = fields.Char()

    order_id = fields.Many2one(comodel_name='restaurant.order',
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
