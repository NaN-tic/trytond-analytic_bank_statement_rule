# This file is part analytic_bank_statement_rule module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import If, Eval

__all__ = ['StatementLineRuleLineAnalytic', 'StatementLineRuleLine',
    'StatementLine']


class StatementLineRuleLineAnalytic(ModelSQL, ModelView):
    'Statement Line Rule Line Analytic'
    __name__ = 'account.bank.statement.line.rule.line.analytic'
    rule_line = fields.Many2One('account.bank.statement.line.rule.line',
        'Rule Line', required=True)
    analytic_account = fields.Many2One('analytic_account.account',
        'Analytic Account', required=True, domain=[
            ('company', If(Eval('context', {}).contains('company'), '=', '!='),
            Eval('context', {}).get('company', -1)),
        ])


class StatementLineRuleLine:
    __metaclass__ = PoolMeta
    __name__ = 'account.bank.statement.line.rule.line'
    # analytic_accounts = fields.Many2One('analytic_account.account.selection',
    #     'Analytic Accounts')
    analytic_accounts = fields.One2Many(
        'account.bank.statement.line.rule.line.analytic', 'rule_line',
        'Analytic Accounts')


class StatementLine:
    __metaclass__ = PoolMeta
    __name__ = 'account.bank.statement.line'

    def get_move_line_from_rline(self, rline, amount):
        Selection = Pool().get('analytic_account.account.selection')

        mline = super(StatementLine, self).get_move_line_from_rline(rline, amount)

        analytic_accounts = []
        for aa in rline.analytic_accounts:
            analytic_accounts.append(aa.analytic_account)
        if analytic_accounts:
            selection = Selection(accounts=analytic_accounts)
            mline.analytic_accounts = selection

        return mline
