from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feedback,Product, Reply, Profile
from django_countries.widgets import CountrySelectWidget

# Create your forms here.

class RegForm(UserCreationForm):

    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )




class FeedbackForm(forms.ModelForm):
    # feedback = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Feedback
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['product'].widget = forms.HiddenInput()



class ReplyForm(forms.ModelForm):
    reply = forms.CharField(widget=forms.Textarea)
    reply.widget.attrs.update(size='10')
    class Meta:
        model = Reply
        fields = "__all__"
       
    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        
        self.fields['sender'].widget = forms.HiddenInput()
        self.fields['receiver'].widget = forms.HiddenInput()
        self.fields['product'].widget = forms.HiddenInput()
        self.fields['feedback'].widget = forms.HiddenInput()




class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget = forms.HiddenInput()
        # self.slug = slugify(self.fields)
        # self.fields['slug'].widget = forms.HiddenInput()

    
class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = {'avatar','bio','store_name','state','country','phone'}
        widgets = {"country": CountrySelectWidget()}
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        # self.fields['username'].widget = forms.HiddenInput()