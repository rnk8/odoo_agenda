from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class SchoolTask(models.Model):
    _name = 'school.task'
    _description = 'Tarea'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Título', required=True)
    description = fields.Text(string='Descripción')
    due_date = fields.Date(string='Fecha de Vencimiento')

    teacher_id = fields.Many2one('school.teacher', string='Maestro', required=True)
    subject_id = fields.Many2one('school.subject', string='Materia', required=True)
    course_id = fields.Many2one('school.course', string='Curso')
    student_ids = fields.Many2many('school.student', string='Estudiantes Específicos')

    submission_ids = fields.One2many('school.task.submission', 'task_id', string='Entregas')

    progress = fields.Float(string='Progreso', compute='_compute_progress', store=True)

    max_grade = fields.Float(string='Calificación Máxima', default=100.0)
    weight = fields.Float(string='Peso en la Nota Final', default=1.0)
    category = fields.Selection([
        ('homework', 'Tarea'),
        ('exam', 'Examen'),
        ('project', 'Proyecto')
    ], default='homework', string='Categoría')

    rubric_ids = fields.One2many('school.task.rubric', 'task_id', string='Rúbrica')

    priority = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Normal'),
        ('2', 'Alta'),
    ], default='1', string='Prioridad')

    @api.depends('submission_ids.status')
    def _compute_progress(self):
        for task in self:
            total = len(task.submission_ids)
            if total:
                graded = len(task.submission_ids.filtered(lambda s: s.status == 'graded'))
                task.progress = (graded / total) * 100
            else:
                task.progress = 0.0

    @api.model
    def default_get(self, fields_list):
        res = super(SchoolTask, self).default_get(fields_list)
        teacher = self.env['school.teacher'].search([('user_id', '=', self.env.uid)], limit=1)
        if teacher:
            res['teacher_id'] = teacher.id
            if teacher.subject_ids:
                res['subject_id'] = teacher.subject_ids[0].id  # Asigna la primera materia si existe
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'teacher_id' not in vals:
                teacher = self.env['school.teacher'].search([('user_id', '=', self.env.uid)], limit=1)
                if teacher:
                    vals['teacher_id'] = teacher.id
                    if teacher.subject_ids:
                        vals['subject_id'] = teacher.subject_ids[0].id
                else:
                    raise UserError("No tienes permisos para crear tareas.")
        tasks = super(SchoolTask, self).create(vals_list)
        tasks.assign_task_to_students()
        tasks.schedule_reminder()
        return tasks

    def assign_task_to_students(self):
        for task in self:
            students = task.student_ids
            if task.course_id and not students:
                students = task.course_id.student_ids
            elif not students:
                raise UserError("Debes asignar un curso o estudiantes específicos a la tarea.")

            for student in students:
                self.env['school.task.submission'].create({
                    'task_id': task.id,
                    'student_id': student.id,
                    'teacher_id': task.teacher_id.id,
                    'subject_id': task.subject_id.id
                })

    @api.onchange('teacher_id')
    def _onchange_teacher_id(self):
        if self.teacher_id:
            return {'domain': {'course_id': [('id', 'in', self.teacher_id.course_ids.ids)]}}
        return {'domain': {'course_id': []}}

    def schedule_reminder(self):
        for task in self:
            if task.due_date:
                reminder_date = fields.Date.from_string(task.due_date) - timedelta(days=2)
                if reminder_date > fields.Date.today():
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'summary': 'Recordatorio de Tarea',
                        'date_deadline': reminder_date,
                        'res_model_id': self.env['ir.model']._get('school.task').id,
                        'res_id': task.id,
                        'user_id': task.teacher_id.user_id.id,
                    })
           
from odoo import models, fields

class SchoolTaskRubric(models.Model):
    _name = 'school.task.rubric'
    _description = 'Rubric for Task'

    task_id = fields.Many2one('school.task', string='Task', required=True, ondelete='cascade') 
    criterion = fields.Char(string='Criterion', required=True)
    description = fields.Text(string='Description')
    max_score = fields.Float(string='Maximum Score', default=10.0)
        
 
    criteria = fields.Char(string='Criteria', required=True)
    weight = fields.Float(string='Weight')
    score = fields.Float(string='Score')
    comments = fields.Text(string='Comments')