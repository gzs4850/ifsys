#encoding:utf-8

from exts import db

class Result(db.Model):
    __tablename__ = 'auto_result'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    mockid = db.Column(db.Integer,nullable=False)
    name = db.Column(db.String(100))
    testresult = db.Column(db.Boolean)
    rspcode = db.Column(db.String(10))
    reqpath = db.Column(db.String(50))
    reqhead = db.Column(db.Text)
    reqbody = db.Column(db.Text)
    rsphead = db.Column(db.Text)
    rspbody = db.Column(db.Text)
    ts = db.Column(db.DateTime)