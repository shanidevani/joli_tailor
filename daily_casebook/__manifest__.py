# -*- encoding: UTF-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015-Today Laxicon Solution.
#    (<http://laxicon.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
{
    "name": "Daily CaseBook",
    "summary": "Sales",
    'description': """
        Safa Rental Management
    """,
    'author': "Laxicon Solution",
    'website': "www.laxicon.in",
    "version": "16.0.1.0.0",
    "category": "Rent",
    "license": "LGPL-3",
    "depends": ['base','hr_expense'],
    "data": [
        'security/ir.model.access.csv',
        'views/daily_casebook_view.xml',
    ],
    'sequence': 1,
    'installable': True,
    'auto_install': False,
    'application': True,
}
