
from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        # fields=['id','cat_title','description','slug']
        fields="__all__"

class SubCategorySerializer(serializers.ModelSerializer):
    # cat_id=CategorySerializer()
    class Meta:
        model=SubCategory
        fields=['id','sub_title','cat_id','sub_image','slug']
    
    def to_representation(self, instance):
        response= super().to_representation(instance)
        response['cat_id']=CategorySerializer(instance.cat_id).data
        return response
   
class ProductSrializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductVariation
        fields=['id','variation','value','variation_image']
    def to_representation(self, instance):
        res= super().to_representation(instance)
        res['variation'] = ProductSrializer(instance.variation).data
        return res
class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderProduct
        # exclude=['user']
        fields='__all__'
        depth=1

    def to_representation(self, instance):
        res= super().to_representation(instance)
        res['product']=ProductSrializer(instance.product).data
        return res
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        # exclude=["user"]
        fields='__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        # exclude=["user"]
        fields='__all__'
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['id','address','payment','coupon','ref_code','product','start_date','delivery_fees','ordered','being_delivered','recieved','refund_required','refund_granted']
        depth=1
    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['address'] = AddressSerializer(instance.address).data
        res['payment'] = PaymentSerializer(instance.payment).data
        res['coupon'] = CouponSerializer(instance.coupon).data

        return res
class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model=Refund
        fields="__all__"
    
    def to_representation(self, instance):
        res=super().to_representation(instance)
        res['order']=OrderProductSerializer(instance.order).data
        return res
