# -*- coding: utf-8  -*-
from from_shareresource_repository import *
from user_repository import *
from shareresource_repository import *
from entity import *
from core.log import *
from core.time_util import time2string

# tz_utc_8 =datetime.timezone(datetime.timedelta(hours=8))
SharedLevel={"SELFANDGROUPOWNER": 0,"GROUP":1, "PRIVATE": 2}
ResourceType={ "UnKnown":0, "Folder":1, "File":2}

def sqlTextResult2String(text):
    return text.encode("utf-8")

class DataHandler:
    """"
                数据处理器
                """
    def __init__(self,begin_time=datetime.datetime.now(),end_time=datetime.datetime.now()):
        self.begin_time=begin_time
        self.end_time=end_time
        self.class_ids=[]
        # self.ori_share_resource_repository=None
        self.data_tag=self.init_data_tag()

        self.count = 0
        self.share_resources_count = 0
        self.user_resource_count = 0
        self.ex_record_count =0


    def work(self):
        start_time = time.time()
        log_info('开始处理数据，%s' % self.data_tag)
        try:
            # 获取班级
            self.init_class_data()
            if len(self.class_ids) <= 0:
                log_info('本次任务需要处理的班级数据为空，处理结束，%s' % self.data_tag)
                return
            log_info('本次任务需要处理的班级数据有%d个，%s' % (len(self.class_ids), self.data_tag))
            for class_id in self.class_ids:
                log_info('处理班级-%d数据，%s' % (class_id, self.data_tag))
                try:
                    class_data_handler = ClassDataHandler(class_id, self.begin_time, self.end_time)
                    class_data_handler.work()
                    #汇总数据
                    self.count +=class_data_handler.count
                    self.share_resources_count+=class_data_handler.share_resources_count
                    self.ex_record_count+=(class_data_handler.ex_records.size())
                    self.user_resource_count+=class_data_handler.user_resource_count
                except Exception, ex:
                    log_ex('处理班级-%d数据发生异常：%s,%s' % (class_id,ex.message, self.data_tag))
                log_info('班级-%d数据处理结束，%s' % (class_id, self.data_tag))

            #输出报表
            log_info('本次任务数据处理完毕，需处理共享资源数目：%d,实际入库共享资源数目：%d'
                     ',存在异常共享资源数目：%d,入库用户资源数目：%d，%s' %
                     (self.count, self.share_resources_count, self.ex_record_count, self.user_resource_count,
                      self.data_tag))
        except Exception,ex:
            log_ex('发生异常：%s,%s' % (ex.message, self.data_tag))

        log_cost(start_time)
        log_info('本次处理结束，%s' % self.data_tag)

    def init_data_tag(self):
        return '目标数据:begintime[%s] endtime[%s]' % (time2string(self.begin_time) ,time2string(self.end_time))

    def init_class_data(self):
        class_id_datas =load_class_ids(self.begin_time, self.end_time)
        if not class_id_datas or len(class_id_datas) <= 0:
            return
        for class_id_data in class_id_datas:
            self.class_ids.append(class_id_data[0])

