from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'theme/index.html')



def home1(request):
    return render(request, 'theme/home1.html')