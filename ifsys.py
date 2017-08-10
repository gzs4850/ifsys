#encoding:utf-8
from flask import Flask,jsonify,render_template,request
from models import Result
import config

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/demoapi')
def demoapi():
    # jsonResponse = dict(code='200',msg=u'查询成功')
    # response = jsonify(jsonResponse)
    # return response
    return render_template("testset.html")

@app.route('/caselist')
def caselist():
    return render_template("testset.html")

@app.route('/getResult')
def getResult():
    result = Result.query.all()
    resp = jsonify({'result':result})
    return resp

@app.route('/getResult/<int:id>')
def getResultByID():
    result = Result.query.filter(Result.mockid == 'id').frist()
    resp = jsonify({'result': result})
    return resp

def addResult():



if __name__ == '__main__':
    app.run()
