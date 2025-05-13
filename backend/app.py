from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return {"message": "Hello, World!"}, 200

if __name__ == '__main__':
    app.run(debug=True)