from odoo import models, fields, api

class InformeTrimestreWizard(models.TransientModel):
    _name = 'gestion.informe.trimestre.wizard'
    _description = 'Filtro de Partes por Fechas'

    fecha_inicio = fields.Date(string='Fecha Inicio', required=True, default=fields.Date.context_today)
    fecha_fin = fields.Date(string='Fecha Fin', required=True, default=fields.Date.context_today)

    def action_generar_informe(self):
        # Buscamos las faltas que caen en ese rango (comparando solo la parte fecha del Datetime)
        faltas = self.env['gestion.falta'].search([
            ('fecha_hora', '>=', self.fecha_inicio),
            ('fecha_hora', '<=', self.fecha_fin)
        ])
        
        # Usamos el informe de resumen que ya tienes definido en report_faltas.xml
        return self.env.ref('gestion_faltas_graves.action_report_resumen_faltas').report_action(faltas)