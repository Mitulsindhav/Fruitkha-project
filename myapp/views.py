from django.shortcuts import render,redirect
from .models import User,Product,Wishlist,Cart
import requests
import random
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe   
from django.conf import settings


stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'
# Create your views here.

def index(request):
    return render(request,'index.html')

def seller_index(request):
    return render(request,'seller-index.html')    

def about(request):
    return render(request,'about.html')

def error404(request):
    return render(request,'404.html')

def single_product(request):
     net_price=0
     user=User.objects.get(email=request.session['email'])
     carts=Cart.objects.filter(user=user,payment_status=False)
     for i in carts:
          net_price+=i.total_price
     return render(request,'single-product.html' ,{'carts':carts,'net_price':net_price})

def single_news(request):
    return render(request,'single-news.html')

def contact(request):
    return render(request,'contact.html')

def shop(request):
    products=Product.objects.all()
    return render(request,'shop.html',{'products':products})

def news(request):
    return render(request,'news.html')

def cart(request):
    return render(request,'cart.html')

def check_out(request):
    return render(request,'checkout.html')

def signup(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            msg="Email Already Registerd"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    phone=request.POST['phone'],
                    message=request.POST['message'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    usertype=request.POST['usertype'],
                )
                msg=" User Sign Up Successfully"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Does Not Matched"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['fname']=user.fname
                if user.usertype=="buyer":
                    wishlists=Wishlist.objects.filter(user=user)
                    carts=Cart.objects.filter(user=user,payment_status=False)
                    return render(request,'index.html')
                else:
                    return render(request,'seller-index.html')
            else:
                msg="Incorrenct Password"  
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email Not Registred"
            return render(request,'login.html',{'msg':msg})

    else:
        return render(request,'login.html')

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return render(request,'login.html')
    except:
        return render(request,'login.html')

def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.phone=request.POST['phone']
        user.message=request.POST['message']
        user.save()
        msg="Profile Updated Successfull"
        if user.usertype=="buyer":
            return render(request,'profile.html',{'msg':msg,'user':user})
        else:
            return render(request,'seller-profile.html',{'msg':msg,'user':user})

    else:
         if user.usertype=="buyer":
            return render(request,'profile.html',{'user':user})   
         else:
            return render(request,'seller-profile.html',{'user':user}) 
         
def change_password(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                if user.password!=request.POST['new_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    del request.session['email']
                    del request.session['fname']
                    return render(request,'login.html')
                else:
                    msg="Your New Password Can't Be From Your Old Password"
                    if user.usertype=="buyer":
                        return render(request,'change-password.htnl',{'msg':msg})
                    else:
                        return render(request,'seller-change-password.htnl',{'msg':msg})
            else:
                msg="Your New Password & Confirm New Password Does Not Matched"
                if user.usertype=="buyer":
                    return render(request,'change-password.html',{'msg':msg})
                else:
                    return render(request,'seller-change-password.html',{'msg':msg})
        else:
            msg="Old Password Does Not Matched"
            if user.usertype=="buyer":
                return render(request,'change-password.html',{'msg':msg})
            else:
                return render(request,'seller-change-password.html',{'msg':msg})
    else:
        if user.usertype=="buyer":
            return render(request,'change-password.html')
        else:
            return render(request,'seller-change-password.html')  


def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(phone=request.POST['phone'])
			phone=str(user.phone)
			otp=str(random.randint(1000,9999))
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"DwF5Auzh16qo3fXC2JMSTcOiyBEZmWH0eR8GIg4NbQrpUnKsjvhz0YwyOCGvHJEFuXRrTc7feDVaM1NA","message":otp,"language":"english","route":"q","numbers":phone}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			request.session['otp']=otp
			request.session['phone']=phone
			return render(request,'otp.html')
		except Exception as e:
			print(e)
			msg="Phone Number Not Regsistered"
			return render(request,'forgot-password.html',{'msg':msg})
	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	otp1=request.session['otp']
	otp2=request.POST['otp']
	if otp1==otp2:
		del request.session['otp']
		return render(request,'new-password.html')
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'msg':msg})

def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		user=User.objects.get(phone=request.session['phone'])
		user.password=request.POST['new_password']
		user.save()
		del request.session['phone']
		msg="Password Updated Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="New Password & Confirm New Password Does Not Matched"
		return render(request,'new-password.html',{'msg':msg})


def seller_add_product(request):
     if request.method=="POST":
          seller=User.objects.get(email=request.session['email'])
          Product.objects.create(
               seller=seller,
               product_name=request.POST['product_name'],
               product_price=request.POST['product_price'],
               product_desc=request.POST['product_desc'],
               product_picture=request.FILES['product_picture'],
               
          )
          msg="Product Added Successfully"
          return render(request,'seller-add-product.html',{'msg':msg})
     else:
          return render(request,'seller-add-product.html')

