#encoding:utf-8
from flask import Flask,jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/demoapi')
def demoapi():
    jsonResponse = dict(code='200',msg=u'查询成功')
    response = jsonify(jsonResponse)
    return response


if __name__ == '__main__':
    app.run(debug=True)
