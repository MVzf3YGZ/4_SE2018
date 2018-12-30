from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from spider_app.spider_top import spider_get
import json


# Create your views here.

class log(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user_input = []
        user = request.POST.get('user', None)
        email = request.POST.get('email', None)
        temp = {'user': user, 'email': email}
        spider_get(user, email)
        fp = open('jsonfile/' + user + '.json')
        a = json.load(fp)
        a = a['RECORDS'][0]
        return render(request, 'login.html', {'data': a})
        # return HttpResponse('200')
# Create your views here.
