from . import views

from django.urls import path

urlpatterns = [

    
# path("",views.lp.as_view(),name="lp"),
    # path('login',views.LoginInterfaceView.as_view(),name='login'),
    path("",views.LoginInterfaceView.as_view(),name='login'),
    path("",views.LogoutInterfaceView.as_view(),name='logout'),
    path('signup',views.SignupView.as_view(),name='signup'),
    path("h",views.home,name="home"),
    path("wallet",views.wallet, name="wallet"),
    path("wallet/<str:wallet>", views.wallet_detail, name ="wallet-detail"),
    path("wallet/<str:wallet>/transactions",views.wallet_transactions,name ="wallet_transactions"),
    path("blogs/",views.blogs, name="blogs"),
    path("qrcode/",views.qrcode, name="qrcode"),
    path("regex",views.regex,name = "regex"),



    
]