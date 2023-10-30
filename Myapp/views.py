from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm 
from .models import Product,Location,Feedback,Reply, History, Contact, Profile, Notification, Alert, Category
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from .forms import RegForm, FeedbackForm, ProductForm, ReplyForm,UpdateProfileForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
# from .filters import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models.query_utils import Q
from Myapp.filters import FarmFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json
from siteajax.toolbox import Ajax, AjaxResponse,ajax_dispatch
from django.core.exceptions import ObjectDoesNotExist
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.template import loader
import json












    #     a =  [
#   "Abia",
#   "Adamawa",
#   "Akwa Ibom",
#   "Anambra",
#   "Bauchi",
#   "Bayelsa",
#   "Benue",
#   "Borno",
#   "Cross River",
#   "Delta",
#   "Ebonyi",
#   "Edo",
#   "Ekiti",
#   "Enugu",
#   "FCT - Abuja",
#   "Gombe",
#   "Imo",
#   "Jigawa",
#   "Kaduna",
#   "Kano",
#   "Katsina",
#   "Kebbi",
#   "Kogi",
#   "Kwara",
#   "Lagos",
#   "Nasarawa",
#   "Niger",
#   "Ogun",
#   "Ondo",
#   "Osun",
#   "Oyo",
#   "Plateau",
#   "Rivers",
#   "Sokoto",
#   "Taraba",
#   "Yobe",
#   "Zamfara"
# ]
#     for i in a:
#         Location.objects.create(

#             name = i
#         )


# def uploading(Wizard):
#     storage_name = 'formtools.wizard.storage.session.SessionStorage'
class ProfileView(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'profilePic/photos'))
    form_list = [RegForm,UpdateProfileForm]
    template_name = 'registration.html'
    # Do something with the cleaned_data, then redirect
    # to a "success" page.
    def done(self,  form_list,**kwargs):
        
        user_form = form_list[0]
        username = user_form.cleaned_data.get('username')
        
        print(username)
        if form_list:
            user_form.save()
            userr = User.objects.get(username__icontains=username)
            profile = form_list[1].save(commit=False)
            profile.username =  userr
            profile.save()
            
        return redirect('home')

def home(request):
    notify = Notification.objects.filter(username_id=request.user.id,isread="Unread")
    machinery = Category.objects.get(id=2)
    livestock = Category.objects.get(id=1)
    food = Category.objects.get(id=3)
    alert = Alert.objects.filter(username_id=request.user.id)
    product = Product.objects.all()
    return render(request, 'index2.html',{'product':product,'notify':notify,'alert':alert,
    'machinery':machinery,'food':food,'livestock':livestock 
                                          })


def products(request):
    product = Product.objects.all()
    myfilter = FarmFilter(request.GET, queryset=product)
        
        
    page = request.GET.get('page', 1)

    paginator = Paginator(myfilter.qs, 2)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'products.html',{
                  'product':product,
                  'myfilter':myfilter,
                  'page_obj':page_obj,

    }
    )

def category(request,slug):
    category = get_object_or_404(Category, slug=slug)
    product = Product.objects.filter(choice = category)
    myfilter = FarmFilter(request.GET, queryset=product)
        
        
    page = request.GET.get('page', 1)

    paginator = Paginator(myfilter.qs, 2)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'category.html',{
                  'product':product,
                  'myfilter':myfilter,
                  'page_obj':page_obj,
                  'category':category

    }
    )


def read(request):
    like = request.POST.get('like')
    print("this is like ",like)
    notify = get_object_or_404(Notification, id=like,username_id=request.user.id)
    notify.isread = "Read"
    notify.save()
    return redirect(request.META.get('HTTP_REFERER'))
    


def register(request):
 
    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
        form = RegForm(request.POST)
 
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'email already taken ')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'username already taken ')
                return redirect('register')
            else:
                form.save()
                user = authenticate(username = username,password = password)
                auth.login(request, user)
                return redirect('home')
         
        else:
            return render(request,'registration.html',{'form':form})
     
    else:
        form = RegForm()
        return render(request,'registration.html',{'form':form})
    


def login(request):

    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'invalid login details')
            form = AuthenticationForm()
            return render(request,'login.html',{'form':form})
     
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
    
    
 
def logout(request):
    request.session.clear()
    return redirect('login')


