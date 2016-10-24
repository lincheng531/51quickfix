#encoding:utf-8
import math
import time
import cStringIO
import xlwt
from datetime import datetime as dt
from django.contrib.auth import login as _login
from settings import DB,SESSION_COOKIE_AGE


def login(request,user):

    if user:
        user.backend = 'mongoengine.django.auth.MongoEngineBackend'
        res = _login(request,user)
        user.last_login = dt.now()
        user.save()
        request.session.set_expiry(SESSION_COOKIE_AGE)
        
        return res

    return False

def rad(d):
    """to弧度
    """
    return d * math.pi / 180.0

def distanceByLatLon(f0, f1, t0, t1):
    EARTH_RADIUS_METER =6378137.0;
    flon = rad(f0)
    flat = rad(f1)
    tlon = rad(t0)
    tlat = rad(t1)
    con  =  math.sin(flat)*math.sin(tlat)
    con  += math.cos(flat)*math.cos(tlat)*math.cos(flon - tlon)
    return round(math.acos(con)*EARTH_RADIUS_METER/1000,4) 


pf = lambda x:x.strftime('%H:%M') if x else ''
pf2 = lambda x:x.strftime('%Y-%m-%d') if x else ''
def pf3(x):
    if x:
        if dt.now().strftime('%Y-%m-%d') == x.strftime('%Y-%m-%d'):
            return pf(x)
        if dt.now().strftime('%Y') == x.strftime('%Y'):
            return x.strftime('%m-%d %H:%M')
        return x.strftime('%Y-%m-%d %H:%M')
    return ''
pf4 = lambda x:x.strftime('%Y/%m/%d') if x else ''
pf5 = lambda x:x.strftime(u'%Y年%m月%d日') if x else ''

def pf6(x):
    x1 = float(x)/float(60) 
    if x1 < 60 and x1 > -60:
        return u"{}分".format(round(float(x)/float(60), 2))
    x2 = float(x)/float(3600) 
    if x2 < 24 and x2 > -24:
        return u"{}小时".format(round(float(x)/float(3600), 2))
    x3 = float(x)/float(86400)
    if  x3 > 1 or x2 < -1:
        return u"{}天".format(round(float(x)/float(86400),2))
    return u"{}秒".format(x)

def pf7(x):
     return time.mktime(x.timetuple())

pf8 = lambda x:dt.strptime(x, '%Y%m%d%H%M%S')
pf9 = lambda x:x.strftime('%Y-%m-%d %H:%M')

def _send_count(head_type=2):
    now = dt.now()
    send_day  = now.strftime('%Y%m%d')
    start_send_day = dt.strptime('{} 00:00:01'.format(send_day), '%Y%m%d %H:%M:%S')
    end_send_day   = dt.strptime('{} 23:59:59'.format(send_day), '%Y%m%d %H:%M:%S')
    send_count     = DB.maintenance.find({'head_type':head_type, 'create_time':{'$lte':end_send_day, '$gte':start_send_day}}).count() + 1
    send_len = 3 if head_type > 1 else 5
    send_counts = '{}{}{}{}'.format(head_type, send_day, (send_len-len(str(send_count)))*'0', send_count)
    return send_counts

def countdown_time(u, close_time):
    seconds = (dt.now() - close_time).seconds
    h = seconds/3600
    m = (seconds - h * 3600)/60
    if m > 0:
        return u - 1 - h, 60 - m
    return u - h, m 


date_formats = [
    '%Y-%m-%d',
    '%y-%m-%d',
    '%Y-%m-%d %H:%M',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y-%m-%d %H:%M',
    '%Y/%m/%d',
    '%y/%m/%d'
]

def get_width(num_characters):
    #num_characters = len(str(uni))
    #cn = len(re.findall(u'[\u4e00-\u9fa5]', uni.decode('utf-8'), re.U))
    if num_characters > 50:
        num_characters = 50
    return int((1+(num_characters)) * 250)

def to_excel(_result, order, trans_order):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet1')

    xlwt.add_palette_colour("header_color", 0x21)
    wb.set_colour_RGB(0x21, 74, 178, 226)
    header_style = xlwt.easyxf('pattern: pattern solid, fore_colour header_color; font: colour white, bold True;')

    default_stype = xlwt.XFStyle()
    default_stype.alignment.wrap = 1
    default_stype.num_format_str = '@'
    default_stype.alignment.vert = xlwt.Alignment.VERT_TOP

    #caculate column max width
    max_len = [0] * len(order)
    for i in range(len(order)):
        _ = len(trans_order[i])
        if _ > max_len[i]:
            max_len[i] = _
    for i in range(len(_result)):
        item = _result[i]
        for j in range(len(order)):
            _value = item.get(order[j])
            if _value is None:
                _value = ''
            _ = len(_value)
            if _ > max_len[j]:
                max_len[j] = _

    for i in range(len(order)):
        ws.write(0, i, unicode(trans_order[i]), header_style)
        ws.col(i).width = get_width(max_len[i])

    output_df = ''

    total_row_offset = 0

    for i in range(len(_result)):
        current_row = i + total_row_offset
        rel_row_offset = 0
        item = _result[i]

        for j in range(len(order)):
            _value = item.get(order[j])
            if _value is None:
                _value = ''
            if isinstance(_value, str) or isinstance(_value, unicode):
                _value = unicode(_value)

            if 'date' in str(order[j]).lower() and output_df:
                for df in date_formats:
                    try:
                        _value = dt.strptime(_value, df)
                        _value = unicode(_value.strftime(output_df)) #'%Y-%m-%d'
                        break
                    except:
                        continue

            if isinstance(_value, list) and _value:
                end_row = current_row
                merged_data = [u'{}{}\n{}'.format(trans_order[j], k+1, item) for k, item in enumerate(_value)]
                end_row += len(merged_data) - 1

                if end_row > current_row:
                    ws.write_merge(current_row+1, end_row+1, j, j, '\n\n'.join(merged_data), default_stype)

                rel_row_offset = max(rel_row_offset, end_row - current_row)
            else:
                try:
                    ws.write(current_row+1, j, _value, default_stype)
                except:
                    raise
        total_row_offset += rel_row_offset

    f = cStringIO.StringIO()
    wb.save(f)
    f.seek(0)
    return f

 
