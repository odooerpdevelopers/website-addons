{
    "name": "Widget Form",
    "version": "18.0.0.1.3",
    "summary": "JS Widgets, Forms for Odoo Website",
    "category": "Website",
    "author": "OdooErpCloud.com",
    "website": "https://campuscleverit.es",
    "license": "AGPL-3",
    "depends": ["base", "portal", "web", "website"],
    "data": [
        "views/templates.xml",
        "views/website_menus.xml",
    ],
    "installable": True,
    "assets": {
        "web.assets_frontend": [
            "website_form/static/src/js/*.js",
            "website_form/static/src/scss/*",
        ],
    },
}
