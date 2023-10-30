from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home, name='home'),
    # path('register/', views.register, name="register"),
    path('register/', views.ProfileView.as_view(), name="register"),
    path('products/', views.products, name='products'),
    path('login/',views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('details/<slug:slug>',views.details, name="details"),
    path('sell/<slug:slug>',views.sell, name="sell"),
    path('reply/<str:id>',views.reply, name="reply"),
    path('create/', views.create, name = 'create'),
    path('profile/<str:username>', views.profile, name = 'profile'),
    path('profileupdate/<str:username_id>', views.profileupdate, name = 'profileupdate'),
    path('update/<slug:slug>',views.update, name="update"),
    path('category/<slug:slug>',views.category, name="category"),
    path('read/', views.read, name = 'read'),
    path('history/', views.history, name='history')
    

]

# htmx_pattern = [
#      path('delete/<str:product_id>', views.delete, name = 'delete')
# ]
# urlpatterns += htmx_pattern
# if settings.DEBUG:
#     urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)