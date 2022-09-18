# from odoo import models, fields
#
#
# class bahan_makanan(models.AbstractModel):
#     _name = 'report.restaurant.report_bahan_makanan_xlsx'
#     _inherit = 'report.report_xlsx.abstract'
#
#     tgl_lap = fields.Date.today()
#
#     def generate_xlsx_report(self, workbook, data, supplier):
#         sheet = workbook.add_worksheet('Daftar Bahan Makanan')
#         bold = workbook.add_format({'bold': True})
#         sheet.write(0, 0, str(self.tgl_lap))
#         sheet.write(1, 0, 'Nama Perusahaan')
#         sheet.write(1, 1, 'Alamat')
#         sheet.write(1, 2, 'No. Telepon')
#         sheet.write(1, 3, 'Produk')
#         row = 2
#         col = 0
#         for obj in supplier:
#             col = 0
#             sheet.write(row, col, obj.name)
#             sheet.write(row, col+1, obj.alamat)
#             sheet.write(row, col+2, obj.no_telp)
#             for xxx in obj.barang_id:
#                 sheet.write(row, col+3, xxx.name)
#                 col += 1
#             row += 1