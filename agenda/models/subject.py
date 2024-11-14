# custom_addons/agenda/models/subject.py

from odoo import models, fields

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Materia'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    teacher_ids = fields.Many2many('school.teacher', string='Maestros')
