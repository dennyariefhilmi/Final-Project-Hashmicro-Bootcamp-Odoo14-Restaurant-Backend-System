from odoo import models, fields
import base64
import io

class Bahan(models.AbstractModel):
    _name = 'report.restaurant.report_bahan_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, bahan):
        sheet = workbook.add_worksheet('Daftar Bahan Makanan')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, str(self.tgl_lap))
        sheet.write(1, 0, 'Nama Bahan')
        sheet.write(1, 1, 'Tipe')
        sheet.write(1, 2, 'Qty')
        sheet.write(1, 3, 'Tanggal Datang')
        sheet.write(1, 4, 'Tanggal Kadaluarsa')
        row = 2
        col = 0
        for obj in bahan:
            col = 0
            sheet.write(row, col, obj.name)
            sheet.write(row, col+1, obj.tipe)
            sheet.write(row, col+2, obj.qty)
            sheet.write(row, col + 3, obj.tgl_datang)
            sheet.write(row, col + 4, obj.kadaluarsa)