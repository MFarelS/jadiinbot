from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.contrib.sessions.models import Session
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from api.forms import GetUserBySessionForm
import json

@csrf_exempt
def get_user_by_session(request: WSGIRequest):
    res = {}
    if request.method != 'GET':
        res['status_code'] = 405
        res['msg'] = 'Method Not Allowed'
        return HttpResponseNotAllowed(json.dumps(res))
    
    form = GetUserBySessionForm(request.GET)
    if not form.is_valid():
        res['status_code'] = 403
        res['msg'] = 'Bad Request'
        return HttpResponseBadRequest(json.dumps(res))
    
    session = Session.objects.filter(session_key = form.cleaned_data['session_key']).first()
    if not session:
        res['status_code'] = 404
        res['msg'] = 'session_key not found'
        return HttpResponseNotFound(json.dumps(res))
    
    res['data'] = {}
    res['data']['user'] = session.get_decoded().get('_auth_user_id')
    res['status_code'] = 200
    res['msg'] = 'ok'
    return HttpResponse(json.dumps(res))
    

