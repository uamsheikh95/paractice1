from odoo import models, fields, api

class Transaction(models.Model):
    _name = "saving_account.transaction"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Saving Account Transaction"
    # _rec_name = 'trancation_no'

    name = fields.Char(default='/', string="Transaction#", tracking=True)
    date = fields.Date(string="Date", default=fields.Date.today())
    
    transaction_type = fields.Selection(
        [('deposit', 'Deposit'), 
         ('withdrawal', 'withdrawal'),
         ('account_to_account', 'Account to Account')],
        string='Transaction Type',
        required=True,
        default='deposit'
    )

    account_id = fields.Many2one('res.partner', string="Account", domain=[('type', '=', 'saving_account')], required=True)
    destination_account_id = fields.Many2one('res.partner', string="Destination Account", domain=[('is_saving_customer','=',True), ('saving_type_id','=',True)])
    journal_id = fields.Many2one('account.journal', string="Journal", domain=[('type','in',['cash', 'bank'])], required=True, tracking=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency", related="company_id.currency_id")
    amount = fields.Monetary(string="Amount")
    state = fields.Selection(
        [('draft', 'Draft'), 
         ('posted', 'Posted'),
         ('cancel', 'Cancel')],
        string='Status',
        required=True,
        default='draft',
        tracking=True
    )
    move_id = fields.Many2one('account.move', string="Journal Entry")

    # Prepare functions
    def _prepare_move_values(self):
        for r in self:
            move_values = {
                'journal_id': r.journal_id.id,
                'company_id': r.company_id.id,
                'date': r.date,
                'ref': r.transaction_type + ' ' + r.name,
                'currency_id': r.currency_id.id,
                'name': '/',
                'move_type': 'entry'
            }
            return move_values
        
    def _prepare_move_line_values(self):
        for record in self:
            vals = []
            transaction_type = record.transaction_type
            amount = record.amount
            account_id = record.account_id
            date = record.date

            if transaction_type == 'deposit':
                move_line_one = {
                    'name': 'Deposit',
                    'debit': amount,
                    'credit': 0,
                    'partner_id': account_id.id,
                    'account_id': record.journal_id.default_account_id.id,
                    'date_maturity': date,
                    'date': date,
                    'currency_id': record.currency_id.id,
                }
                vals.append((0, 0, move_line_one))

                move_line_two = {
                    'name': 'Deposit',
                    'debit': 0,
                    'credit': amount,
                    'partner_id': account_id.id,
                    'account_id': account_id.saving_type_id.account_id.id,
                    'date_maturity': date,
                    'date': date,
                    'currency_id': record.currency_id.id,
                }
                vals.append((0, 0, move_line_two))

            return vals

    def action_post(self):
        for record in self:
            record.name = self.env['ir.sequence'].next_by_code('saving.transaction.seq') or '/'
            move_vals = record._prepare_move_values()
            move_vals['line_ids'] = record._prepare_move_line_values()
            move_id = self.env['account.move'].sudo().create(move_vals)
            move_id.action_post()
            record.move_id = move_id.id

            record.state = 'posted'

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

            if record.move_id:
                record.move_id.button_cancel()