{
    'name': 'Gestión de Faltas',
    'version': '1.0',
    'summary': 'Módulo para gestionar las faltas del instituto',
    'author': 'Equipo de desarrollo',
    'category': 'Education',
    'depends': ['base', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/ir.sequence.xml',
        'views/alumno_views.xml',
        'views/profesor_views.xml',
        'views/grupo_views.xml',
        'views/asignatura_views.xml',
        'views/motivo_views.xml',
        'views/falta_views.xml',
        'views/views.xml',
        'reports/report_faltas.xml',
        
        'demo/demo.xml',  
    ],
    
    'installable': True,
    'application': True,
}