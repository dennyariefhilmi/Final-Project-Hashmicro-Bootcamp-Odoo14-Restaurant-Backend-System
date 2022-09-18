from odoo import fields, models, api


class orderreport(models.TransientModel):
    _name = 'restaurant.orderreport'
    _description = 'Description'

    reference = fields.Many2one(
        comodel_name='restaurant.order',
        string='No. Order',
        required=False)

    def action_order_report(self):
        filter = []
        reference = self.reference
        if reference:
            filter += [('reference', '=', reference.id)]
        print(filter)
        order = self.env['restaurant.order'].search_read(filter)
        print(order)
        data = {
            'form': self.read()[0],
            'order': order,
        }
        print(data)
        return self.env.ref('restaurant.wizard_penjualanreport_pdf').report_action(self, data=data)
