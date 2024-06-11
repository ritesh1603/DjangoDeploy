from django.shortcuts import render

# Create your views here.
#request handler
#request -> response
from django.http import HttpResponse

def hello(request):
    #pull data
    # return HttpResponse('The only way to learn is to live!')
    return render(request, 'hello.html')

def form(request):
    return render(request, 'form.html')
