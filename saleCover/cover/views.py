
from urllib import request
from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics
from django.utils import timezone

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
    def put(self,r,slug):
        product=Product.objects.get(slug=slug)
        order_item=OrderProduct.objects.get(product=product,ordered=False)
        order_qs=Order.objects.filter(ordered=False)
        if order_qs.exists():
            order=order_qs[0]
            # serializer=OrderSerializer(order_qs,many=True)
            # return Response(serializer.data)
            if order.product.filter(product__slug=product.slug).exists():
                order_item.qty +=1
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
