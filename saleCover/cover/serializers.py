
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class RegisterUserSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    # contact=serializers.IntegerField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password=serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2=serializers.CharField(write_only=True,required=True,validators=[validate_password])
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name','password2']
        
        extra_Kwargs={
            'first_name':{"required":True},
            'last_name':{"required":True}
        }
    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Password did not match")
        return data
    
    def save(self):
        user = User()
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.username = self.validated_data['username']
        user.email = self.validated_data['email']
        # user.contact = self.validated_data['contact']
        user.is_staff = True
        user.is_active = True
        user.set_password(self.validated_data['password'])
        
        user.save()
        return user

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
        depth=1

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
