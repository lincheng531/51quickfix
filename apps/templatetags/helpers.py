#encoding:utf-8

import os
import re
import json
from hashlib import md5
from bson.objectid import ObjectId
from django import forms
from django import template
from settings import DB, DEVICE_TYPE, CALL_STATUS, AREA, COMPANY, COMPANYS
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from apps.base.common import get_pinyin_initials
from apps.base.logger import getlogger


logger = getlogger(__name__)


register = template.Library()

@register.filter
def inventory_search(user):
    head_type = user.head_type
    areas = AREA.get(head_type, [])
    companys = COMPANY.get(head_type, [])
    companys2 = COMPANYS.get(head_type, {}) 
    stores = DB.store.find({'head_type':head_type})
    citys  = {}
    for store in stores:
        area, company, city = [store.get(i) for i in ['area', 'company', 'city']]
        if citys.get(city):
            if company: citys[city][1] = company 
            if area: citys[city][0] = area
        else:
            citys.update({city:[area if area else '', company if company else '']})

    area_template = ''.join(['<a cid="c2" name="are" onclick="javascript:inventory_search(this, 1)" >'+a+'</a>' for a in areas])
    company_template = ''.join(['<a cid="c2" style="width:'+str(len(a)*12)+'px" name="company" onclick="javascript:inventory_search(this, 2)"  area='+companys2.get(a)+'>'+a+'</a>' for a in companys])
    city_template = ''.join(['<a cid="c2" style="width:'+str(len(key)*12)+'px" name="city" onclick="javascript:inventory_search(this, 3)" area='+val[0]+' company='+val[1]+'>'+key+'</a>' for key, val in citys.iteritems()])
    html = '''
            <table class="table4" cellspacing='10'>
                <tr><th>区域</th><td>{}</td></tr>
                <tr><th>所属公司</th><td >{}</td></tr>
                <tr><th>城市</th><td>{}</td></tr>
            </table>
            '''.format(area_template, company_template, city_template)
    return mark_safe(html)


@register.filter
def region(cdata, user):
    stores = DB.store.find({'head_type':user.head_type})
    citys  = {}
    for store in stores:
        area, city = [store.get(i) for i in ['area', 'city']]
        if citys.get(area):
            if city not in citys.get(area, []):
                citys[area].append(city)
        else:
            citys.update({area:[city]})

    province_value, city_value, area_value, data, c_data = '010000', '010100', '010101', [], {}
    pf = lambda x:'0{}'.format(x+1) if len(str(x+1)) == 1 else str(x+1)
    for index, area in enumerate(citys.keys()):
        pid = pf(index)
        pidc = '{}0000'.format(pid)
        if area == cdata.area: province_value = pidc
        data.append('{}:{}'.format(pidc, area))
        c_data.update({pidc:area})
        city = citys.get(area, [])
        for index2, cit in enumerate(city):
            cid = pf(index2)
            cidc = '{}{}00'.format(pid, cid)
            if cdata.city == cit: city_value = cidc
            data.append('{}:{}'.format(cidc, cit))
            region = DB.region.find_one({'name':cit,'rid':{'$regex':'c'}})
            c_data.update({cidc:cit})
            if region:
                districts = DB.region.find({'parent_id':region['rid']})
                for index3, dis in enumerate(districts):
                    name = dis.get('name')
                    didc = u'{}{}{}'.format(pid, cid, pf(index3))
                    if cdata.district == name: area_value = didc
                    c_data.update({didc:name})
                    data.append(u'{}:{}'.format(didc, name))
    html = '''
            <script src="/static/js/jquery.inputbox.js" type="text/javascript"></script>
            <script src="/static/js/jquery.ganged.js" type="text/javascript"></script>
            <link rel="stylesheet" href="/static/css/jquery.inputbox.css" type="text/css" />
            <script type="text/javascript">
            $(function(){var store_data = '''+json.dumps(data)+'''; $('#squar').ganged({'data': store_data, 'width': 150, 'height': 30});})
            var store_data = '''+json.dumps(c_data)+'''
            </script>
            <div id="squar" style="float:left; margin-right:50px;" >
                <input type="hidden" class="province" value="'''+province_value+'''"/>
                <input type="hidden" class="city" value="'''+city_value+'''"/>
                <input type="hidden" class="area" value="'''+area_value+'''"/>
                <div name="province" type="selectbox" style="z-index:2;"><div class="opts"></div></div>
                <div name="city" type="selectbox" style="z-index:2;"><div class="opts"></div></div>
                <div name="area" type="selectbox" style="z-index:2;"><div class="opts"></div></div>
            </div>
            '''
    return mark_safe(html)
            

