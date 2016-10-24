#encoding:utf-8
from apps.base.common import json_response, get_json_data
from apps.base.uploader import upload as _upload
from apps.base.common import login_required
from apps.base.logger import getlogger

logger = getlogger(__name__)


@login_required
def upload(request):

    resp = {'info':{},'status':0, 'alert':''}
    error, url = _upload(request, full_url=True)
    
    if error == 0:
        resp['error'] = 0
        resp['status']  = 1
        key = '{}_url'.format(request.REQUEST.get('category'))
        resp['info'][key] = url
    else:
        resp['alert']  = u'上传文件失败'
    resp['url'] = url
    return json_response(resp)




