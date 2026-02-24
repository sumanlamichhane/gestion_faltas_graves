from odoo import models, fields, api

class InformeTrimestreWizard(models.TransientModel):
    _name = 'gestion.informe.trimestre.wizard'
    _description = 'Filtro de Partes por Fechas'

    fecha_inicio = fields.Date(string='Fecha Inicio', required=True, default=fields.Date.context_today)
    fecha_fin = fields.Date(string='Fecha Fin', required=True, default=fields.Date.context_today)

    def action_generar_informe(self):
        faltas = self.env['gestion.falta'].search([
            ('fecha_hora', '>=', self.fecha_inicio),
            ('fecha_hora', '<=', self.fecha_fin)
        ])
        
        return self.env.ref('gestion_faltas_graves.action_report_resumen_faltas').report_action(faltas)