from django.conf import settings
from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    cat_title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("cover:category", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.cat_title

class SubCategory(models.Model):
    sub_title = models.CharField(max_length=200)
    cat_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_image = models.ImageField(upload_to='sub_image/',null=True,blank=True,default="")
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("cover:subcategory", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.sub_title

class Product(models.Model):
    title = models.CharField(max_length=350)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    # category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subCategory = models.ForeignKey(SubCategory,on_delete=models.SET_NULL,blank=True,null=True)
    image = models.ImageField(upload_to="product/")
    image1 = models.ImageField(upload_to="product/",blank=True,null=True,default="")
    image2 = models.ImageField(upload_to="product/",blank=True,null=True,default="")
    image3 = models.ImageField(upload_to="product/",blank=True,null=True,default="")
    image4 = models.ImageField(upload_to="product/",blank=True,null=True,default="")
    rating = models.FloatField(blank=True,null=True,default=0.0)
    noOfStock = models.IntegerField(default=1)
    stockBoxNo = models.IntegerField(null=True,blank=True)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("cover:product", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

class ProductVariation(models.Model):
    variation = models.ForeignKey(Product,on_delete=models.CASCADE)
    value = models.CharField(max_length=200)#For  colors
    variation_image = models.ImageField(upload_to="product/",null=True,blank=True)
    
    def __str__(self):
        return self.value

class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    produt_variation = models.ManyToManyField(ProductVariation)
    ordered = models.BooleanField(default=False)
    qty = models.IntegerField(default=1)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def get_total_price(self):
        return self.qty * self.product.price
    
    def get_total_discount_price(self):
        return self.qty * self.product.discount_price

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_price()
        else:
            return self.get_total_price()
    def get_saved_amount(self):
        return self.get_total_price() - self.get_final_price()
    
    def get_total_discount_percent(self):
        return int(100-(self.product.discount_price/self.product.price)*100)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=200)
    product = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    delivery_fees = models.FloatField(blank=True)
    address = models.ForeignKey("Address",related_name="shipping_address",on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey("Payment",on_delete=models.SET_NULL,blank=True,null=True)
    coupon = models.ForeignKey("Coupon",on_delete=models.SET_NULL,blank=True,null=True)
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    refund_required = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.product.all():
            total +=order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    def get_total_tax(self): 
        total=self.get_total()
        return round(0.18 * total)
    def get_total_discount_amount(self):
        total=0
        for order_item in self.product.all():
            total += order_item.get_saved_amount()
        return total
    
    def get_payable_amount(self):
        if self.delivery_fees:
            return self.get_total_tax() + self.get_total() + self.delivery_fees

        return self.get_total_tax() + self.get_total() 
    

ADDRESS_CHOICE=(
    ("H","HOME"),
    ("O","OFFICE"),
)
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    contact=models.IntegerField()
    pincode=models.IntegerField()
    locality=models.CharField(max_length=200)
    street_address=models.TextField()
    use_location=models.FloatField(blank=True)
    landmarks=models.CharField(max_length=200,blank=True,null=True)
    alternative_no=models.IntegerField(blank=True,null=True)
    address_type=models.CharField(choices=ADDRESS_CHOICE,blank=True,null=True,max_length=1)
    default=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="Addresses"


class Payment(models.Model):
    text_id=models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount=models.IntegerField()
    timestamp=models.DateTimeField(auto_now_add=True)

class Coupon(models.Model):
    code=models.CharField(max_length=200)
    amount=models.FloatField()
    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reason=models.TextField()
    accepted=models.BooleanField(default=False)
    email=models.EmailField()

    def __str__(self):
        return f"{self.pk}"


