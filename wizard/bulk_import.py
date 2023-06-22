import base64
import io
from datetime import datetime
import pandas as pd
from odoo import models, fields


class MiWizard(models.TransientModel):
    _name = 'bulk.import'
    _description = 'Bulk Import'

    file_attached = fields.Binary(string='Load file')
    file_template = fields.Binary(string='Template')
    template_name = fields.Char(string='Template Name')

    # Define the method which will be executed when click over "Accept"
    def upload_file(self):
        decoded_data = base64.b64decode(self.file_attached)
        df = pd.read_csv(io.BytesIO(decoded_data), delimiter=";")
        my_data = df.to_dict("records")

        UniversityElection = self.env['university.election']
        ResPartner = self.env['res.partner']

        # Creating Election
        data = my_data[0]

        description = data['description_election']
        start_date = datetime.strptime(data['start_date'], '%d/%m/%y')
        end_date = datetime.strptime(data['end_date'], '%d/%m/%y')

        election = UniversityElection.create({
            'name': description,
            'start_date': start_date,
            'end_date': end_date,
        })
        print("Created UniversityElection record with ID:", election.id)

        # Creating Candidates
        for data in my_data:

            name = data['candidate_name']
            nro_identificacion = data['candidate_nro_identificacion']
            description = data['candidate_description']

            partner = ResPartner.create({
                'name': name,
                'nro_identificacion': nro_identificacion,
                'description': description,
                'es_candidato': True,
            })

            # Creating Relationship
            # The number 4 represents the command to add a new record to a many-to-many relationship field in Odoo
            election.candidates = [(4, partner.id)]

            print("Created ResPartner record with ID:", partner.id)

        return {'type': 'ir.actions.act_window_close'}

    def download_file(self):
        return {
            "type": "ir.actions.act_url",
            "url": "https://drive.google.com/file/d/1DhtPFBxRigIsM_baps8bIMFTv7u9EbqQ/view?usp=drive_link",
            "target": "new",
        }
