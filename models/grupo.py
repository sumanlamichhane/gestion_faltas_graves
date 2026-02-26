from odoo import models, fields

class GestionGrupo(models.Model):
    _name = 'gestion.grupo'
    _description = 'Grupos'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Código del Grupo', required=True)
    denominacion = fields.Char(string='Nombre Completo')
    aula = fields.Char(string='Aula')
    tutor_id = fields.Many2one('gestion.profesor', string='Tutor Principal')
    falta_ids = fields.One2many('gestion.falta', 'grupo_id', string='Faltas del Grupo')