import base64
import logging
from lxml import etree
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ImportadorDatosWizard(models.TransientModel):
    _name = 'gestion.importador.wizard'
    _description = 'Importador'

    archivo_xml = fields.Binary(string='Archivo XML', required=True)
    tipo_importacion = fields.Selection([
        ('profesores', 'Profesores'),
        ('grupos', 'Grupos'),
        ('alumnos', 'Alumnos')
    ], string='Tipo', required=True)

    def action_importar(self):
        if not self.archivo_xml:
            return
        
        xml_content = base64.b64decode(self.archivo_xml)
        try:
            root = etree.fromstring(xml_content)
        except Exception as e:
            raise UserError(f"Error XML: {str(e)}")

        # --- PROFESORES ---
        if self.tipo_importacion == 'profesores':
            docentes = root.xpath('//docente')
            for d in docentes:
                dni = d.get('documento')
                if dni:
                    existente = self.env['gestion.profesor'].search([('dni', '=', dni)])
                    if not existente:
                        self.env['gestion.profesor'].create({
                            'nombre': f"{d.get('nombre')} {d.get('apellido1')} {d.get('apellido2') or ''}".strip(),
                            'dni': dni,
                            'domicilio': d.get('domicilio'),
                            'telefono1': d.get('telefono1'),
                            'email1': d.get('email1'),
                        })

        # --- GRUPOS ---
        elif self.tipo_importacion == 'grupos':
            grupos = root.xpath('//grupo')
            for g in grupos:
                codigo = g.get('codigo')
                if codigo:
                    existente = self.env['gestion.grupo'].search([('nombre', '=', codigo)])
                    if not existente:
                        # Buscamos el tutor por el DNI que viene en 'tutor_ppal'
                        tutor_dni = g.get('tutor_ppal')
                        tutor = self.env['gestion.profesor'].search([('dni', '=', tutor_dni)], limit=1)
                        
                        self.env['gestion.grupo'].create({
                            'nombre': codigo,
                            'denominacion': g.get('nombre'),
                            'aula': g.get('aula').strip() if g.get('aula') else '',
                            'tutor_id': tutor.id if tutor else False,
                        })

        # --- ALUMNOS ---
        elif self.tipo_importacion == 'alumnos':
            alumnos = root.xpath('//alumno')
            for a in alumnos:
                nia = a.get('NIA')
                if nia:
                    existente = self.env['gestion.alumno'].search([('nia', '=', nia)])
                    if not existente:
                        # Buscamos el grupo por el código exacto
                        cod_grupo = a.get('grupo')
                        grupo = self.env['gestion.grupo'].search([('nombre', '=', cod_grupo)], limit=1)
                        
                        self.env['gestion.alumno'].create({
                            'nombre': f"{a.get('nombre')} {a.get('apellido1')} {a.get('apellido2') or ''}".strip(),
                            'nia': nia,
                            'dni': a.get('documento'),
                            'grupo_id': grupo.id if grupo else False,
                            'email1': a.get('email1'),
                            'telefono1': a.get('telefono1'),
                            'localidad': a.get('municipio_nac_ext'),
                        })

        # Esto fuerza a la interfaz a recargar los datos
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Éxito',
                'message': 'Datos importados correctamente',
                'sticky': False,
                'next': {'type': 'ir.actions.client', 'tag': 'reload'},
            }
        }