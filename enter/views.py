from django.shortcuts import render

# Create your views here.


def enter_page(request):
    return render(request, 'enter/home.html')
