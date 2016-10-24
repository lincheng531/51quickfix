#encoding:utf-8
import os
import StringIO
from PIL import Image
from hashlib import md5
from datetime import datetime as dt
from apps.base.common import json_response
from settings import *
from apps.base.logger import getlogger
from bson.objectid import ObjectId as _id


logger = getlogger(__name__)

def transpose(filename, angle=90):
    assert angle in [90, 180]

    im = Image.open(filename)
    angle_val = getattr(Image, 'ROTATE_{}'.format(angle)) 
    new_im = im.transpose(angle_val)
    new_im.save(filename, 'jpeg', quality=100)

    return True


def base_upload(request):
    logger.info("start base upload 1")
    f           = request.FILES.get('file') or  request.FILES.get('imgFile')
    category    = request.REQUEST.get('category','upload')

    base_path   =  STATIC_ROOT + '/' + category

    now         = dt.now()
    dir1        = str(now.year)
    dir2        = str(now.month)
    dir3        = str(now.day) 
    dir_path    = os.path.join(base_path,dir1,dir2,dir3)
  
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    sufix       = f.name.rsplit('.')[-1].lower()
    file_name   = '{}.{}'.format(str(_id()),sufix)
    full_path   = os.path.join(dir_path,file_name)

    if sufix not in ['jpg','png','jpeg','gif', 'pdf', 'xls', 'xlsx', 'docx', 'doc']:
        return 1, ''
    
    #with open(full_path,'wb') as _f:
    #    _f.write(f_data)
        
    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return 0, '/static/{}/{}/{}/{}/{}'.format(category,dir1,dir2,dir3,file_name)
    
    
def upload(request,max_size=(1000,1000),category=None, full_url=True):
    logger.info("start upload 1")

    f           = request.FILES.get('file') or  request.FILES.get('imgFile')
    category    = category or request.REQUEST.get('category','upload')
    base_path   = STATIC_ROOT + '/upload'

    f_data      = f.read()
    md5_key     = md5(f_data).hexdigest()
    dir1        = md5_key[0:2]
    dir2        = md5_key[2:4]
    dir3        = md5_key[4:6]
    dir_path    = os.path.join(base_path,dir1,dir2,dir3)
  
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    sufix       = f.name.rsplit('.')[-1].lower()
    file_name   = '{}.{}'.format(md5_key,sufix)
    full_path   = os.path.join(dir_path,file_name)
    
    thumb_size = (100,100)
    thumb_file_name = '{}_thumb.{}'.format(md5_key,sufix)
    thumb_full_path   = os.path.join(dir_path,thumb_file_name)
            
    # 判断文件类型
    if sufix in ['jpg','png','jpeg','gif']:
        file_name   = '{}.{}'.format(md5_key,sufix)

        try:
            im = Image.open(StringIO.StringIO(f_data))
        except IOError,e:
            return 1,'io error:{}'.format(e.message)
        
        try:
            im.thumbnail(max_size,Image.ANTIALIAS)
            im.convert('RGB').save(full_path,'jpeg',quality=100)

            # gen thumb pic
            im.thumbnail(thumb_size,Image.ANTIALIAS)
            im.convert('RGB').save(thumb_full_path,'jpeg',quality=80)

        except Exception,e:
            print str(e)
            return 1,'can not convert:{}'.format(e)

    with open(full_path,'wb') as _f:
        _f.write(f_data)

    path= '/{}/{}/{}/{}/{}'.format(category,dir1,dir2,dir3,file_name)
    return 0 ,path
