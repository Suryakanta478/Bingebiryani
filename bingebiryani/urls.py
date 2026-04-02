from django.contrib import admin
from django.urls import path, include
from hotel import views
from django.contrib.sitemaps.views import sitemap

from django.contrib.sitemaps.views import sitemap
from hotel.sitemaps import StaticSitemap

sitemaps = {
    'static': StaticSitemap,
}

urlpatterns = [
    ...
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

    # Admin
    path('admin/', admin.site.urls),

    # Home / Signup
    path('', views.signup, name='signup'),
    path('home/', views.home, name='home'),

    # Authentication
    path('signup/', views.signup, name='signup'),
    path('verify-signup/', views.verify_signup, name='verify_signup'),
    path('accounts/', include('allauth.urls')),
    path('login/', views.login_user, name='login'),
    path('verify-login/', views.verify_login, name='verify_login'),
    path('logout/', views.logout_view, name='logout'),

    # OTP System
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),

    # Forgot / Reset Password
    path('forgot/', views.forgot, name='forgot'),
    path('reset/', views.reset, name='reset'),

    # User
    path('profile/', views.profile, name='profile'),

    # Hotel Features
    path('booking/', views.book_room, name='booking'),
    path('menu/', views.menu, name='menu'),
    path('party/', views.party, name='party'),
    path('room/', views.book_room, name='room'),

    # Payment
    path('payment/', views.payment, name='payment'),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path("success/", views.success, name="success"),
    path("failure/", views.failure, name="failure"),
    path('payment-history/', views.payment_history, name='payment_history'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
