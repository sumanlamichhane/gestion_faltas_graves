from odoo import models, fields, api

class GestionAlumno(models.Model):
    _name = 'gestion.alumno'
    _description = 'Alumno'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre Completo', required=True)
    nia = fields.Char(string='NIA', required=True)
    dni = fields.Char(string='Documento')
    domicilio = fields.Char(string='Calle/Vía')
    numero = fields.Char(string='Nº')
    piso = fields.Char(string='Piso')
    localidad = fields.Char(string='Localidad/Municipio')
    telefono1 = fields.Char(string='Teléfono 1')
    telefono2 = fields.Char(string='Teléfono 2')
    email1 = fields.Char(string='Email')
    
    grupo_id = fields.Many2one('gestion.grupo', string='Grupo')
    foto = fields.Image(string="Foto Alumno", max_width=200, max_height=200)
    total_faltas = fields.Integer(string="Total Faltas", compute="_compute_total_faltas") 
    falta_ids = fields.One2many('gestion.falta', 'alumno_id', string="Historial de Faltas")

    @api.depends('falta_ids')
    def _compute_total_faltas(self):
        for record in self:
            record.total_faltas = len(record.falta_ids)