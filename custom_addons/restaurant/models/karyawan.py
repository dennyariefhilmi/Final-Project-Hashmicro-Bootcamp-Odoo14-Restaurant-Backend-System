from odoo import fields, models, api, _
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


class karyawan(models.Model):
    _name = 'restaurant.karyawan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char("Nama", tracking=True)
    mulai_bekerja = fields.Date(string='Mulai Bekerja',
                                required=False, tracking=True)
    no_hp = fields.Char(string='No HP',
                        required=False, tracking=True)
    alamat = fields.Text(
        string='Alamat',
        required=False, tracking=True)

    role = fields.Selection(
        string='Role',
        selection=[('manajer', 'Manajer'),
                   ('supervisor', 'Supervisor'),
                   ('kitchen_staff', 'Kitchen Staff'),
                   ('pramusaji', 'Pramusaji'),
                   ('kasir', 'Kasir'),
                   ('driver', 'Driver')],
        required=False, tracking=True)

    usia = fields.Integer(string='Usia',
                          required=False,
                          tracking=True,
                          compute='_hitung_usia')

    jadwal_ids = fields.One2many(
        comodel_name='restaurant.jadwal',
        inverse_name='jadwal_shift',
        string='Jadwal ID',
        required=False, tracking=True)

    shift = fields.Selection(string='Shift',
                             selection=[('shift_1', 'Shift 1'),
                                        ('shift_2', 'Shift 2'),
                                        ('libur', 'Libur')],
                             required=False, tracking=True)
    status = fields.Selection(
        string='Status',
        selection=[('tetap', 'Tetap'),
                   ('kontrak', 'Kontrak'),
                   ('parttime', 'Part-time')],
        required=False, tracking=True, default='tetap')

    tanggal_lahir = fields.Date(
        string='Tanggal Lahir',
        required=False, default=fields.Date.today(), tracking=True)

    lama_bekerja = fields.Char(
        string='Lama Bekerja',
        compute='_lama_bekerja',
        required=False, tracking=True)

    reference = fields.Char(string='ID Karyawan', required=True, copy=False, readonly=True,
                            default=lambda self: _('ID Karyawan'), tracking=True)

    # menghitung umur karyawan
    # computing age
    @api.depends('tanggal_lahir')
    def _hitung_usia(self):
        for record in self:
            if record.tanggal_lahir is not False:
                record.usia = (datetime.today().date() - datetime.strptime(str(record.tanggal_lahir),
                                                                          '%Y-%m-%d').date()) // timedelta(days=365)
            else:
                record.age = 0.0

    # computing working time
    @api.depends('mulai_bekerja')
    # @api.multi
    def _lama_bekerja(self):
        for record in self:
            if record.mulai_bekerja:
                years = relativedelta(date.today(), record.mulai_bekerja).years
                months = relativedelta(date.today(), record.mulai_bekerja).months
                day = relativedelta(date.today(), record.mulai_bekerja).days
                record.lama_bekerja = str(int(years)) + ' Tahun ' + str(int(months)) + ' Bulan ' + str(day) + ' Hari'
            else:
                record.lama_bekerja = '0 Tahun 0 Bulan 0 Hari'
    @api.model
    def create(self, vals):
        if vals.get('reference', _('ID Karyawan')) == _('ID Karyawan'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('restaurant.karyawan') or _('ID Karyawan')
        res = super(karyawan, self).create(vals)
        return res


class Jadwal(models.Model):
    _name = 'restaurant.jadwal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Many2one(comodel_name='restaurant.karyawan',
                           string='Name',
                           required=False, tracking=True)

    role = fields.Many2one(comodel_name='restaurant.karyawan',
                           string='Role',
                           required=False, tracking=True)

    senin = fields.Selection(string='Senin',
                             selection=[('shift_1', 'Shift 1'),
                                        ('shift_2', 'Shift 2'),
                                        ('libur', 'Libur')],
                             required=False, tracking=True)
    selasa = fields.Selection(string='Selasa',
                              selection=[('shift_1', 'Shift 1'),
                                         ('shift_2', 'Shift 2'),
                                         ('libur', 'Libur')],
                              required=False, tracking=True)
    rabu = fields.Selection(string='Rabu',
                            selection=[('shift_1', 'Shift 1'),
                                       ('shift_2', 'Shift 2'),
                                       ('libur', 'Libur')],
                            required=False, tracking=True)
    kamis = fields.Selection(string='Kamis',
                             selection=[('shift_1', 'Shift 1'),
                                        ('shift_2', 'Shift 2'),
                                        ('libur', 'Libur')],
                             required=False, tracking=True)
    jumat = fields.Selection(string='Jumat',
                             selection=[('shift_1', 'Shift 1'),
                                        ('shift_2', 'Shift 2'),
                                        ('libur', 'Libur')],
                             required=False, tracking=True)
    sabtu = fields.Selection(string='Sabtu',
                             selection=[('shift_1', 'Shift 1'),
                                        ('shift_2', 'Shift 2'),
                                        ('libur', 'Libur')],
                             required=False, tracking=True)
    minggu = fields.Selection(string='Minggu',
                              selection=[('shift_1', 'Shift 1'),
                                         ('shift_2', 'Shift 2'),
                                         ('libur', 'Libur')],
                              required=False, tracking=True)
    jadwal_shift = fields.Many2one(
        comodel_name='restaurant.karyawan',
        string='Jadwal_shift',
        required=False, tracking=True)
