from odoo import models, fields

class GestionProfesor(models.Model):
    _name = 'gestion.profesor'
    _description = 'Profesor'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre Completo', required=True)
    dni = fields.Char(string='Documento', required=True)
    domicilio = fields.Char(string='Domicilio')
    numero = fields.Char(string='Nº')
    piso = fields.Char(string='Piso')
    letra = fields.Char(string='Letra')
    cp = fields.Char(string='C.P.')
    telefono1 = fields.Char(string='Teléfono 1')
    telefono2 = fields.Char(string='Teléfono 2')
    email1 = fields.Char(string='Email 1')
    email2 = fields.Char(string='Email 2')
    
    usuario_id = fields.Many2one('res.users', string='Usuario Odoo')
    falta_ids = fields.One2many('gestion.falta', 'profesor_id', string='Faltas Reportadas')

    _sql_constraints = [
        ('dni_unique', 'unique(dni)', '¡El DNI del profesor ya existe!')
    ]