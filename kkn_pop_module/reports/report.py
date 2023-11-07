from odoo import models
import datetime


class WirelessReport(models.Model):
    _name = 'report.kkn_pop_module.all_pop_location_report'

    def _get_report_values(self, docids, data=None):
        docs_new = []

        domains = data['domains']
        wireless_host = self.env['stock.location'].search(domains)

        return {
            'doc_ids': self.ids,
            'docs_new': docs_new,
            'data': data,
            'date_now': (datetime.datetime.now()+datetime.timedelta(hours=5)).strftime("%d %b %Y %H:%M:%S"),
            'wireless_host': wireless_host,
            'print_new_person': self.env.user.name,
        }