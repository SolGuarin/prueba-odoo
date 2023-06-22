# -*- coding: utf-8 -*-
from odoo import fields, models


class UniversityVotesCandidate(models.Model):
    _name = 'university.votes.candidate'

    name = fields.Char(string="Name")
    candidate_id = fields.Many2one(comodel_name="res.partner", string="Candidate")
    candidate_image = fields.Binary(related="candidate_id.image_1920", string="Image", readonly=True)
    election_id = fields.Many2one(comodel_name="university.election", string="Election")
    votes_qty = fields.Integer(string="Votes", default=0)


