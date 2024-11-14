# custom_addons/agenda/models/communication.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SchoolCommunication(models.Model):
    _name = 'school.communication'
    _description = 'Comunicación de Administración'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char(string='Título', required=True)
    message = fields.Html(string='Mensaje', required=True, default=lambda self: '<p></p>')
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    attachment_ids = fields.One2many('school.communication.attachment', 'communication_id', string='Archivos Adjuntos')
    recipient_type = fields.Selection([
        ('all', 'Todos'),
        ('teachers', 'Maestros'),
        ('students', 'Estudiantes'),
        ('parents', 'Padres'),
    ], string='Destinatarios', required=True, default='all')

    category_id = fields.Many2one('school.communication.category', string='Categoría')
    priority = fields.Selection([
        ('low', 'Baja'),
        ('normal', 'Normal'),
        ('high', 'Alta'),
    ], string='Prioridad', default='normal')
    tag_ids = fields.Many2many('school.communication.tag', string='Etiquetas')

    @api.constrains('attachment_ids')
    def _check_attachments(self):
        for record in self:
            for attachment in record.attachment_ids:
                if not attachment.filename.lower().endswith('.pdf'):
                    raise ValidationError("Solo se permiten archivos PDF como adjuntos.")

class SchoolCommunicationAttachment(models.Model):
    _name = 'school.communication.attachment'
    _description = 'Adjunto de Comunicación de Administración'

    communication_id = fields.Many2one('school.communication', string='Comunicación', ondelete='cascade')
    filename = fields.Char(string='Nombre del Archivo')
    file = fields.Binary(string='Archivo', required=True)

class SchoolCommunicationCategory(models.Model):
    _name = 'school.communication.category'
    _description = 'Categoría de Comunicación'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color')

class SchoolCommunicationTag(models.Model):
    _name = 'school.communication.tag'
    _description = 'Etiqueta de Comunicación'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color')
