
from django.contrib import admin
from .models import *
# Register your models here.
def make_accepted_refund(modeladmin,request,queryset):
    queryset.update(refund_required=False,refund_granted=True)
    
class OrderAdmin(admin.ModelAdmin):
    list_display=['user','ordered','being_delivered','recieved','refund_required','refund_granted','address','payment','coupon']
    list_display_links=['user','address','payment','coupon']
    list_filter=['ordered','being_delivered','recieved','refund_required','refund_granted']

    search_fields=['user__username','ref_code']
    actions=[make_accepted_refund]

class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['sub_title']

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['price','discount_price','stockBoxNo']
    
admin.site.register(Category)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariation)
admin.site.register(OrderProduct)
admin.site.register(Order,OrderAdmin)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)