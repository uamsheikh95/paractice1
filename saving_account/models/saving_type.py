from odoo import models, fields

class TestModel(models.Model):
    _name = "saving_account.saving_type"

    name = fields.Char(required=True, string="Name")