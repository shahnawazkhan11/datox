from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins (for dev)

@app.route("/api/hello")
def hello():
    return {"message": "Hello from Flask!"}
