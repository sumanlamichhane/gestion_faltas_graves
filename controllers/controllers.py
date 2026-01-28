# -*- coding: utf-8 -*-
# from odoo import http


# class GestionFaltasGraves(http.Controller):
#     @http.route('/gestion_faltas_graves/gestion_faltas_graves', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_faltas_graves/gestion_faltas_graves/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_faltas_graves.listing', {
#             'root': '/gestion_faltas_graves/gestion_faltas_graves',
#             'objects': http.request.env['gestion_faltas_graves.gestion_faltas_graves'].search([]),
#         })

#     @http.route('/gestion_faltas_graves/gestion_faltas_graves/objects/<model("gestion_faltas_graves.gestion_faltas_graves"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_faltas_graves.object', {
#             'object': obj
#         })
