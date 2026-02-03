from odoo import models, fields

class GestionAsignatura(models.Model):
    _name = 'gestion.asignatura'
    _description = 'Asignatura'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre Asignatura', required=True)
    profesor_id = fields.Many2one('gestion.profesor', string='Profesor Responsable')