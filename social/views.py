from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from social.forms import AboutForm
from .models import About,SocialLink



def about_page(request):
    return render(request,'social/about.html')

login_required
def dashboard_about_page(request):
    about = About.objects.first()
    Social_links = SocialLink.objects.all()
    context = {
        'about':about,
        'Social_links':Social_links
    }
    return render(request,'dashboards/social/about.html',context)

login_required
def dashboard_about_edit(request,header):
    about = get_object_or_404(About,about_header=header)
    if request.method == 'POST':
        form = AboutForm(request.POST,instance=about)
        if form.is_valid():
            form.save()
            messages.success(request,'About updated successfully!')
            return redirect('social:dashboard_about_page')
    else:
        form = AboutForm(instance=about)
    context = {
        'form':form,
    }
    return render(request,'dashboards/social/about_edit.html',context)


