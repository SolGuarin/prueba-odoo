from odoo import fields, models


class UniversityCareer(models.Model):
    _name = 'university.career'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    area = fields.Char(string="Area")
