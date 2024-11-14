# custom_addons/agenda/models/course.py

from odoo import models, fields

class SchoolCourse(models.Model):
    _name = 'school.course'
    _description = 'Curso'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    subject_ids = fields.Many2many('school.subject', string='Materias')
    teacher_ids = fields.Many2many('school.teacher', string='Maestros')
    student_ids = fields.One2many('school.student', 'course_id', string='Estudiantes')
    task_ids = fields.One2many('school.task', 'course_id', string='Tareas')
    term_id = fields.Many2one('school.academic.term', string='Periodo Académico') 
    
    def calculate_student_average(self, student_id):
        submissions = self.env['school.task.submission'].search([
            ('student_id', '=', student_id),
            ('task_id.course_id', '=', self.id),
            ('status', '=', 'graded')
        ])
        weighted_sum = sum(s.grade * s.task_id.weight for s in submissions)
        total_weight = sum(s.task_id.weight for s in submissions)
        return weighted_sum / total_weight if total_weight else 0.0
    
class AcademicTerm(models.Model):
    _name = 'school.academic.term'
    _description = 'Academic Term'  # Add this line
 
    name = fields.Char(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    course_ids = fields.One2many('school.course', 'term_id', string='Cursos') 