from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .bot import wrap

import json

@csrf_exempt
def wrapper(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		wrap(data)
		return HttpResponse("OK!")
	if request.method == 'GET':
		return HttpResponse("Only for telegram.")

def home(request):
	if request.method == 'GET':
		return HttpResponse("You can get information from FreexelBot telegram bot.")




