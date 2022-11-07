
from urllib import request
from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics
from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
def get_tokens_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }
class Register(APIView):
    
    def post(self,request):
        serializer=RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':"register succfully"},status=status.HTTP_201_CREATED)
            # return Response({'token':token})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class HomeView(APIView):
    def get(self,request):
        data=SubCategory.objects.all()
        serializer=SubCategorySerializer(data,many=True)
        return Response(serializer.data)

    # def post(self,request):
    #     serializer=SubCategorySerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response({"msg":"Not data is valid"})

    
class CategoryView(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class SubCategoryView(generics.ListAPIView):
    queryset=SubCategory.objects.all()
    serializer_class=SubCategorySerializer

class ProductView(APIView):
    def get(self,r,slug=None):
        if slug != None:
            try:
                obj=Product.objects.get(slug=slug)
                serializer=ProductSrializer(obj,many=False)
                return Response(serializer.data)
            except:
                return Response({"msg":"Product Not found"})
        obj=Product.objects.all()
        serializer=ProductSrializer(obj,many=True)
        return Response(serializer.data)

class AddToCart(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,r,slug):
        print(r.user)
        try:
            product=Product.objects.get(slug=slug)
        
            order_item=OrderProduct.objects.get(product=product,ordered=False,user=r.user)
        
            order_qs=Order.objects.filter(ordered=False,user=r.user)
        
            if order_qs.exists():
                order=order_qs[0]
                if order.product.filter(product__slug=product.slug).exists():
                    order_item.qty +=1
                    serializer=OrderProductSerializer(order_item,data=r.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                else:
                    return Response({"msg":"Middle level Not"})
        except:
            product=Product.objects.get(slug=slug)
           
            ordered_date= timezone.now()
            print(r.data)
            serializer=OrderSerializer(data=r.data)
            if serializer.is_valid():
                serializer.save(product=product)
                return Response({"msg":"Ok"})
            
       
            return Response({"msg":"Product Not found"})
    def post(self,request,slug):
        print(slug)
        try:
            
            product=Product.objects.get(slug=slug)
            ordered_date= timezone.now()
            serializer=OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(product=product)
                return Response({"msg":"Ok"})
            return Response({"msg":"Not order Generate"})
        except:
            return Response({"msg":"Product Not found"})

class MinusQtyFromCard(APIView):
    def put(self,r,slug):
        product=Product.objects.get(slug=slug)
        order_item=OrderProduct.objects.get(product=product,ordered=False)
        order_qs=Order.objects.filter(ordered=False)
        if order_qs.exists():
            order=order_qs[0]
            # serializer=OrderSerializer(order_qs,many=True)
            # return Response(serializer.data)
            if order.product.filter(product__slug=product.slug).exists():
                order_item.qty -=1
                serializer=OrderProductSerializer(order_item,data=r.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response({"msg":"Middle level Not"})
      
        else:
             #Not  working
            ordered_date= timezone.now()
           
            serializer=OrderSerializer(data=r.data)
            if serializer.is_valid():
                serializer.save(product=order_item)
                return Response({"msg":"Ok"})
            return Response({"msg":"Not order Generate"})
class RemoveProduct(APIView):
    def delete(self,r,slug):
        product=Product.objects.get(slug=slug)
        order_item=OrderProduct.objects.get(product=product,ordered=False)
        order_qs=Order.objects.filter(ordered=False)
        if order_qs.exists():
            order=order_qs[0]
            # serializer=OrderSerializer(order_qs,many=True)
            # return Response(serializer.data)
            if order.product.filter(product__slug=product.slug).exists():
                order=OrderProduct.objects.get(product__slug=product.slug)
                order.delete()
                return Response({"msg":"orderItem  Deleted successfully"})
            return Response({"msg":"Middle level Not"})

class MyOrder(APIView):
    def get(self,r):
        obj=Order.objects.filter(ordered=True)
        if obj:
            serializer=OrderSerializer(obj,many=True)
            return Response(serializer.data)

        return Response({"msg":"Not Order Found"})
