# encoding:utf-8

from flask import Flask, jsonify, render_template

import config
from models import Result, db

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def hello_world():
    return render_template("login.html")


@app.route('/caselist')
def caselist():
    return render_template("testset.html")


@app.route('/getResult')
def getResult():
    result = Result.query.all()
    resultlist = []
    for res in result:
        data = {
            'name': res.name,
            'url': res.reqpath,
            'reqhead': res.reqhead,
            'reqbody': res.reqbody,
            'rspcode': res.rspcode,
            'rsphead': res.rsphead,
            'rspbody': res.rspbody,
            'time': res.ts
        }
        resultlist.append(data)

    resp = jsonify(resultlist)
    return resp


@app.route('/getResult/<id>')
def getResultByID(id):
    result = Result.query.filter(Result.id == id).first()
    data = {
        'name': result.name,
        'testresult:': result.testresult,
        'url': result.reqpath,
        'reqhead': result.reqhead,
        'reqbody': result.reqbody,
        'rspcode': result.rspcode,
        'rsphead': result.rsphead,
        'rspbody': result.rspbody,
        'time': result.ts
    }
    resp = jsonify(data)
    return resp


# @app.route('/addResult')
# def addResult1():
#     addResult('2', 'testname', 'True', 200, 'http://127.0.0.1/getResult',
#               '{"Accept":"text/html,application/xhtml+xml,application/xml";"q"="0.9,image/webp,image/apng,*/*";"q"="0.8"}',
#               '{"sign":"7783e85c2ed70224593599fbefdc168a"}',
#               '{"Content-Type":"application/json"}', '{"count":0,"notifications":0,"messages":0}')
#     resp = jsonify({'result': 'success'})
#     return resp


def addResult(mockid, name, testresult, rspcode, reqpath, reqhead, reqbody, rsphead, rspbody):
    result = Result()
    result.mockid = mockid
    result.name = name
    result.testresult = testresult
    result.rspcode = rspcode
    result.reqpath = reqpath
    result.reqhead = reqhead
    result.reqbody = reqbody
    result.rsphead = rsphead
    result.rspbody = rspbody
    db.session.add(result)
    db.session.commit()

# if __name__ == '__main__':
#     app.run()
