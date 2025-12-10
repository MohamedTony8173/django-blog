from django.shortcuts import render

def about_page(request):
    return render(request,'social/about.html')
