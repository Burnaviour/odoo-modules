{
    "name": "Sales All In One Report Generator",
    "version": "16.0.1",
    "summary": "Dynamic Sales Report Maker",
    "description": "Dynamic Sales Report Maker",
    "category": "Customizations",
    "author": "KKNetworks",
    "maintainer": "KKNetworks",
    "company": "KKNetworks",
    "website": "https://kknetworks.com.pk",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_report.xml",
        "report/sale_order_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sale_report_generator/static/src/**/*",
            "sale_report_generator/static/src/xml/**/*",
            "sale_report_generator/static/src/js/sale_report.js",
            "sale_report_generator/static/src/css/sale_report.css",
        ],
        "web.assets_qweb": [
            "sale_report_generator/static/src/xml/**/*",
            "sale_report_generator/static/src/xml/sale_report_view.xml",
        ],
    },
    "images": ["static/description/banner.png"],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "auto_install": False,
}
