from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

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
    testigos = fields.Text(
    string='Testigos', 
    placeholder='Nombres de alumnos o profesores que lo vieron...',
    help='Si no hay testigos, dejar en blanco' 
)
    
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

    @api.onchange('asignatura_id')
    def _onchange_asignatura_id(self):
        """Auto-asigna el profesor de la asignatura seleccionada"""
        if self.asignatura_id and self.asignatura_id.profesor_id:
            self.profesor_id = self.asignatura_id.profesor_id

    def action_cerrar_falta(self):
        self.estado = 'cerrado'

    def action_reabrir_falta(self):
        self.estado = 'borrador'

    @api.constrains('fecha_llamada')
    def _check_fecha_llamada(self):
        for record in self:
            if record.fecha_llamada and record.fecha_llamada > fields.Datetime.now():
                raise ValidationError("La fecha de la llamada no puede ser futura.")