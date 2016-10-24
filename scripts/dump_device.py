#!/user/bin/env python
# encoding:utf-8

import xlrd
from pymongo import Connection
from bson.objectid import ObjectId
from datetime import datetime as dt

from pypinyin import pinyin, lazy_pinyin
import pypinyin


def get_pinyin_initials(text):
    if not text:return ""
    pinyin_text = ''.join([s[0] for s in lazy_pinyin(text) if len(s) > 0])
    #fixlist = [(u'单', 's'), (u'褚', 'c'), (u'解', 'x')]
    fixlist =  [(u'乘','C'),(u'乘','C'),(u'适','K'),(u'句','G'),(u'阚','K'),(u'车','C'),(u'叶','Y'),(u'合','H'),(u'冯','F'),(u'陶','T'),(u'汤','T'),(u'尾','W'),(u'贾','J'),
        (u'系','X'),(u'将','J'),(u'谷','G'),(u'宿','S'),(u'祭','Z'),(u'氏','S'),(u'石','S'),(u'盛','S'),(u'於','Y'),(u'强','Q'),(u'艾','A'),(u'塔','T'),(u'丁','D'),(u'种','Z'),(u'单','S'),
        (u'解','X'),(u'查','Z'),(u'区','O'),(u'繁','P'),(u'仇','Q'),(u'沈','S'),(u'宁','N'),(u'褚','C'),(u'适','K'),(u'句','G'),(u'阚','K'),(u'焦','J'),
        (u'车','C'),(u'叶','Y'),(u'合','H'),(u'冯','F'),(u'陶','T'),(u'汤','T'),(u'尾','W'),(u'贾','J'),(u'系','X'),(u'将','J'),(u'谷','G'),(u'宿','S'),(u'祭','Z'),(u'氏','S'),(u'石','S'),
        (u'盛','S'),(u'於','Y'),(u'强','Q'),(u'艾','A'),(u'塔','T'),(u'丁','D'),(u'种','Z'),(u'单','S'),(u'解','X'),(u'查','Z'),(u'区','O'),(u'繁','P'),(u'仇','Q'),(u'沈','S'),(u'宁','N'),(u'褚','C')
    ]

    res = []

    for i, j in zip(text, pinyin_text):
        for _i, _j in fixlist:
            if i == _i:
                j  = _j
        res.append(j.upper())

    return u''.join(res)


if __name__ == '__main__':
    conn   = Connection()
    DB     = conn['51quickfix'] 

    data   = xlrd.open_workbook(u'doc/device_new.xlsx')
    table  = data.sheets()[0]
    nrows  = table.nrows
    ncols  = table.ncols
    product_no   = table.cell(3, 8).value
    if not product_no:
        print "餐厅编号不得为空"
        raise
    store = DB.b_k_store.find_one({'no':str(int(product_no))})
    if not store:
        print "未找到该编号的餐厅，请查看餐厅表"
        raise
    keys = ['no', 'ecategory', 'name', 'description', 'model', 'brand', 'supplier', 'qty', 'price']
    for i in range(nrows -1):
        if i > 4:
            item = {'restaurant_name':store['name'], 'restaurant_no':store['no']}
            for i2 in range(ncols):
                if i2 < len(keys):
                    key = keys[i2]
                    cell  = table.cell(i,i2).value
                    item.update({key:cell})
            supplier, name = [item.get(i) for i in ['supplier', 'name']]
            
            if len(item) >0 and supplier and name:
                
                supp =  DB.supplier.find_one({'name':supplier})
                if not supp:
                    supp = DB.supplier.save({'name':supplier, 'create_time':dt.now(), 'update_time':dt.now()})
                prodct = DB.products.find_one({
                                                'name':name, 
                                                'supplier':supp if isinstance(supp, ObjectId) else supp['_id']
                                                })
                if not prodct:
                    prodct = DB.products.save({
                                    'name':name, 
                                    'supplier':supp if isinstance(supp, ObjectId) else supp['_id'],
                                    'create_time':dt.now(),
                                    'update_time':dt.now()
                        })
                brand = DB.brand.find_one({'name':item['brand']})
                if not brand:
                    DB.brand.save({'name':item['brand'], 'create_time':dt.now(), 'initial':get_pinyin_initials(item['brand']), 'update_time':dt.now()})
                item.update({
                            'store':store['_id'],
                            'provider':supplier,
                            'qty':item['qty'],
                            'product':prodct if isinstance(prodct, ObjectId) else prodct['_id'], 
                            'supplier':supp if isinstance(supp, ObjectId) else supp['_id']
                            })
                if item.get('price'):
                    item['price'] = str(item['price'])
                if item.get('qty'):
                    item['qty']   = str(item['qty'])
                if not DB.b_k.find_one({'name':item['name'], 'supplier':item['supplier'], 'product':item['product']}):
                    DB.b_k.save(item)
        

        





















