from odoo import models, fields

class Branch(models.Model):
    _name = "saving_account.branch"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Branch"

    name = fields.Char(required=True, string="Branch Name", tracking=True)