def seller_view_product(request):
     seller=User.objects.get(email=request.session['email'])
     products=Product.objects.filter(seller=seller)
     return render(request,'seller-view-product.html',{'products':products})        

def seller_product_details(request,pk):
     product=Product.objects.get(pk=pk)
     return render(request,'seller-product-details.html',{'product':product})     

def  product_details(request,pk):
     wishlist_flag=False
     cart_flag=False
     product=Product.objects.get(pk=pk)
     user=User.objects.get(email=request.session['email'])
     try:
          Wishlist.objects.get(user=user,product=product)
          wishlist_flag=True
     except:
          pass

     try:
          Cart.objects.get(user=user,product=product,payment_status=False)
          cart_flag=True
     except:
          pass          
     return render(request,'product-details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})     


def seller_edit_product(request,pk):
     product=Product.objects.get(pk=pk)
     if request.method=="POST":
          product.product_name=request.POST['product_name']
          product.product_price=request.POST['product_price']
          product.product_desc=request.POST['product_desc']
          try:
             product.product_picture=request.FILES['product_picture']
          except:
               pass
          product.save()
          return redirect('seller-view-product')

     else:
        return render(request,'seller-edit-product.html',{'product':product})
     
def seller_delete_product(request,pk):
     product=Product.objects.get(pk=pk)
     product.delete()
     return redirect('seller-view-product')


def add_to_wishlist(request,pk):
     product=Product.objects.get(pk=pk)
     user=User.objects.get(email=request.session['email'])
     Wishlist.objects.create(user=user,product=product)
     return redirect('wishlist')

def wishlist(request):
     user=User.objects.get(email=request.session['email'])
     wishlists=Wishlist.objects.filter(user=user)
     return render(request,'wishlist.html',{'wishlists':wishlists})

def remove_wishlist(request,pk):
     user=User.objects.get(email=request.session['email'])
     product=Product.objects.get(pk=pk)
     wishlists=Wishlist.objects.get(user=user,product=product)
     wishlists.delete()
     return redirect('wishlist')


def add_to_cart(request,pk):
     product=Product.objects.get(pk=pk)
     user=User.objects.get(email=request.session['email'])
     Cart.objects.create(user=user,product=product,product_price=product.product_price,product_qty=1,total_price=product.product_price)
     return redirect('cart')

def  cart(request):
     net_price=0
     user=User.objects.get(email=request.session['email'])
     carts=Cart.objects.filter(user=user,payment_status=False)
     for i in carts:
          net_price+=i.total_price
     return render(request,'cart.html',{'carts':carts,'net_price':net_price})

def remove_cart(request,pk):
     user=User.objects.get(email=request.session['email'])
     product=Product.objects.get(pk=pk)
     carts=Cart.objects.get(user=user,product=product)
     carts.delete()
     return redirect('cart')


def carts(request):
     net_price=0
     user=User.objects.get(email=request.session['email'])
     carts=Cart.objects.filter(user=user,payment_status=False)
     for i in carts:
          net_price+=i.total_price
     return render(request,'cart1.html',{'carts':carts,'net_price':net_price})

def change_qty(request,pk):
     cart=Cart.objects.get(pk=pk)
     product_qty=int(request.POST['product_qty'])
     cart.product_qty=product_qty
     cart.total_price=cart.product_price*product_qty
     cart.save()
     return redirect('cart')
          
def change_qtys(request,pk):
     carts=Cart.objects.get(pk=pk)
     product_qty=int(request.POST['product_qty'])
     carts.product_qty=product_qty
     carts.total_price=carts.product_price*product_qty
     carts.save()
     return redirect('carts')
                    


@csrf_exempt
def create_checkout_session(request):
    net_price = int(json.load(request)['post_data'])
    final_price=net_price*100
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user,payment_status=False)
    print("First Name : ",user.fname)
    for i in carts:
        i.payment_status=True
        i.save()
    user_name=f"{user.fname} {user.lname}"
    user_messgae=f"{user.message}"
    user_phone=f"{user.phone}"
    session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'unit_amount': final_price,
				'product_data': {
					'name': 'Checkout Session Data',
					'description':f'''Customer:{user_name},\n\n
					Messgae:{user_messgae},\n
					Phone:{user_phone}''',
				},
			},
			'quantity': 1,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success',
		cancel_url=YOUR_DOMAIN + '/cancel',
		customer_email=user.email,
		shipping_address_collection={
			'allowed_countries':['IN'],
		}
		)
    return JsonResponse({'id': session.id})

def success(request):
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user,payment_status=False)
    request.session['cart_count']=len(carts)
    return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

def myorder(request):
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user,payment_status=True)
    return render(request,'myorder.html',{'carts':carts})