def details(request, slug):
    # try:
        if request.user.is_active and request.user.is_authenticated:
            product = Product.objects.get(slug=slug)
            profile = Profile.objects.get(username=product.username)
            feedback = Feedback.objects.filter(Q(product_id=product))
            backer = Feedback.objects.select_related('product__username').filter(product=product, username_id=request.user.id)
            print('this is backer ',backer)
            # try:
            #     back = Feedback.objects.filter(username_id = request.user.id,product_id=product.id)
            # except ObjectDoesNotExist:
            #     back = None
            # backer = Feedback.objects.get(username_id = request.user.id)                               
            count =  feedback.count()
            if request.method == 'POST':
                sold = int(request.POST.get('Qsold'))
                form = FeedbackForm(request.POST)
            
                if form.is_valid():
                    username = form.cleaned_data['username']
                    feed = form.cleaned_data['chat_with_seller']
                    if feedback.filter(username=username).exists():
                        messages.error(request,'you can only send one feedback per product')
                        return HttpResponseRedirect(reverse("details",args={product.slug}))
                    elif product.username_id == request.user.id:
                        messages.error(request,'you cannot message yourself are you normal?')
                        return HttpResponseRedirect(reverse("details",args={product.slug}))

                    else:
                        Notification.objects.create(
                            username = product.username,
                            notify = feed,
                            topic = product.name,
                            ids = product.id
                        )
                        form.save()
                        return HttpResponseRedirect(reverse("details",args={product.slug}))
               
                else:
                    messages.error(request, 'something no clear ')
                    form = FeedbackForm(initial = {'username':request.user.id,'product':product, 'backer':backer})
                
                
                    
            #         response_message = '<div style="color: green;">Payment successful!</div>'
            #         html_response = f'''
            #     <div id="response-div">
            #         {response_message}
            #     </div>
            #     <script>
            #         setTimeout(function() {{
            #             var responseDiv = document.getElementById('response-div');
            #             responseDiv.style.display = 'none';
            #         }}, 10000); // Set the duration in milliseconds (e.g., 10000ms = 10 seconds)
            #     </script>
            # '''
            
            # # Return the HTML response as HttpResponse
            #     return HttpResponse(html_response)
            else:
                form = FeedbackForm(initial = {'username':request.user.id,'product':product})
            return render(request, 'details.html', {'product': product,'form':form,'feedback':feedback,'count':count, 'backer':backer,'profile':profile})
        else:
            messages.error(request, 'you are not logged in ')
            return redirect('login')
    # except:
    #     messages.error(request,'register to have full access ')
    #     return redirect('register')
    



def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
#       {{content|safe }}
        if form.is_valid():
            form.save()
            return redirect('home')
            # name = request.POST.get('name')
            # body = request.POST.get('description')
            # if Product.objects.filter(name=name):
            #     messages.error(request, 'Blog already exist')
            #     return redirect('create')
            # elif len(body)  < 255:
            #     messages.error(request, 'your content is too small ')
            #     return redirect('create')
            # else:
            #     form.save()
            #     return redirect('home')
         
        else:
            messages.error(request, 'something went wrong')
            return redirect('create')
    
    
    else:
        form = ProductForm(initial = {'username':request.user.id,'title':request.user.username})
        return render(request,'uploader.html',{'form':form})
    


