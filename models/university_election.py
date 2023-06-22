from odoo import fields, models
import pytz


class UniversityElection(models.Model):
    _name = 'university.election'

    name = fields.Char(string="Description")
    start_date = fields.Datetime(string="Start date")
    end_date = fields.Datetime(string="End date")
    candidates = fields.Many2many(comodel_name="res.partner", string='Candidates')
    votes_ids = fields.One2many('university.votes.candidate', 'election_id', string='Votes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progres', 'In progres'),
        ('closed', 'Closed')], string='State', default='draft')

    def button_multi_start(self):
        for election in self:
            tz = pytz.timezone(
                self.env.context.get('tz') or self.env.user.tz or 'UTC')
            now = tz.localize(
                fields.Datetime.from_string(fields.Date.context_today(self)))
            start_date = election.start_date.replace(tzinfo=tz)
            end_date = election.end_date.replace(tzinfo=tz)
            if (election.state == 'draft') and (start_date <= now) and (now <= end_date):
                election.button_start()

    def button_start(self):
        self.state = 'in_progres'

    def button_close(self):
        self.state = 'closed'
