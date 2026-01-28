from odoo import models, fields

class GestionMotivo(models.Model):
    _name = 'gestion.motivo'
    _description = 'Motivos Sanción'
    _rec_name = 'descripcion'

    codigo = fields.Char(string='Código (F-001)', required=True)
    descripcion = fields.Char(string='Descripción', required=True)
    dias_sancion_min = fields.Integer(string='Días Mínimos', default=3)
    dias_sancion_max = fields.Integer(string='Días Máximos', default=10)
    es_grave = fields.Boolean(string='Falta Grave', default=True)
