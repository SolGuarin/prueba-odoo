# -*- coding: utf-8 -*-
from odoo import fields, models


class EjEstudiante(models.Model):
    _name = 'ej.estudiante'
    nro_identificacion = fields.Integer(string='nro_identificacion')
    nombre = fields.Char(string='nombre', required=True)
    carrera = fields.Char(string='carrera')
    sede = fields.Boolean(string='sede', default=True)
