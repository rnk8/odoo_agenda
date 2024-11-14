# custom_addons/agenda/models/student.py

from odoo import models, fields, api
from odoo.exceptions import UserError

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Estudiante'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add this line

    name = fields.Char(string='Nombre', required=True)
    login = fields.Char(string='Usuario (login)', required=True)
    password = fields.Char(string='Contraseña', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', required=True, ondelete='cascade')
    parent_id = fields.Many2one('school.parent', string='Padre', ondelete='set null')
    course_id = fields.Many2one('school.course', string='Curso', required=True)
    task_submission_ids = fields.One2many(
        'school.task.submission', 'student_id', string="Entregas de Tareas"
    )
    task_id = fields.Many2one('school.task', string="Tarea")
    status = fields.Selection([
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded')
    ], string="Status", default="pending", tracking=True)
    grade = fields.Float(string="Nota")
    
    
    
    @api.model_create_multi
    def create(self, vals_list):
        students = super(SchoolStudent, self).create(vals_list)
        for student, vals in zip(students, vals_list):
            if 'login' in vals and 'password' in vals:
                user_vals = {
                    'name': vals.get('name'),
                    'login': vals.get('login'),
                    'password': vals.get('password'),
                    'groups_id': [
                        (6, 0, [
                            self.env.ref('base.group_user').id,
                            self.env.ref('agenda.group_student').id
                        ])
                    ]
                }
                user = self.env['res.users'].create(user_vals)
                student.user_id = user.id
        return students