@register.filter
def city(data):
    items = {}
    regions = DB.store.find()
    indexs = {'A':'ABCD', 'B':'ABCD', 'C':'ABCD', 'D':'ABCD', 'E':'EFGH', 'F':'EFGH', 'G':'EFGH', 'H':'EFGH', 'I':'IJKL','J':'IJKL','K':'IJKL','L':'IJKL','M':'MNOP','N':'MNOP','O':'MNOP','P':'MNOP', 'Q':'QRST','R':'QRST','S':'QRST','T':'QRST','U':'UVWX','V':'UVWX','W':'UVWX','X':'UVWX','Y':'YZ','Z':'YZ'}
    items  = {'ABCD':[],'EFGH':[],'IJKL':[],'MNOP':[],'QRST':[],'UVWX':[],'YZ':[]}
    for reg in regions:
        name    = reg.get('city')
        if name:
            initial = get_pinyin_initials(name)[0].upper()
            if name not in items[indexs[initial]]:items[indexs[initial]].append(name)
        
    citys = [u'上海市',u'南京市',u'北京市',u'杭州市',u'深圳市',u'武汉市',u'广州市',u'长沙市',u'天津市',u'合肥市',u'厦门市',u'保定市']
    template = "<a href=\"javascript:jump('region', '{}', 'page')\">{}</a>"
    
    trs, td = [], []
    for c in citys:
        td.append(template.format(c, c))
    trs.append('<span class="citys" id="FIRST">{}</span>'.format("".join(td)))

    for tag, citys in items.iteritems():
        td = []
        for c in citys:
            td.append(template.format(c, c))
        trs.append('<span class="citys" id="{}" style="display:none">{}</span>'.format(tag, "".join(td)))

    return mark_safe(''.join(trs))

@register.filter
def store(data):
    query = {}
    if data.get('region'):
        query['city'] = data.get('region')
    return [{'id':str(i['_id']), 'name':i.get('name'), 'no':i.get('no')} for i in DB.store.find(query)]

@register.filter
def paginat(data, p):
    if len(data) < 20: return data
    if p <10:
        return data[0:20]
    return data[int(p)-10:int(p)+10]


@register.filter
def search_form(txt):
    txts = txt.split('|')
    name = txts[0]
    tip  = txts[1] 
    html = '<div style="width:360px;line-height:30px;;height:30px;background-color:#FF7315;"><label for="box" style="text-align:center;color:#ffffff;padding:0 15px;font-weight:bold">'+name+'</label><input type="text"  value="'+tip+'" onfocus="this.value=\'\'" onblur="if(this.value==\'\'){this.value=\''+tip+'\'}"  name="tag" id="store" style="width:275px;border:none;height:23px;line-height:23px;margin-bottom:2px;margin-right:3px;"/><input type="image" src="/static/images/icon_search.png" value="查询" /></div>'
    return mark_safe(html)


@register.filter
def search_squar(txt):
    txts = txt.split('|')
    name = txts[0]
    tip  = txts[1] 
    hip  = '<input name="q" value="'+txts[2]+'" type="hidden"/>' if len(txts) > 2 else ''
    html = '<div style="width:360px;line-height:30px;;height:30px;background-color:#FF7315;"><form action="" method="GET"><label for="box" style="text-align:center;color:#ffffff;padding:0 15px;font-weight:bold">'+name+'</label><input type="text"  value="'+tip+'" onfocus="this.value=\'\'" onblur="if(this.value==\'\'){this.value=\''+tip+'\'}"  name="tag" id="store" style="width:275px;border:none;height:23px;line-height:23px;margin-bottom:2px;margin-right:3px;"/><input type="image" src="/static/images/icon_search.png" value="查询" /></form></div>'
    return mark_safe(html)

@register.filter
def search_call(data):
    html = '<div style="width:360px;line-height:30px;;height:30px;background-color:#FF7315;"><form action="" method="GET"><label for="store" style="text-align:center;color:#ffffff;padding:0 15px;font-weight:bold">设备</label><input type="text"  value="请输入设备名称" onfocus="this.value=\'\'" onblur="if(this.value==\'\'){this.value=\'请输入餐厅名称或者编号\'}"  name="tag" id="store" style="width:275px;border:none;height:23px;line-height:23px;margin-bottom:2px;margin-right:3px;"/><input type="image" src="/static/images/icon_search.png" value="查询"/></form></div>'
    return mark_safe(html)