def reply(request, id):
     # try:
        if request.user.is_active and request.user.is_authenticated:
            
            
            curr_user = User.objects.get(id=request.user.id)
            feedback = Feedback.objects.get(id=id)
            print(feedback.username_id)
            product = Product.objects.get(id=feedback.product_id)
            valid = Reply.objects.all()

            # reply = Reply.objects.filter(id=feedback.id)
            # id = getUserId(request.user.username)
            reply =Reply.objects.filter(feedback_id=feedback.id, sender_id=request.user.id,receiver_id=product.username_id ).order_by('id')| Reply.objects.filter(feedback_id=feedback.id, sender_id=product.username_id,receiver_id=feedback.username_id ) | Reply.objects.filter(feedback_id=feedback.id, sender_id=feedback.username_id,receiver_id=request.user.id )
           
            # reply = Feedback.objects.filter(Q(product_id=product),  Q(username_id=request.user.id or product.username_id ))
            count =  reply.count()
            notify = Notification()
            if request.method == 'POST':
                
                form = ReplyForm(request.POST)
            
                if form.is_valid():
                    receiver = form.cleaned_data['receiver']
                    sender = form.cleaned_data['sender']
                    print(' this is reciever', receiver.username)
                    print('this is sender ',sender.username)
                   
                    reply = form.cleaned_data['reply']
                    if valid.filter(reply=reply).exists():
                        messages.error(request,'cant send same reply again')
                        return HttpResponseRedirect(reverse("reply",args={feedback.id}))
                    else:
                        Notification.objects.create(
                            username = receiver,
                            notify = reply,
                            topic = product.name,
                            ids = feedback.id
                        )
                       
                        form.save()
                        
                        
                        return HttpResponseRedirect(reverse("reply",args={feedback.id}))
                else:
                    messages.error(request, 'something no clear ')
                    form = ReplyForm(initial = {'username':request.user.id,'product':product,'sender':product.username_id,'receiver':feedback.username_id, 'feedback':feedback})
                    return render(request, 'chats.html', {'product': product,'form':form,'reply':reply,'count':count})
            else:
                if request.user.is_active and request.user.is_authenticated and request.user.id!=feedback.username_id:
                    form = ReplyForm(initial = {'username':request.user.id,'product':product,'sender':product.username_id,'sender':request.user.id,
                                                'receiver':feedback.username_id, 'feedback':feedback})
                elif request.user.is_active and request.user.is_authenticated and request.user.id==feedback.username_id:
                     form = ReplyForm(initial = {'username':request.user.id,'product':product,'sender':product.username_id,'sender':request.user.id,
                                                'receiver':product.username_id, 'feedback':feedback})
            return render(request, 'chats.html', {
                'product': product,'form':form,'reply':reply,'count':count,
                'feedback': feedback,
                       
                       'curr_user': curr_user,})
        else:
            messages.error(request, 'you are not logged in ')
            return redirect('login')
    # except:
    #     messages.error(request,'register to have full access ')
    #     return redirect('register')



@ajax_dispatch({
    # Map request source element id (see html below)
    # to a handler.
    'news-list': reply,
})

def profile(request,username):
    notify = Notification.objects.filter(username_id=request.user.id,isread="Unread")
    userr = get_object_or_404(User, username=username)
    profile = Profile.objects.get(username=userr)
    users = User.objects.filter(username=profile.username)
    print(userr.id)
    product = Product.objects.filter(username_id=userr.id)
    return render(request,"profile.html",
                  {'product':product,
                   'profile':profile,
                   'users':users,
                   'notify':notify
                   }
                  )

def profileupdate(request,username_id):
    
    username = User.objects.get(id=request.user.id)
    userr = get_object_or_404(Profile, username_id=username.id)
    print(userr.username)
    # usa = 
    if request.method == "POST":
        form = UpdateProfileForm(request.POST,request.FILES, instance=userr)
        
        if form.is_valid():
            

            form.save()
            return HttpResponse(
               f"{userr.username} updated. reload profile to see changes"
                    
            )
    else:
        form = UpdateProfileForm(instance=userr)
    return render(request, 'edit.html', {
        'form': form,
        'userr': userr,
    })
def sell(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
      
        sold = int(request.POST.get('Qsold'))
        if sold < 1:
            messages.error(request, 'product quantity cannot be less than 1 ')
            return redirect('details', slug=product.slug)
        elif sold > product.quantity:
            messages.error(request, f'quantity available is {product.quantity} ')
            return redirect('details', slug=product.slug)

        else:
            product.quantity -=  sold
            
            product.save()
            messages.success(request, "payment successful ")
            return redirect('details', slug=product.slug)

def update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES, instance=product)
        sold = int(request.POST.get('Qsold'))
        if form.is_valid():
            status = form.cleaned_data['status']
            username = form.cleaned_data['username']
            location = form.cleaned_data['location']
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            choice = form.cleaned_data['choice']
            quantity = form.cleaned_data['quantity']
            if quantity < 1:
                product.status = "SoldOut"
                product.save()
                if status == 'SoldOut':
                    History.objects.create(
                        username_id = request.user.id,
                        location = location,
                        name = name,
                        price = price,
                        category = choice
                    )
            else:
                product.quantity -=  sold
                product.status ="Available"
                product.save()
            form.save()
            return HttpResponse(
               f"{product.name} updated. reload profile to see changes"
                    
            )
    else:
        form = ProductForm(instance=product)
    return render(request, 'uploaded.html', {
        'form': form,
        'product': product,
    })


def history(request):
  
    history  = History.objects.filter(username_id=request.user.id)
    return render(request,"history.html", {'history':history})


