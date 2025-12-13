from django import forms 
from blogs.models import Blog, Category
from django.contrib.auth import get_user_model
from users.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()


class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('blog_title', 'blog_category', 'blog_feature_image', 'blog_short_description', 'blog_long_description', 'blog_status', 'is_feature')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category 
        fields = ('category_name',)

class DashboardUserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('email','username','is_active','is_staff','groups')

class DashboardUserProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo','phone')


class DashboardUserFormCreation(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username','email','is_active','is_staff','groups')
