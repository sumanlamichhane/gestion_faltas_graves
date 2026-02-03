from odoo import models, fields, api

class GestionProfesor(models.Model):
    _name = 'gestion.profesor'
    _description = 'Profesor'
    _rec_name = 'nombre'

    

    nombre = fields.Char(string='Nombre del Profesor', required=True)
    dni = fields.Char(string='DNI', required=True)
    usuario_id = fields.Many2one('res.users', string='Usuario Odoo')

    _sql_constraints = [
        ('dni_unique', 'unique(dni)', '¡El DNI del profesor ya existe en el sistema!')
    ]