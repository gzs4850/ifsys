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


# class OracledbHelper:
#     '''
#         tns的取值tnsnames.ora对应的配置项的值，如：
#         tns = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=10.16.18.23)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=MYDB)))'
#         '''
#
#     # def __init__(self, uname, upwd, tns):
#     def __init__(self):
#         self._uname = ''
#         self._upwd = ''
#         self._tns = ''
#         self._conn = None
#         self._ReConnect()
#
#     def _ReConnect(self):
#         if not self._conn:
#             self._conn = cx_Oracle.connect(self._uname, self._upwd, self._tns)
#         else:
#             pass
#
#     def __del__(self):
#         if self._conn:
#             self._conn.close()
#             self._conn = None
#
#     def _NewCursor(self):
#         cur = self._conn.cursor()
#         if cur:
#             return cur
#         else:
#             print "#Error# Get New Cursor Failed."
#             return None
#
#     def _DelCursor(self, cur):
#         if cur:
#             cur.close()
#
#     # 检查是否允许执行的sql语句
#     def _PermitedUpdateSql(self, sql):
#         rt = True
#         lrsql = sql.lower()
#         sql_elems = [lrsql.strip().split()]
#
#         # update和delete最少有四个单词项
#         if len(sql_elems) < 4:
#             rt = False
#         # 更新删除语句，判断首单词，不带where语句的sql不予执行
#         elif sql_elems[0] in ['update', 'delete']:
#             if 'where' not in sql_elems:
#                 rt = False
#
#         return rt
#
#     # 导出结果为文件
#     def Export(self, sql, file_name, colfg='||'):
#         rt = self.Query(sql)
#         if rt:
#             with open(file_name, 'a') as fd:
#                 for row in rt:
#                     ln_info = ''
#                     for col in row:
#                         ln_info += str(col) + colfg
#                     ln_info += '\n'
#                     fd.write(ln_info)
#
#     # 查询
#     def Query(self, sql, nStart=0, nNum=- 1):
#         rt = []
#
#         # 获取cursor
#         cur = self._NewCursor()
#         if not cur:
#             return rt
#
#         # 查询到列表
#         cur.execute(sql)
#         if (nStart == 0) and (nNum == 1):
#             rt.append(cur.fetchone())
#         else:
#             rs = cur.fetchall()
#             if nNum == - 1:
#                 rt.extend(rs[nStart:])
#             else:
#                 rt.extend(rs[nStart:nStart + nNum])
#
#         # 释放cursor
#         self._DelCursor(cur)
#
#         return rt
#
#     # 更新
#     def Exec(self, sql):
#         # 获取cursor
#         rt = None
#         cur = self._NewCursor()
#         if not cur:
#             return rt
#
#         # 判断sql是否允许其执行
#         if not self._PermitedUpdateSql(sql):
#             return rt
#
#         # 执行语句
#         rt = cur.execute(sql)
#
#         # 释放cursor
#         self._DelCursor(cur)
#
#         return rt
#
# # 类使用示例
#
# tns = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=10.16.17.46)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=MYDB)))'
# ora = OracledbHelper ('nicker', '123456', tns)
#
# # 导出结果为文件
# rs = ora .Export("SELECT * FROM org", '1.txt')
#
# # 查询结果到列表
# rs = ora.Query("SELECT * FROM org")
# print rs
#
# # 更新数据
# ora.Exec("update org set org_name='NewNameForUpdate' where org_id=123456;")