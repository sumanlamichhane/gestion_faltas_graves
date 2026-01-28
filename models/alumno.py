from odoo import models, fields

class GestionAlumno(models.Model):
    _name = 'gestion.alumno'
    _description = 'Alumno'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre Completo', required=True)
    nia = fields.Char(string='NIA', required=True)
    grupo_id = fields.Many2one('gestion.grupo', string='Grupo')
