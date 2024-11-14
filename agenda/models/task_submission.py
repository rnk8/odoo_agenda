from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class SchoolTaskSubmission(models.Model):
    _name = 'school.task.submission'
    _description = 'Entrega de Tarea'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    teacher_id = fields.Many2one(
        'school.teacher', string='Maestro',
        related='task_id.teacher_id', store=True, readonly=True)
    subject_id = fields.Many2one(
        'school.subject', string='Materia',
        related='task_id.subject_id', store=True, readonly=True)
    task_id = fields.Many2one(
        'school.task', string='Tarea', required=True, ondelete='cascade')
    student_id = fields.Many2one(
        'school.student', string='Estudiante', required=True)
    submission_date = fields.Datetime(string='Fecha de Entrega')
    attachment = fields.Binary(string='Archivo Adjunto')
    attachment_filename = fields.Char(string='Nombre del Archivo')
    grade = fields.Float(string='Calificación')
    feedback = fields.Text(string='Comentarios')
    due_date = fields.Date(
        related='task_id.due_date', store=True, string='Fecha de Vencimiento')
    status = fields.Selection([
        ('pending', 'Pendiente'),
        ('submitted', 'Enviada'),
        ('graded', 'Calificada'),
    ], default='pending', tracking=True)
    
    message = fields.Html(
        string='Respuesta', required=True, default=lambda self: '<p></p>')

    course_id = fields.Many2one(
        'school.course', string='Curso',
        related='task_id.course_id', store=True, readonly=True)
    
    
    # Campo de rúbrica (opcional)
    rubric_ids = fields.Many2many(
        comodel_name='school.task.rubric',
        compute='_compute_rubric_ids',
        string='Rúbrica'
    )

    @api.depends('task_id')
    def _compute_rubric_ids(self):
        for record in self:
            record.rubric_ids = record.task_id.rubric_ids

    def submit_task(self):
        """Permite solo al estudiante enviar la tarea."""
        for rec in self:
            if rec.student_id.user_id.id != self.env.uid:
                raise UserError("Solo el estudiante puede enviar esta tarea.")
            if rec.status != 'pending':
                raise UserError("La tarea ya ha sido enviada o calificada.")
            rec.status = 'submitted'
            rec.submission_date = fields.Datetime.now()

    def grade_task(self):
        """Permite solo al maestro calificar la tarea."""
        for rec in self:
            if rec.teacher_id.user_id.id != self.env.uid:
                raise UserError("Solo el maestro puede calificar esta tarea.")
            if rec.status != 'submitted':
                raise UserError("Solo se pueden calificar tareas enviadas.")
            if rec.grade is None and rec.grade != 0:
                raise UserError("Debe asignar una calificación antes de marcar la tarea como calificada.")
            rec.status = 'graded'

    @api.constrains('grade')
    def _check_grade(self):
        for record in self:
            if record.grade < 0 or record.grade > record.task_id.max_grade:
                raise ValidationError("La calificación debe estar entre 0 y la calificación máxima")
