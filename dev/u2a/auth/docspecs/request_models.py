USER4LOGIN = {
  "type": "object",
  "properties": {
    "login": {
      "type": "string",
    },
    "password": {
      "type": "string"
    }
  },
  "required": [
    "login",
    "password"
  ],
  "example": {
    "login": "adam",
    "password": "adam1man",
  }
}

USER4REGISTER = {
  "type": "object",
  "properties": {
    "login": {
      "type": "string",
    },
    "email": {
      "type": "string"
    },
    "password": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "lastname": {
      "type": "string"
    },
  },
  "required": [
    "login",
    "email",
    "password",
  ],
  "example": {
    "login": "adam",
    "email": "adam@mankind.com",
    "password": "adam1man",
    "name": "adam",
    "lastname": "firstman"
  }
}


USER4UPDATE = {
  "type": "object",
  "properties": {
    "login": {
      "type": "string",
    },
    "email": {
      "type": "string"
    },
    "password": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "lastname": {
      "type": "string"
    },
  },
  "required": [
  ],
  "example": {
    "lastname": "thefirstman"
  }
}


AUTH_HEADER = {
  "api_key": {
    "type": "apiKey",
    "name": "api_key",
    "in": "header"
  }
}


ROLE = {
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
    },
    "name": {
      "type": "string"
    }
  },
  "required": [
    "id",
    "name"
  ],
  "example": {
    "id": "3807bdc3-439b-4941-b456-58da0cb50e50",
    "name": "user",
  }
}

ROLE4CREATE = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    }
  },
  "required": [
    "name"
  ],
  "example": {
    "name": "passerby",
  }
}


USER2ROLE = {
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
    },
    "role_id": {
      "type": "string",
    },
  },
  "required": [
    "user_id",
    "role_id"
  ],
  "example": {
    "role_id": "9744d299-abc6-48a9-8862-0357cd4355a9",
    "user_id": "3807bdc3-439b-4941-b456-58da0cb50e50"
  }
}
