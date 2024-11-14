# custom_addons/agenda/models/parent.py

from odoo import models, fields, api

class SchoolParent(models.Model):
    _name = 'school.parent'
    _description = 'Padre'

    name = fields.Char(string='Nombre', required=True)
    login = fields.Char(string='Usuario (login)', required=True)
    password = fields.Char(string='Contraseña', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', required=True, ondelete='cascade')
    student_ids = fields.One2many('school.student', 'parent_id', string='Hijos')

    @api.model_create_multi
    def create(self, vals_list):
        parents = super(SchoolParent, self).create(vals_list)
        for parent, vals in zip(parents, vals_list):
            if 'login' in vals and 'password' in vals:
                user_vals = {
                    'name': vals.get('name'),
                    'login': vals.get('login'),
                    'password': vals.get('password'),
                    'groups_id': [
                        (6, 0, [
                            self.env.ref('base.group_user').id,
                            self.env.ref('agenda.group_parent').id
                        ])
                    ]
                }
                user = self.env['res.users'].create(user_vals)
                parent.user_id = user.id
        return parents
