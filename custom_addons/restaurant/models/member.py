from odoo import fields, models, api, _

class member(models.Model):
    _name = 'restaurant.member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char(string='Nama Member',
                       required=False, tracking=True)

    member_id = fields.Char(string='ID Pegawai', required=True, copy=False, readonly=True,
                            default=lambda self: _('ID Member :'),
                            tracking=True,)

    level = fields.Selection(string='Level',
                             selection=[('bronze', 'Bronze'),
                                        ('Silver', 'Silver'),
                                        ('gold', 'Gold'),
                                        ('platinum', 'Platinum')],
                             required=False, tracking=True)
    no_hp = fields.Char(string='No HP',
                        required=False,
                        tracking=True)
    tanggal_gabung = fields.Date(string='Tanggal Bergabung',
                                 required=False,
                                 tracking=True)

    tanggal_lahir = fields.Date(string='Tanggal Lahir',
                                required=False,
                                tracking=True)
    img_member = fields.Binary(string="Image Member",
                               required=False,
                               tracking=True)
    alamat = fields.Text(string="Alamat",
                         required=False)
    @api.model
    def create(self, vals):
        if vals.get('member_id', _('ID Member :')) == _('ID Member :'):
            vals['member_id'] = self.env['ir.sequence'].next_by_code('restaurant.member') or _('ID Member :')
            res = super(member, self).create(vals)
        return res
