# -*- coding: utf-8 -*-
###############################################################################
#
#   account_check_deposit for Odoo
#   Copyright (C) 2012-2015 Akretion (http://www.akretion.com/)
#   @author: Benoît GUILLOT <benoit.guillot@akretion.com>
#   @author: Chafique DELLI <chafique.delli@akretion.com>
#   @author: Alexis de Lattre <alexis.delattre@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class AccountCheckDeposit(models.Model):
    _inherit = "account.check.deposit"

    @api.model
    def _prepare_counterpart_move_lines_vals(
            self, deposit, total_debit, total_amount_currency):
        res = super(AccountCheckDeposit, self).\
            _prepare_counterpart_move_lines_vals(deposit, total_debit,
                                                 total_amount_currency)
        # Check account exit
        journal = deposit.partner_bank_id.journal_id
        account_id = journal.default_debit_account_id.id or \
            journal.default_credit_account_id.id
        if not account_id:
            raise UserError(
                _("Missing counter part account on Bank"))
        res.update({'account_id': account_id})
        return res
