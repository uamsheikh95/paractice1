from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_saving_customer = fields.Boolean(string="Is Saving Customer", default=False)
    saving_branch_id = fields.Many2one('saving_account.branch', string="Branch")