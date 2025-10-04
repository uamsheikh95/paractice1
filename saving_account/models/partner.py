from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_saving_customer = fields.Boolean(string="Is Saving Customer", default=False)
    saving_branch_id = fields.Many2one('saving_account.branch', string="Branch")
    type = fields.Selection(selection_add=[('saving_account', 'Saving Account')])
    saving_type_id = fields.Many2one('saving_account.saving_type', string='Saving Type')
    saving_account_no = fields.Char(string="Acc#", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            is_saving_customer = vals.get('is_saving_customer')
            parent_id = vals.get('parent_id')
            if is_saving_customer == True and parent_id:
                vals['saving_account_no'] = self.env['ir.sequence'].next_by_code('saving.account.seq') or '/'
            else:
                vals['saving_account_no'] = ''
        return super(ResPartner, self).create(vals_list)