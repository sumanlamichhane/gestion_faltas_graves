from odoo import models, fields, api
from datetime import datetime

class GestionFalta(models.Model):
    _name = 'gestion.falta'
    _description = 'Faltas Graves'
    _rec_name = 'numero_parte'
    _order = 'fecha_hora desc'

    numero_parte = fields.Char(string='Nº Parte', required=True, copy=False, readonly=True,
                              default=lambda self: self.env['ir.sequence'].next_by_code('gestion.falta'))
    
    alumno_id = fields.Many2one('gestion.alumno', string='Alumno', required=True)
    nia = fields.Char(string='NIA', related='alumno_id.nia', readonly=True)
    grupo_id = fields.Many2one('gestion.grupo', string='Grupo', related='alumno_id.grupo_id', store=True)
    profesor_id = fields.Many2one('gestion.profesor', string='Profesor', required=True,
                                 default=lambda self: self._get_default_profesor())
    asignatura_id = fields.Many2one('gestion.asignatura', string='Asignatura')
    
    fecha_hora = fields.Datetime(string='Fecha y Hora', required=True, default=fields.Datetime.now)
    lugar = fields.Selection([
        ('aula', 'Aula'),
        ('pasillo', 'Pasillo'),
        ('patio', 'Patio'), 
        ('gimnasio', 'Gimnasio'),
        ('otros', 'Otros')
    ], string='Lugar', required=True, default='aula')
    
    motivo_id = fields.Many2one('gestion.motivo', string='Motivo Sanción', required=True)
    descripcion_hechos = fields.Text(string='Descripción Hechos', required=True)
    testigos = fields.Text(string='Testigos')
    
    llamada_familia = fields.Selection([
        ('llamada', 'Llamada OK'),
        ('sin_contestar', 'Sin contestar'),
        ('no_llamada', 'No llamada')
    ], string='Llamada Familia', default='no_llamada')
    
    fecha_llamada = fields.Datetime(string='Fecha Llamada')
    observaciones_familia = fields.Text(string='Obs. Familia')
    
    medidas_iniciales = fields.Text(string='Medidas Iniciales')
    observaciones_directiva = fields.Text(string='Obs. Directiva')
    
    estado = fields.Selection([
        ('borrador', 'Abierto'),
        ('en_instruccion', 'En Instrucción'),
        ('cerrado', 'Cerrado'),
        ('resuelto', 'Resuelto')
    ], string='Estado', default='borrador', required=True)

    @api.model
    def _get_default_profesor(self):
        profesor = self.env['gestion.profesor'].search([('usuario_id', '=', self.env.user.id)], limit=1)
        return profesor.id if profesor else False

    def action_cerrar_falta(self):
        self.estado = 'cerrado'

    def action_reabrir_falta(self):
        self.estado = 'borrador'
