# custom_addons/agenda/__manifest__.py

{
    'name': 'Agenda Escolar',
    'version': '1.0',
    'summary': 'Gestión escolar de estudiantes, maestros, cursos y tareas',
    'description': 'Módulo para gestionar estudiantes, maestros, cursos, tareas, entregas y comunicaciones de la administración.',
    'author': 'Rene el choma de martinez',
    'depends': ['base', 'contacts', 'mail', 'portal'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/parent_views.xml',
        'views/student_views.xml',
        'views/teacher_views.xml',
        'views/course_views.xml',
        'views/subject_views.xml',
        'views/task_views.xml',
        'views/task_calendar_views.xml',
        'views/communication_views.xml',
        'views/views_both.xml',
        'views/menu.xml',
    ],  
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
