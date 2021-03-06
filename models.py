#encoding:utf-8
import datetime

from exts import db

class Result(db.Model):
    __tablename__ = 'auto_result'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    mockid = db.Column(db.Integer)
    name = db.Column(db.String(150))
    testresult = db.Column(db.Boolean)
    reqmethod = db.Column(db.String(10))
    rspcode = db.Column(db.String(10))
    reqpath = db.Column(db.String(100))
    reqhead = db.Column(db.Text)
    reqbody = db.Column(db.Text)
    rsphead = db.Column(db.Text)
    rspbody = db.Column(db.Text)
    diff = db.Column(db.Text)
    ts = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

class avlDept(db.Model):
    __tablename__ = 'avl_dept'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_code = db.Column(db.String(64),nullable=False)
    dept_name = db.Column(db.String(32),nullable=False)
    status = db.Column(db.String(10))
    ts = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    useage = db.Column(db.String(50),nullable=False)
