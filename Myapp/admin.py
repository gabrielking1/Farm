from django.contrib import admin
from .models import Product,Category,Feedback,Reply,History, Profile
from django.contrib import messages
from django.utils.translation import ngettext
from django.utils.html import format_html
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('choice', 'slug')
    prepopulated_fields = {'slug': ('choice',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    # prepopulated_fields = {'slug': ('name',)}
# admin.site.register(Product, ProductAdmin)

# class OrderAdmin(admin.ModelAdmin):
#     def marked_seen(self, request, queryset):
#         for obj in queryset:
#             if obj.status == False:
#                 updated = queryset.update(status='True')
#                 self.message_user(request, ngettext(
#                     '%d Transaction was successful',
#                     '%d Transactions were successful.',
#                     updated,
#                 ) % updated, messages.SUCCESS)
                
            
                
#             else:
#                 self.message_user(request,
#                     'Error transaction already Apporoved.',  messages.ERROR)
                
            
#     def image_tag(self, obj):
#         return format_html('<img src="{}" width="150" height="150"/>'.format(obj.image.url))

#     image_tag.short_description = 'Image'
    
    
    
#     list_display = ('product', 'status','image_tag',)
    
#     actions = [marked_seen]



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('username', 'product',)
    # prepopulated_fields = {'slug': ('choice',)}

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver','reply','feedback',)

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    # list_display = ('name', 'username','location',)
    list_display = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # list_display = ('name', 'username','location',)
    list_display = ('store_name',)

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ( 'username',)
#     # list_display = ('store_name',)

# @admin.register(Alert)
# class AlertAdmin(admin.ModelAdmin):
#     list_display = ( 'username',)
#     # list_display = ('store_name',)