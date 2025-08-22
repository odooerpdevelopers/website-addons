{
    "name": "OWL Welcome Component - Ejercicio 0",
    "version": "18.0.1.0.0",
    "summary": """
    EJERCICIO 1 OWL - Campus Cleverit
    Tu primer componente OWL
    ========================
    Componente de bienvenida OWL.
    """,
    "author": "Campus Cleverit",
    "website": "https://campuscleverit.es",
    "category": "Tools",
    "depends": ["base", "web", "contacts"],
    "data": ["views/menu_action.xml"],
    "assets": {
        "web.assets_backend": [
            "owl_welcome/static/src/components/welcome_component.js",
            "owl_welcome/static/src/components/welcome_component.xml"
        ],
    },
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
