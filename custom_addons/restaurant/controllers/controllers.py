# -*- coding: utf-8 -*-
# from odoo import http


# class Restaurant(http.Controller):
#     @http.route('/restaurant/restaurant/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restaurant/restaurant/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('restaurant.listing', {
#             'root': '/restaurant/restaurant',
#             'objects': http.request.env['restaurant.restaurant'].search([]),
#         })

#     @http.route('/restaurant/restaurant/objects/<model("restaurant.restaurant"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restaurant.object', {
#             'object': obj
#         })
