from flasgger import Swagger
from auth.extensions.flask import app

swagger_config = {
    "title": "API авторизации и управления ролями",
    "version": "1.0",
    "uiversion": 3,
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "endpoint": '/auth',
            "route": '/auth',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "securityDefinitions": {
        "Bearer": {
           "type": "apiKey",
           "name": "Authorization",
           "in": "header"
        }
    },
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/auth/openapi"
}
flassger = Swagger(app, config=swagger_config)
