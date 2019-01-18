# -*- coding: utf-8 -*-
import datetime
import time
# from datetime import datetime,timedelta
from core.db_config import UserDBConfig
from sql_db_client import MsDBClient,AzureDBClient
from properties import user_db_config

# user_db_config = UserDBConfig()
# db_client = MsDBClient(host=user_db_config.host,
#                        user=user_db_config.user,
#                        pwd=user_db_config.pwd,
#                        db=user_db_config.db_name)
db_config= user_db_config()
db_client = AzureDBClient(host=db_config["host"],
                       user=db_config["user"],
                       pwd=db_config["pwd"],
                       db=db_config["db"])
def load_class_student_users(class_id):
    datas = []

    datas = db_client.ExecQuery(
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

    datas = db_client.ExecQuery(
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
    datas = db_client.ExecQuery(
        "SELECT [Identity] FROM[dbo].[Users]"
        " WHERE Id =" + str(user_id))

    Identity = datas[0][0]

    return Identity

def get_user(user_id):
    user =None

    datas = db_client.ExecQuery(
        "SELECT * FROM[dbo].[Users]"
        " WHERE Id =" + str(user_id))
    if len(datas)>0:
        user=datas[0]

    return user

# #test
# # load_class_student_users(7157)
# load_class_subject_teacher(7157)