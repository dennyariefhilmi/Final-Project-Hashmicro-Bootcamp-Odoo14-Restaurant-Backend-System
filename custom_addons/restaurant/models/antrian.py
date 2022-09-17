from odoo import fields, models, api, _


class antrian(models.Model):
    _name = 'restaurant.antrian'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char('Atas Nama', tracking=True)
    qty = fields.Integer(string='Jumlah Orang',
                         required=False,
                         tracking=True)

    jam_datang = fields.Datetime(string='Jam Datang',
                                 required=False,
                                 default=fields.Datetime.now(),
                                 tracking=True)

    no_hp = fields.Char(string='No HP',
                        required=False,
                        tracking=True)

    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('Antrian'), tracking=True)

    # membuat sequence nomor antrian
    @api.model
    def create(self, vals):
        if vals.get('reference', _('Antrian')) == _('Antrian'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('restaurant.antrian') or _('Antrian')
        res = super(antrian, self).create(vals)
        return res