@register.filter
def search_store_admin(data):
    html = '<div style="width:360px;line-height:30px;;height:30px;background-color:#FF7315;"><form action="" method="GET"><label for="store" style="text-align:center;color:#ffffff;padding:0 15px;font-weight:bold">商户</label><input type="text"  value="请输入餐厅名称或者编号" onfocus="this.value=\'\'" onblur="if(this.value==\'\'){this.value=\'请输入餐厅名称或者编号\'}"  name="store" id="store" style="width:275px;border:none;height:23px;line-height:23px;margin-bottom:2px;margin-right:3px;"/><input type="image" src="/static/images/icon_search.png" value="查询"/></form></div>'
    return mark_safe(html)

@register.filter
def search_account_admin(data):
    html = '<div style="width:360px;line-height:30px;;height:30px;background-color:#FF7315;"><form action="" method="GET"><label for="tag" style="text-align:center;color:#ffffff;padding:0 15px;font-weight:bold">检索</label><input type="text"  value="请输入餐厅名称或编号或城市或用户名或手机号码" onfocus="this.value=\'\'" onblur="if(this.value==\'\'){this.value=\'请输入餐厅名称或编号或城市或用户名或手机号码\'}"  name="tag"  style="width:275px;border:none;height:23px;line-height:23px;margin-bottom:2px;margin-right:3px;"/><input type="image" src="/static/images/icon_search.png" value="查询"/></form></div>'
    return mark_safe(html)

@register.filter
def search_account(data):
    html = '<div style="width:360px;line-height:30px;;height:30px;background-color:#FF7315;"><form action="/store/account/list" method="GET"><label for="tag" style="text-align:center;color:#ffffff;padding:0 15px;font-weight:bold">检索</label><input type="text"  value="请输入餐厅名称或编号或城市或用户名或手机号码" onfocus="this.value=\'\'" onblur="if(this.value==\'\'){this.value=\'请输入餐厅名称或编号或城市或用户名或手机号码\'}"  name="tag"  style="width:275px;border:none;height:23px;line-height:23px;margin-bottom:2px;margin-right:3px;"/><input type="image" src="/static/images/icon_search.png" value="查询"/></form></div>'
    return mark_safe(html)

@register.filter
def search_store(data):
    html = '<div style="width:360px;line-height:30px;;height:30px;background-color:#FF7315;"><form action="/store/assets/list" method="GET"><label for="store" style="text-align:center;color:#ffffff;padding:0 15px;font-weight:bold">商户</label><input type="text"  value="请输入餐厅名称或者编号" onfocus="this.value=\'\'" onblur="if(this.value==\'\'){this.value=\'请输入餐厅名称或者编号\'}"  name="store" id="store" style="width:275px;border:none;height:23px;line-height:23px;margin-bottom:2px;margin-right:3px;"/><input type="image" src="/static/images/icon_search.png" value="查询"/></form></div>'
    return mark_safe(html)

@register.filter
def search_deivce(data):
    html = '<div style="width:280px;line-height:28px;;height:28px;background-color:#FF7315;padding-left:3px"><form action="" method="GET"><input type="text"  value="请输入资产名称或者编号" onfocus="this.value=\'\';this.style.color=\'#000\'" onblur="if(this.value==\'\'){this.value=\'请输入资产名称或者编号\';this.style.color=\'#555\'}" name="device" id="device" style="width:250px;border:none;height:25px;line-height:25px;margin-bottom:2px;margin-right:3px;color:#555"/><input type="image" src="/static/images/icon_search.png" value="查询"/></form></div>'
    return mark_safe(html)

@register.filter
def search_box(data):
    p = []
    for k, v in data.iteritems():
        if v:
            if k == 'q' and v in ['0', '1,3,5', '2,4']:
                pass
            else:
                item = {}
                if k in ['brand','supplier']:
                    item = getattr(DB, k).find_one({'_id':ObjectId(v)})
                elif k in ['region','efcategory','category','category', 'product', 'inventory_status', 'inventory_detail_status']:
                    item = {'name':v}
                elif k in ['state']:
                    item = {'name':u'非紧急' if v=='2' else u'紧急'}
                elif k in ['area', 'company']:
                    item = {'name':v}
                elif k in ['error_code']:
                    item = getattr(DB, k).find_one({'_id':ObjectId(v)})
                    item = {'name':item.get('error')}
                elif k in 'status':
                    item = {'name':CALL_STATUS.get(int(v))}
                elif k == 'tag':
                    item = {'name':v}
                elif k == 'store':
                    try:
                        item = DB.store.find_one({'_id':ObjectId(v)})
                    except Exception as e:
                        item = DB.store.find_one({'$or':[{'name':{'$regex':v}},{'no':{'$regex':v}}]})
                elif k in ['start_day', 'end_day']:
                    item = {'name':v}
                if item:
                    p.append('<li name="{}" value="{}">{}</li>'.format(k, v, item.get('name')))
    return mark_safe('<div class="search_box"><ul>{}</ul></div>'.format(''.join(p))) if p else ''

