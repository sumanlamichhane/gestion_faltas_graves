import base64
from lxml import etree
from odoo import models, fields, api
from odoo.exceptions import UserError

class ImportadorDatosWizard(models.TransientModel):
    _name = 'gestion.importador.wizard'
    _description = 'Importador de Datos'

    archivo_xml = fields.Binary(string='Archivo XML', required=True)
    tipo_importacion = fields.Selection([
        ('profesores', 'Profesores'),
        ('grupos', 'Grupos'),
        ('alumnos', 'Alumnos')
    ], string='¿Qué vas a importar?', required=True)

    def action_importar(self):
        if not self.archivo_xml:
            return
        
        xml_content = base64.b64decode(self.archivo_xml)
        try:
            root = etree.fromstring(xml_content)
        except Exception as e:
            raise UserError(f"Error en el formato del XML: {str(e)}")

        # 1. PROFESORES (Mapeo: nombre, documento -> dni)
        if self.tipo_importacion == 'profesores':
            for doc in root.xpath('//docente'):
                dni = doc.get('documento')
                if dni and not self.env['gestion.profesor'].search([('dni', '=', dni)]):
                    self.env['gestion.profesor'].create({
                        'nombre': f"{doc.get('nombre')} {doc.get('apellido1')}",
                        'dni': dni,
                    })

        # 2. GRUPOS (Mapeo: codigo -> nombre, aula, tutor_ppal -> tutor_id)
        elif self.tipo_importacion == 'grupos':
            for g in root.xpath('//grupo'):
                codigo = g.get('codigo') # Usamos el código corto tipo "2CFSJ"
                if codigo and not self.env['gestion.grupo'].search([('nombre', '=', codigo)]):
                    tutor = self.env['gestion.profesor'].search([('dni', '=', g.get('tutor_ppal'))], limit=1)
                    self.env['gestion.grupo'].create({
                        'nombre': codigo,
                        'aula': g.get('aula') or 'Sin Aula',
                        'tutor_id': tutor.id if tutor else False,
                    })

        # 3. ALUMNOS (Mapeo: NIA, nombre, grupo -> grupo_id)
        elif self.tipo_importacion == 'alumnos':
            for al in root.xpath('//alumno'):
                nia = al.get('NIA')
                if nia and not self.env['gestion.alumno'].search([('nia', '=', nia)]):
                    grupo = self.env['gestion.grupo'].search([('nombre', '=', al.get('grupo'))], limit=1)
                    self.env['gestion.alumno'].create({
                        'nombre': f"{al.get('nombre')} {al.get('apellido1')}",
                        'nia': nia,
                        'grupo_id': grupo.id if grupo else False,
                    })

        return {'type': 'ir.actions.client', 'tag': 'reload'}