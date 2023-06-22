# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nro_identificacion = fields.Char(string='nro_identificacion')
    carrera = fields.Many2one(comodel_name="university.career", string='Carrera')
    sede = fields.Char(string='Sede')  # I didn't delete this because it was raising and exception
    es_estudiante = fields.Boolean(string='Estudiante')
    campus_id = fields.Many2one(comodel_name="university.campus", string="Campus")

    es_candidato = fields.Boolean(string="Candidato")
    description = fields.Char(string="Descripcion")
    _sql_constraints = [
        ('nro_identificacion_unique',
         'UNIQUE(nro_identificacion)',
         "El número de identificación debe ser único"),
    ]


