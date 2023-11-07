import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FuelMonthlyReportWizard(models.TransientModel):
    _name = "fuel.monthly.report.wizard"
    _description = "Fuel Monthly Report Wizard"
    year = fields.Selection(
        [
            (str(year), str(year))
            for year in range(2000, datetime.datetime.now().year + 11)
        ],
        string="Year",
        required=True,
        default=str(datetime.datetime.now().year),
        help="Select the year for which you want to generate the report",
    )
    month = fields.Selection(
        [
            ("01", "January"),
            ("02", "February"),
            ("03", "March"),
            ("04", "April"),
            ("05", "May"),
            ("06", "June"),
            ("07", "July"),
            ("08", "August"),
            ("09", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ],
        string="Month",
        default="01",
        required=True,
    )

    @api.constrains("year")
    def _check_year_range(self):
        current_year = datetime.datetime.now().year
        if int(self.year) < 2000 or int(self.year) > current_year + 11:
            raise ValidationError(
                _("Year must be between 2000 and %s", current_year + 11)
            )

    def generate_report(self):
        pass
