from odoo import models, fields

class SavingType(models.Model):
    _name = "saving_account.saving_type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Saving Type"

    name = fields.Char(required=True, string="Name", tracking=True)
    account_id = fields.Many2one('account.account', domain=[('account_type', '=', 'liability_payable')], tracking=True)