@register.filter
def nav_box(text, needs_autoescape=True):
    result, ipt = [], '<input type="text">'
    data  = []
    if text == 'category':
        ipt = ''
        data = [{'_id':i, 'name':i} for i in  DEVICE_TYPE.keys()]
    elif text == 'state':
        ipt=''
        data = [{'_id':1, 'name':u'紧急'},{'_id':2, 'name':u'非紧急'}]
    elif text == 'status':
        ipt = ''
        data = [{'_id':k, 'name':v} for k,v  in CALL_STATUS.iteritems()]
    elif text == 'product':
        ipt = ''
        data = [{'_id':p, 'name':p} for p in DB.product.find().distinct('name')]
    elif text == 'error_code':
        ipt = ''
        data = [{'_id':i['_id'], 'name':"{}-{}".format(i.get('name'),i.get('error'))} for i in  getattr(DB, text).find()]
    elif text == 'region':
        ipt = ''
        data = [{'_id':i.get('name'), 'name':i.get('name')} for i in getattr(DB, text).find({'rid':{'$regex':'c'}})]
    elif text == 'use_status':
        status_message = [u'未盘点', u'存在', u'缺失', u'租借', u'买卖', u'闲置', u'报废']
        ipt = ''
        data = [{'_id':s, 'name':s} for s in status_message]
    elif text == 'inventory_status':
        status_message = [u'未开始', u'进行中', u'已完成']
        ipt = ''
        data = [{'_id':s, 'name':s} for s in status_message]
    else:
        ipt = ''
        data = getattr(DB, text).find()
    for i in data:
        result.append('<li id="{}">{}</li>'.format(i['_id'],i.get('name')))
    return mark_safe('<div id="dropdown_{}" class="none">{}<ul>{}</ul></div>'.format(text, ipt, ''.join(result)))

@register.filter
def fix_none(text):
    return text if text else ''

@register.filter
def count(text):
    return len(text)

@register.filter
def default_logo(text):
    return text if text else '/static/images/avatar_l.png'

@register.filter
def md5_str(text):
    if text is None:
        return None
    return md5(text).hexdigest()

@register.filter
def thumb(url):
    b = url[0:-4]
    return '{}_thumb.jpg'.format(b)

@register.filter
def user_info(uid,key='username'):
    try:
        oid = ObjectId(uid)
    except:
        return uid

    user = DB.user.find_one({'_id':oid})
    if not user:
        return None

    return user.get(key)

@register.filter
def user_select_field(form, index):
    res = []
    names = ['train_type_', 'train_name_', 'train_brand_', 'train_category_', 'train_day1_', 'train_day2_', 'train_msg_']
    for name in names:
        key = '{}{}'.format(name, index)
        boundField = forms.forms.BoundField(form, form.fields[key], key)
        res.append(boundField)
    html ='''<div class="cbox">
                <p>{}</p>
                <p>证件名称:{}</p>
                <p>品牌:{}</p>
                <p>设备:{}</p>
                <p>有效期:{}-{}</p>
            </div>
            <div class="cbox">
                <p>{}</p>
                <p>失败原因:{}</p>
            </div>'''.format(res[0][0], res[1], res[2], res[3], res[4], res[5], res[0][1], res[6])
    return mark_safe(html)

@register.filter
def truncatewords(s,num,end_text='...'):  
    if s:
        if len(s) > num:
            return s[0:num] + end_text
        return s
    return ''


@register.inclusion_tag('sec/global_detail.tag.html')
def sec_global_detail(item):
    exclude = ['_id','_types','ranking','_cls','id','initials','initial','created_at','updated_at']
    return {'item':item,'exclude':exclude}


@register.inclusion_tag('sec/global_form.tag.html')
def sec_global_form(form):
    return {'form':form}


