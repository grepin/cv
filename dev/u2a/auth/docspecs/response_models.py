RESPONSE_BASE = {
    "type": "object",
    "properties": {
        "code": {
            "type": "integer"
        },
        "description": {
            "type": "string",
        },
        "success": {
            "type": "boolean"
        },
        "data": {
            "type": "object"
        }
    },
    "required": [
        "code",
        "description",
        "success",
        "data"
    ]
}



