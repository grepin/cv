from flask import Flask

app = Flask(__name__)

app.execute_before_request = []


@app.before_request
def _execute_before_request():
    for func in app.execute_before_request:
        func()
