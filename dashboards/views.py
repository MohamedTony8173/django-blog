from django.shortcuts import render


def dashboard(request):
    return render(request, "dashboards/index.html")
