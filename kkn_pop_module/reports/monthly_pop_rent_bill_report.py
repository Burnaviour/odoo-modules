from odoo import api, fields, models, _
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class PopRentBillReportTemplate(models.AbstractModel):
    _name = 'report.kkn_pop_module.monthly_pop_bill_report_temp'
    _description = 'Monthly Pop Rent Bill Report Template'

    @api.model
    def _get_report_values(self, docids, data=None):
        data_temp = []
        docs = self.env['pop.rent.bill.report'].browse(docids[0])
        company_id = self.env.user.company_id
        month = docs.month
        year = docs.year
        datem = date(int(year), int(month), 1)
        this_first = datem.replace(day=1)
        this_last = this_first + relativedelta(months=1, days=-1)
        print(this_first, this_last)
        temp = []
        # pop_bill = self.env['add.pop.rent.bill'].search(
        #     [('billing_date', '>=', this_first), ('billing_date', '<=', this_last),
        #      ('move_id.state', '=', 'posted'), ('move_id.invoice_payment_state', '=', 'paid')])
        sql = "select sl.unique_id, sl.name, rp.name, rp.mobile, COALESCE( am.amount_total, 0 ), ap.payment_terms " \
              "from add_pop_rent_bill as ad " \
              "inner join account_move as am " \
              "on am.id = ad.move_id " \
              "inner join add_pop as ap " \
              "on ap.id = ad.name " \
              "inner join stock_location as sl " \
              "on sl.id = ap.created_location " \
              "inner join res_partner as rp " \
              "on rp.id = ap.partner_id " \
              "where am.state = 'posted' and am.invoice_payment_state = 'paid' " \
              "and ad.billing_date >= '%s' and ad.billing_date <= '%s' " \
              "order by  am.amount_total asc" % (str(this_first), str(this_last))
        self.env.cr.execute(sql)
        pop_bill = self.env.cr.fetchall()
        for bill in pop_bill:
            vals = {
                'id': bill[0],
                'name': bill[1],
                'poc': bill[2],
                'mobile': bill[3],
                'term': bill[5],
                'bill_amount': bill[4],
            }
            temp.append(vals)
        temp2 = temp
        data_temp.append(
            [temp2])
        return {
            'doc_ids': self.ids,
            'doc_model': 'pop.rent.bill.report',
            'dat': data_temp,
            'docs': docs,
            'company_id': company_id,
            'data': data,
        }
