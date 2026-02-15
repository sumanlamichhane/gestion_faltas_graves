from odoo import models, fields

class GestionGrupo(models.Model):
    _name = 'gestion.grupo'
    _description = 'Grupos'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre del Grupo', required=True)
    aula = fields.Char(string='Aula')
    tutor_id = fields.Many2one('gestion.profesor', string='Tutor')
    falta_ids = fields.One2many('gestion.falta', 'grupo_id', string='Faltas del Grupo')