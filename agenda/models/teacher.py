# custom_addons/agenda/models/teacher.py

from odoo import models, fields, api

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Maestro'

    name = fields.Char(string='Nombre', required=True)
    login = fields.Char(string='Usuario (login)')
    password = fields.Char(string='Contraseña')
    user_id = fields.Many2one('res.users', string='Usuario', required=True, ondelete='cascade')
    
    subject_ids = fields.Many2many('school.subject', string='Materias')
    course_ids = fields.Many2many('school.course', string='Cursos')
    task_ids = fields.One2many('school.task', 'teacher_id', string='Tareas')
    task_submission_ids = fields.One2many('school.task.submission', 'teacher_id', string="Entregar Nota")

    @api.model_create_multi
    def create(self, vals_list):
        teachers = super(SchoolTeacher, self).create(vals_list)
        for teacher, vals in zip(teachers, vals_list):
            if 'login' in vals and 'password' in vals:
                user_vals = {
                    'name': vals.get('name'),
                    'login': vals.get('login'),
                    'password': vals.get('password'),
                    'groups_id': [
                        (6, 0, [
                            self.env.ref('base.group_user').id,
                            self.env.ref('agenda.group_teacher').id
                        ])
                    ]
                }
                user = self.env['res.users'].create(user_vals)
                teacher.user_id = user.id
        return teachers