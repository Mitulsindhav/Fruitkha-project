from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('error404/',views.error404,name='error404'),
    path('shop/',views.shop,name='shop'),
    path('news/',views.news,name='news'),
    path('cart/',views.cart,name='cart'),
    path('check-out/',views.check_out,name='check-out'),
    path('single-product/',views.single_product,name='single-product'),
    path('single-news/',views.single_news,name='single-news'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('change-password/',views.change_password,name='change-password'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('new-password/',views.new_password,name='new-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('seller-index/',views.seller_index,name='seller-index'),
    path('seller-add-product/',views.seller_add_product,name='seller-add-product'),
    path('seller-view-product/',views.seller_view_product,name='seller-view-product'),
    path('seller-product-details/<int:pk>',views.seller_product_details,name='seller-product-details'),
    path('seller-edit-product/<int:pk>',views.seller_edit_product,name='seller-edit-product'),
    path('seller-delete-product/<int:pk>',views.seller_delete_product,name='seller-delete-product'),
    path('product-details/<int:pk>',views.product_details,name='product-details'),
    path('add-to-wishlist/<int:pk>',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove-wishlist/<int:pk>',views.remove_wishlist,name='remove-wishlist'),
    path('add-to-cart/<int:pk>',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('remove-cart/<int:pk>',views.remove_cart,name='remove-cart'),
    path('carts/',views.carts,name='carts'),
    path('change-qty/<int:pk>',views.change_qty,name='change-qty'),

    path('change-qtys/<int:pk>',views.change_qtys,name='change-qtys'),
 
    path('create-checkout-session/', views.create_checkout_session, name='payment'),
    path('success/', views.success,name='success'),
    path('cancel/', views.cancel,name='cancel'),
    path('myorder/', views.myorder,name='myorder'),


   

]
