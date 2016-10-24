# -*- encoding: utf-8 -*-
from pymongo import Connection
# from apps.base.models.base import HEAD_BRAND
import cStringIO
import datetime
import xlwt

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

HEAD_BRAND = {
    2: u'汉堡王',
    3: u'达美乐',
    4: u'永和大王'
}

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
                        _value = datetime.datetime.strptime(_value, df)
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

def list_export():
    result = []
    order = ['_id', 'head_type', 'category', 'efcategory', 'ecategory', 'no', 'barcode', 'purchase_code', 'description', 'name', 'model', 'specification', 'initial', 'brand_name']
    trans_order = [u'id', u'餐厅的类别', u'类别', u'设备设施类别', u'分类', u'编号', u'二维码', u'采购码', u'描述', u'设备名称', u'型号', u'规格', u'首字母', u'品牌名称']

    conn = Connection()
    DB = conn['51quickfix']
    products = DB.product.find({'head_type':2})
    for product in products:
        product['_id'] = str(product['_id'])
        product['head_type'] = HEAD_BRAND.get(product['head_type'], '')
        result.append(product)

    f_object = to_excel(result, order, trans_order)

    with open('products.xls', 'wb') as f:
        f.write(f_object.read())


if __name__ == '__main__':
    list_export()
