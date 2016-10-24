#!/user/bin/env python
#encoding:utf-8

import xml.dom.minidom
from pypinyin import pinyin, lazy_pinyin
import pypinyin


def get_full_pinyin_initials(text):
    res = lazy_pinyin(text)
    return u''.join(res)

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


dom = xml.dom.minidom.parse('province/Provinces.xml')
root = dom.documentElement

results = []
for i in  root.getElementsByTagName('Province'):
	rid, name, parent_id =  i.getAttribute('ID'), i.getAttribute('ProvinceName'), '0'
	results.append({
					'name':name,
					'rid':"p{}".format(rid),
					'parent_id':parent_id,
					'short_name_en':get_pinyin_initials(name),
					'name_en':get_pinyin_initials(name)
				})


dom = xml.dom.minidom.parse('province/Cities.xml')
root = dom.documentElement
for i in  root.getElementsByTagName('City'):
	rid, parent_id, name =  i.getAttribute('ID'), i.getAttribute('PID'), i.getAttribute('CityName')
	results.append({
					'name':name,
					'rid':"c{}".format(rid),
					'parent_id':"p{}".format(parent_id),
					'short_name_en':get_pinyin_initials(name),
					'name_en':get_pinyin_initials(name)
				})

dom = xml.dom.minidom.parse('province/Districts.xml')
root = dom.documentElement
for i in  root.getElementsByTagName('District'):
	rid, parent_id, name =  i.getAttribute('ID'), i.getAttribute('CID'), i.getAttribute('DistrictName')
	results.append({
					'name':name,
					'rid':"d{}".format(rid),
					'parent_id':"c{}".format(parent_id),
					'short_name_en':get_pinyin_initials(name),
					'name_en':get_pinyin_initials(name)
				})

from bson.objectid import ObjectId as _id
from pymongo import Connection
conn = Connection()
db = conn['51quickfix']

for res in results:
	db.region.save(res)
