from odoo import models, fields

class GestionProfesor(models.Model):
    _name = 'gestion.profesor'
    _description = 'Profesor'
    _rec_name = 'nombre'

    

    nombre = fields.Char(string='Nombre del Profesor', required=True)
    dni = fields.Char(string='DNI', required=True)
    usuario_id = fields.Many2one('res.users', string='Usuario Odoo')
