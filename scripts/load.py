#!/user/bin/env python
#encoding:utf-8

data1   = xlrd.open_workbook(u'data/餐厅信息.xlsx')
columns = [ u'使用部门编号',
			u'使用部门',
			u'地址',
			u'电话',
			u'传真',
			u'邮箱',
			u'联系人',
			u'地区',
			u'城市',
			u'开店日期',
			u'关店日期',
			u'保固日期',
			u'服务商',
			u'冷库服务商（保固期外）',
			u'冷库服务商（保固期内）',
			u'联系人',
			u'联系人手机号码',
			u'省	',
			u'区域',
			u'公司',
			u'管理部门']
table1  = data1.sheets()[0] 
nrows 	= table1.nrows
ncols 	= table1.ncols
result1 = {}
for i in range(nrows):
	if i > 1:
		item = {}
		for i3 in range(ncols):
			key = columns[i3]
			cell   = table1.cell(i,i3).value
			item.update({key:cell})
		result1.update({item[u'使用部门编号']:item})
		

data2      = xlrd.open_workbook(u'data/设备信息.xlsx')
table2     = data2.sheets()[0] 
name, code =  table2.cell(1,23).value, table2.cell(1,24).value
columns = [	
			u"汇总",
			u"B",
			u"区域", 
			u"D",
			u"E",
			U"F",
			u'设备设施名称',
			u'Description',
			u"I",
			u"J",
			u"K",
			u"供应商",
			u"数量",
			u"单价",
			u"合计",
			u"安装费",
			u"运输费",
			u"其它费用",
			u"合计",
			u"备注",
			u"提供者",
			u"型号",
			u"生产日期",
			u"安装日期",
			u"过期日期",
			u"类别",
			u"设备设施类别",
			u"设备类别",
			u"品牌",
			u"固定资产编号",
			u"财富类别代码",
			u"制作厂商",
			u"规格",
			u"设备出厂序列号",
			u"使用状态",
			u"存放地",
			u"购置日期",
			u"单位",
			u"报废时限",
			u"每月折旧金额"]

nrows 	= table2.nrows
ncols 	= table2.ncols
result2 = []
for i2 in range(nrows):
	if i2 > 3:
		item = {u'使用部门编号':code, u'使用部门':name}
		for i4 in range(len(columns)):
			key  = columns[i4]
			cell = table2.cell(i2,i4).value
			item.update({key:cell})
		result2.append(item)