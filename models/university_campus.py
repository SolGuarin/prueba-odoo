from odoo import fields, models


class UniversityCampus(models.Model):
    _name = 'university.campus'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    city = fields.Char(string="City")
    country = fields.Char(string="Country")

