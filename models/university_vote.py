from odoo.exceptions import ValidationError
from odoo import fields, models, api, _
import pytz


class UniversityVote(models.Model):
    _name = 'university.vote'

    name = fields.Char(string="Name")
    elections_id = fields.Many2one(
        comodel_name="university.election", string='Election', required=True)
    student_id = fields.Many2one(
        comodel_name="res.partner", string='Student', required=True)
    candidate_id = fields.Many2one(
        comodel_name="res.partner", string='Candidate', required=True)

    @api.onchange('elections_id')
    def _onchange_elections_id(self):
        domain = []
        if self.elections_id:
            domain = [('es_candidato', '=', True), ('id', 'in', self.elections_id.candidates.ids)]
        return {'domain': {'candidate_id': domain}}

    @api.model
    def create(self, vals):
        # validamos los rangos de votación usando el timezone del usuario o
        # UTC en caso de no existir
        tz = pytz.timezone(
            self.env.context.get('tz') or self.env.user.tz or 'UTC')
        now = tz.localize(
            fields.Datetime.from_string(fields.Date.context_today(self)))
        if 'elections_id' in vals:
            election = self.env['university.election'].browse(vals['elections_id'])
            start_date = election.start_date.replace(tzinfo=tz)
            end_date = election.end_date.replace(tzinfo=tz)
            if start_date > now:
                raise ValidationError(_('The election has not started yet'))
            if end_date < now:
                raise ValidationError(_('The election has already ended'))

            # Validar que la elección no esté cerrada o en borrador
            if election.state != 'in_progres':
                raise ValidationError(_('The election is not in progress'))

        # Validamos que el estudiante no pueda votar 2 veces
        if 'student_id' in vals and 'elections_id' in vals:
            vote = self.search(
                [('student_id', '=', vals['student_id']),
                 ('elections_id', '=', vals['elections_id'])], limit=1)
            if vote:
                raise ValidationError(_('The student already voted'))
        res = super(UniversityVote, self).create(vals)
        # Creamos el objeto votes.candidates para el conteo de votos
        if 'candidate_id' in vals and 'elections_id' in vals:
            candidate = self.env['university.votes.candidate'].search(
                [('candidate_id', '=', vals['candidate_id']),
                 ('election_id', '=', vals['elections_id'])], limit=1)
            if candidate:
                candidate.update({'votes_qty': candidate.votes_qty + 1})
            else:
                self.env['university.votes.candidate'].create({
                    'candidate_id': vals['candidate_id'],
                    'election_id': vals['elections_id'],
                    'votes_qty': 1,
                    'name': f'{vals["candidate_id"]}-{vals["elections_id"]}'
                })
        return res
