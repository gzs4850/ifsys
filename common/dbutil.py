#encoding:utf-8

import MySQLdb

class MysqldbHelper:

    def getCon(self):
        try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='ifsys',port=3306,charset='utf8')
            return conn
        except MySQLdb.Error,e:
            print "Mysqldb Erroe:%s" %e

    #查询
    def select(self,sql):
        try:
            con = self.getCon()
            print con
            cur = con.cursor(MySQLdb.cursors.DictCursor)
            count = cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except MySQLdb.Error,e:
            print "Mysqldb Error:%s" %e
        finally:
            cur.close()
            con.close()

    #不带参数的更新方法
    def update(self,sql):
        try:
            print sql
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql)
            con.commit()
            return count
        except MySQLdb.Error,e:
            con.rollback()
            print "Mysqldb Error" %e
        finally:
            cur.close()
            con.close()

    #带参数的更新方法
    def updateByParam(self,sql,params):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql,params)
            con.commit()
            return count
        except MySQLdb.Error,e:
            con.rollback()
            print "Mysqldb Error:%s" %e
        finally:
            cur.close()
            con.close()

    #开发环境数据库配置
    def getDevCon(self):
        try:
            conn2 = MySQLdb.connect(host='192.168.10.240',user='test',passwd='1234',db='system',port=3306,charset='utf8')
            return conn2
        except MySQLdb.Error,e:
            print "Mysqldb Erroe:%s" %e

    #查询开发环境数据
    def selectdev(self,sql):
        try:
            con = self.getDevCon()
            print con
            cur = con.cursor(MySQLdb.cursors.DictCursor)
            count = cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except MySQLdb.Error,e:
            print "Mysqldb Error:%s" %e
        finally:
            cur.close()
            con.close()
