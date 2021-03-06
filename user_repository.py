# -*- coding: utf-8 -*-
# from datetime import datetime,timedelta
from cfg_mapper import UserDBConfig
from core.sql_pro import *


def db_client():
    return sql_sesson(UserDBConfig())

def load_class_student_users(class_id):
    datas = []

    datas = db_client().ExecQuery(
        "Select U.Id from ClassStudents C"
        " INNER JOIN Students S ON C.StudentId=S.Id"
        " INNER JOIN Users U ON S.UserId=U.Id"
        " INNER JOIN Classs L ON C.ClassId=L.Id "
        " INNER JOIN Departments D ON L.DeptId=D.Id"
        " where C.ClassId=" + str(class_id) +
        " AND C.Available=1 AND S.Available=1 AND U.Available=1 AND D.Available=1")

    return datas

def load_class_subject_teacher(class_id):
    datas = []

    datas = db_client().ExecQuery(
        "SELECT S.Code, T.UserId"
        " FROM TeacherSubject TS"
        " INNER JOIN Teachers T ON TS.TeacherId=T.Id"
        " INNER JOIN Users U ON T.UserId=U.Id"
        " INNER JOIN [Subject] S ON TS.SubjectId=S.Id"
        " INNER JOIN Classs C ON TS.ClassId=C.Id"
		" INNER JOIN Departments D ON C.DeptId=D.Id"
        " WHERE TS.ClassId=" + str(class_id) +
        " AND T.Available=1"
        " AND U.Available=1"
        " AND D.Available=1")

    return datas

def get_user_identity(user_id):
    datas = db_client().ExecQuery(
        "SELECT Identity FROM[dbo].[Users]"
        " WHERE Id =" + str(user_id))

    Identity = datas[0][0]

    return Identity

def get_user(user_id):
    user =None

    datas = db_client().ExecQuery(
        "SELECT [Identity] FROM[dbo].[Users]"
        " WHERE Id =" + str(user_id))
    if len(datas)>0:
        user=datas[0]

    return user

def batch_get_user(ids=[]):
    datas = []

    in_query = build_in_query_sql(ids)
    datas = db_client().ExecQuery(
        "SELECT Id, [Identity] FROM [dbo].[Users]"
        " WHERE Id IN " + in_query)

    return datas

# #test
# # load_class_student_users(7157)
# load_class_subject_teacher(7157)