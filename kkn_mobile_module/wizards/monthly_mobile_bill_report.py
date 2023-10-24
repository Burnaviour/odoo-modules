import datetime
from datetime import datetime
from odoo import api, fields, models, _, tools
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class MobileBillReportWiz(models.TransientModel):
    _name = 'mobile.bill.report'
    _description = "Monthly Mobile Bill Report"

    def year_selection(self):
        year = 2022
        year_list = []
        while year != 3000:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    year = fields.Selection(year_selection, string="Year", default=str(datetime.now().year))

    month = fields.Selection(
        [('1', 'January'),
         ('2', 'February'),
         ('3', 'March'),
         ('4', 'April'),
         ('5', 'May'),
         ('6', 'June'),
         ('7', 'July'),
         ('8', 'August'),
         ('9', 'September'),
         ('10', 'October'),
         ('11', 'November'),
         ('12', 'December')], string='Month', default='%s' % str(datetime.now().month))


