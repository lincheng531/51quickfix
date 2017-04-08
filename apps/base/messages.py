#!/user/bin/env python
#encoding:utf-8
from datetime import datetime as dt

ERROR  = (0,'未知错误')
SUCCESS = (1,'操作成功')
SERVER_ERROR = (2,'服务器异常')
PARAMS_ERROR =(3,'参数错误')
LOGIN_REQUIRED = (4,'请先登录')
INVALID_REQUEST = (5,'非法请求')

# account
PWD_ERROR = (1001,'用户名和密码不匹配')
INVALID_USERNAME = (1002,'用户名错误，请填写正确的手机号码格式')
INVALID_PASSWORD = (1003,'密码长度必须在6~20个字符以内')
USERNAME_EXISTS  = (1004,'该用户名已存在')
INVALID_CAPTCHA = (1005,'验证码错误')
OLD_PWD_ERROR = (1006,'原密码错误')
NOT_ACTIVE = (1007,'帐号未激活')
UPDATE_PROFILE_FIELD_ERROR = (1008,'更新个人信息时，字段值{}错误')
# USER_DOES_NOT_EXISTS = (1009,'用户不存在')
USER_DOES_NOT_EXISTS = (1009,'请先去应用商店下载最新版本')
NOT_GENDER = (1012, '性别不得为空')
NOT_NAME = (1013, '名字不得为空')
NOT_VERIFY_CODE = (1014, '未验证验证码')

#type=0 接单通知
PUSH0 = u'{}:{}需要维修，赶快去接单吧！'

#type=1 接单通知
PUSH1 = u'{} {} 师傅接单啦!'

#type=2 填写工单
PUSH2 = u"{}填写了工单，快去确认吧！"

#type=6 取消叫修单
PUSH6 = u'{}维修单取消了!'

#type=3 确认修单
PUSH3 = u'{}确认了您的维修单，快去查看吧'

#type=7 维修失败
PUSH7 = u"{} {} 维修失败！"

#type=8 到店推送
PUSH8 = u'{} 师傅到店啦!'

#type=9 盘点
PUSH9 = dt.now().strftime('%Y年%m月盘点')

#type=10 盘点开始
PUSH10 = '{}盘点开始'

#type=11 维修即将暂停通知
PUSH11 = u'暂停即将结束!'

#type=12 维修暂停
PUSH12 = u'{}:{}维修暂停!'

#type=13 拒绝维修暂停
PUSH13 = u'{}:{}拒绝维修暂停!'

#type=14 餐厅收到报价单
#{'type':14, 'oid':叫修单id, 'cid':报价单id, 'name':维修工, 'product':设备名}
PUSH14 = u'您有新的报价单'

#type=15 维修员收到餐厅增加工单
#{'type':15, 'oid':叫修单id, 'cid':报价单id, 'name':维修工, 'product':设备名}
PUSH15 = u'您有新的工单'

#type=16 餐厅收到本次维修结束
#{'type':16, 'oid':维修单id, 'name':用户名, 'product':设备名称}
PUSH16 = u'本次维修结束'

#type=17 确认或者拒绝报价单,data较大请通过api获取
#{'type':17, 'oid':叫修单id, 'cid':报价单id，无则同意全部, 'sub_type':1为同意 -1为拒绝}
PUSH17 = ''

#type=18,迟到提醒，维修工，维修工主管
#{'type':18,'id':oid}
PUSH18 = u'{}{}({})正在等待你的维修，请在{}前到店。'

#type=19 到店签到提醒，餐厅，维修工，维修工主管
#{'type':19,'id':oid}
PUSH19 = u'{}到店请扫描二维码签到!'

#type=20餐厅，离店填写工单，维修工，维修工主管
#{'type':20,'id':oid}
PUSH20 = u'报修{}已过维修时效，请上传维修工单。'

#type=21餐厅，工单有误，重新修改
#{'type':21,'id':oid}
PUSH21 = u'工单有误:{}，请修改!'

#type=22餐厅，申请延时到店
#{'type':22,'id':叫修单id,'company':汉堡王or达美乐,'store_name':餐厅名称, 'store_no':餐厅编号,'msg':延时说明,'will_time':预计到店时间,'must_time':合约到店时间}
PUSH22 = u'{}师傅申请延时到店'

#type=23餐厅，申请延时到店
#{'type':23,'id':叫修单id,'company':汉堡王or达美乐,'store_name':餐厅名称, 'store_no':餐厅编号,'msg':延时说明,'will_time':预计到店时间,'must_time':合约到店时间}
PUSH23 = u'{}未在规定时间到达'

#type=24,迟到提醒，维修工主管
#{'type':24,'id':oid}
PUSH24 = u'{}师傅未到达{}{}({}),请务必在{}前到店维修.'

#type=25餐厅，离店填写工单，维修工主管
#{'type':25,'id':oid}
PUSH25 = u'报修{}已过维修时效，{}师傅还未上传维修工单。'




