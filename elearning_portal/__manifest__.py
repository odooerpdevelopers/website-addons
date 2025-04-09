{
    "name": "My eLearning Portal Component",
    "author": "OdooErpCloud",
    "website": "https://campuscleverit.es",
    "version": "18.0.0.1.0",
    "summary": "Shows subscribed eLearning courses in the portal using OWL",
    "category": "Portal/eLearning",
    "depends": [
        "portal",
        "website_slides",  # Dependencia clave para elearning app
        "web",
    ],
    "data": [
        "views/portal_template.xml",  # El XML que hereda del portal
    ],
    "assets": {
        "web.assets_frontend": [  # Bundle para portal/website
            # Asegúrate que las rutas sean correctas
            "elearning_portal/static/src/components/subscribed_courses.js",
            "elearning_portal/static/src/components/subscribed_courses.xml",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