class ClassDataHandler:
    """"
            班级数据处理器
            """
    def __init__(self,class_id=0,begin_time=datetime.datetime.now(),end_time=datetime.datetime.now()):
        self.class_id=class_id
        self.begin_time=begin_time
        self.end_time=end_time
        self.page_index = 1
        self.page_size = 10
        self.count=0
        self.page_count=0
        self.student_users=[]
        self.subject_teacher_users={}

        self.data_tag = self.init_data_tag()
        self.share_resources_count=0
        self.user_resource_count=0
        self.ex_records=ExRecordList()
        self.share_resource_repository= ShareResourceRepository()
        self.user_resource_repository = UserResourceRepository()
        self.ex_record_repository=ExRecordRepository()

    def get_data(self, page_index, page_size):
        """"
        初始化学生用户数据
        :param  img_car:  图片实体
        :return:图片集合
        """
    def init(self):
        """
      初始化
          """
        log_info('开始初始化数据，%s' % self.data_tag)
        try:
            # 初始化学生用户
            self.init_class_student_users()
            # 初始化老师用户
            self.init_class_teacher_users()
            # 初始化分页策略
            self.init_page_strategy()

        except Exception, e:
            log_ex('初始化发生异常：%s,%s' % (e.message,self.data_tag))
            return False
        log_info('初始化数据完成，%s' % (self.data_tag))
        return True

    def init_data_tag(self):
        return '目标数据:classid-%d begintime-%s endtime-%s' % (self.class_id\
            ,time2string(self.begin_time),time2string(self.end_time))

    def init_class_student_users(self):
        """
            初始化学生用户数据
                """
        user_datas = load_class_student_users(self.class_id)
        if (not user_datas or len(user_datas) <= 0):
            return
        for user_data in user_datas:
            self.student_users.append(user_data[0])

    def init_class_teacher_users(self):
        """
                    初始化教师用户数据
                        """
        subject_teacher_datas = load_class_subject_teacher(self.class_id)
        if (not subject_teacher_datas or len(subject_teacher_datas) <= 0):
            return
        for subject_teacher_data in subject_teacher_datas:
            self.subject_teacher_users[sqlTextResult2String(subject_teacher_data[0])] = subject_teacher_data[1]


    def init_page_strategy(self):
        """
                  初始化分页策略
                      """
        self.count = get_share_resource_count(self.class_id, self.begin_time, self.end_time)
        if self.count <= 0:
            return

        # 获取分页
        self.page_count = self.count / self.page_size;
        if (self.count % self.page_size) != 0:
            self.page_count = self.page_count + 1

    def work(self):
        start_time = time.time()
        log_info('开始处理班级数据，%s' % (self.data_tag))
        #初始化
        if not self.init():
            return

        #是否有数据需要处理
        if len(self.student_users) <= 0 and len(self.subject_teacher_users) <= 0:
            log_info('该班级已被删除或已无用户，处理结束，%s' % (self.data_tag))
            return
        if self.count<=0 or self.page_count<=0:
            log_info('该班级下无数据，处理结束，%s' % (self.data_tag))
            return
        log_info('该班级下有%d条（%d页）数据需要处理，%s' % (self.count,self.page_count, self.data_tag))

        #遍历处理
        for index in range(self.page_count):
            self.page_index = index + 1
            log_info('开始处理第%d页数据，%s' % (self.page_index, self.data_tag))
            try:
                # 获取数据
                datas = load_share_resources(self.class_id, self.begin_time, self.end_time, self.page_index,
                                             self.page_size)
                self.deal_share_resource_datas(datas)
            except Exception,ex:
                log_ex('处理第%d页数据发生异常：%s,%s' % (self.page_index, ex.message, self.data_tag))
                continue
            log_info('第%d页数据处理完毕，%s' % (self.page_index, self.data_tag))

        self.dispose()
        log_info('班级数据处理完毕，需处理共享资源数目：%d,实际入库共享资源数目：%d'
                 ',存在异常共享资源数目：%d,入库用户资源数目：%d，%s' %
                 (self.count,self.share_resources_count,self.ex_records.size(),self.user_resource_count,self.data_tag))
        log_cost(start_time)

    def dispose(self):
        if self.ex_records.size()>0:
            self.ex_record_repository.batchAdd(self.ex_records.datas.values())

    def ori_share_resource_data2share_resource_entity(self,data):
        """"
                         提取分享资源实体
                         :param  data:  分享资源数据
                         :return:分享资源实体
                         """
        share_resource=None

        if data==None:
            return share_resource
        try:
            # 策略
            strategy_result = self.create_user_id_shared_level_strategy(data)
            if not strategy_result:
                return
            sharedLevel = strategy_result["sharedLevel"]
            create_user_id = strategy_result["create_user_id"]
            gid=str(data[2]).lower()
            parentId=''
            if data[17]:
                parentId=str(data[17]).lower()
            name= sqlTextResult2String(data[3])
            file_guid=''
            if data[5]:
                file_guid = str(data[5]).lower()
            file_size=0
            if data[16]:
                file_size=data[16]
            share_resource = ShareResource(
                gid=gid,
                parentId=parentId,
                sharedLevel=sharedLevel,
                available=data[8],
                resourceType=data[11],
                name=name,
                fileGuid=file_guid,
                fileSize=file_size,
                classId=data[7],
                subjectCode=sqlTextResult2String(data[4]),
                createUserId=create_user_id,
                createTime=DateTime.timezone8(data[10]),
                updateTime=DateTime.timezone8(data[9]),
                syncTime=DateTime.timezone8(data[14]),
                isAllowAppendFile=data[13]
            )
        except Exception, e:
            log_ex('资源数据转换发生异常：%s,id:%d' % (e.message,data[1]))
            self.ex_records.add(data[1], '资源数据转换发生异常：%s' % (e.message))
            return None

        return share_resource

    def create_user_id_shared_level_strategy(self, data):
        """"
                                 共享资源的创建人和分享级别取值策略
                                 :param  data:  分享资源数据
                                 :return:策略
                                 """
        #科目不存在
        id=data[1]
        subject_code=sqlTextResult2String(data[4])
        user_id = data[6]
        if subject_code not in self.subject_teacher_users.keys():
            self.ex_records.add(id,'科目不存在;未处理')
            return False

        create_user_id=0
        cur_subject_teacher_user_id=self.subject_teacher_users[subject_code]
        sharedLevel = 0
        if data[11] == 1:  # 文件夹
            sharedLevel=1
            create_user_id=cur_subject_teacher_user_id
        else:  # 文件
            #先断定为学生
            if user_id in self.student_users:
                sharedLevel=0
                create_user_id=user_id
            elif user_id in self.subject_teacher_users.values():
                sharedLevel=1
                create_user_id=user_id
            else:
                self.ex_records.add(id, '用户已删除或离班;未知')
                user_data=get_user(user_id)
                if user_data==None:
                    self.ex_records.add(id, '用户不存在（物理删除）;未处理')
                    return False
                if user_data[11]==1:
                    sharedLevel=1
                    create_user_id=cur_subject_teacher_user_id
                elif user_data[11]==2:
                    sharedLevel = 0
                    create_user_id = user_id #todo:可能会带来问题
                else:
                    self.ex_records.add(id, '用户身份不合法;未处理')
                    return False
        if create_user_id!=user_id:
            self.ex_records.add(id,'创建人被替换;已处理')

        return {"sharedLevel":sharedLevel,"create_user_id":create_user_id}

    def share_users(self,share_resource=ShareResource()):
        users=[]

        if share_resource.sharedLevel==SharedLevel['SELFANDGROUPOWNER']:
            subject_code=share_resource.subjectCode
            teacher_user_id= self.subject_teacher_users[subject_code]
            users.append(teacher_user_id)
        elif share_resource.sharedLevel==SharedLevel['GROUP']:
            #科目老师
            subject_code=share_resource.subjectCode
            teacher_user_id= self.subject_teacher_users[subject_code]
            #学生
            users.append(teacher_user_id)
            for user_id in self.student_users:
                users.append(user_id)
        else:
            pass

        #剔除创建者自己
        if share_resource.createUserId in users:
            users.remove(share_resource.createUserId)

        return users


    def deal_share_resource_datas(self,datas):
        """"
               处理一簇共享资源数据
               :param  datas:  分享资源数据集合
               :return:
               """
        #提取实体
        share_resources =self. ori_share_resource_datas2share_resource_entities(datas)
        #处置实体
        self.share_resources_handler(share_resources)
    def ori_share_resource_datas2share_resource_entities(self,datas):
        """"
                      批量提取分享资源实体
                      :param  datas:  分享资源数据集合
                      :return:分享资源实体集合
                      """
        share_resources = []

        if datas == None or len(datas) <= 0:
            return

        for data in datas:
            share_resource = self.ori_share_resource_data2share_resource_entity(data)
            if not share_resource:
                continue
            share_resources.append(share_resource)

        #补充parentId，暂时方案
        # self.share_resources_parent_id_patch(share_resources)

        return share_resources

    def share_resources_parent_id_patch(self, share_resources):
        """"
                     处理共享资源
                     :param  share_resources:  共享资源集合
                     :return:
                     """
        try:
            ids = []
            for share_resource in share_resources:
                if share_resource.parentId:
                    ids.append(int(share_resource.parentId))
            if len(ids) <= 0:
                return

            guid_datas = get_share_resource_guid(ids)
            if guid_datas == None or len(guid_datas) <= 0:
                return
            for share_resource in share_resources:
                if share_resource.parentId:
                    parent_id = int(share_resource.parentId)
                    parent_id_data = [x for x in guid_datas if x[0] == parent_id]
                    if parent_id_data:
                        share_resource.parentId = str(parent_id_data[0][1])
                    else:
                        self.ex_records.add(parent_id, '该资源不存在， 其子孙资源parentId有误')
        except Exception,ex:
            raise Exception('补充parentId发生异常：%s' % ex.message)

    def share_resources_handler(self,share_resources):
        """"
                     处理共享资源
                     :param  share_resources:  共享资源集合
                     :return:
                     """
        if share_resources == None or len(share_resources) <= 0:
            return
        self.share_resources_count += len(share_resources)
        for share_resource in share_resources:
            user_resources= self.share_resources_dispatcher(share_resource)
            self.user_resource_count+=len(user_resources)
            # 资源入库
            self.commit_user_resources_to_db(user_resources)

        #资源入库
        self.commit_share_resources_to_db(share_resources)

    def share_resources_dispatcher(self,share_resource):
        """"
                             共享资源分发
                             :param  share_resource:  共享资源
                             :return:
                             """
        share_users = self.share_users(share_resource)
        share_user_resources = share_resource.share_to_users(share_users)
        share_user_resources.append(share_resource.author_resource())

        return share_user_resources

    def commit_share_resources_to_db(self,share_resources):
        self.share_resource_repository.batchAdd(share_resources)

    def commit_user_resources_to_db(self, user_resources):
        self.user_resource_repository.batchAdd(user_resources)

# #test
# datahandler=DataHandler()
# datahandler.work()




























