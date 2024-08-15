"""
URL configuration for ekart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", views.index),  
    path("base/", views.base),  
    path("about/", views.about),  
    path("contact/", views.contact),  
    path("register/", views.register),  
    path("login/", views.user_login),  
    path("logout/", views.logout),  
    path("place_order/", views.place_order),  
    path("product_detail/<pid>", views.product_detail),
    path("",views.product),
    path("catfilter/<cv>",views.catfilter),
    path("sort/<sv>",views.sort_price),
    path("filterbyprice/",views.filterbyprice, name='search'),
    path("cart/<pid>",views.cart),
    path("viewcart/",views.view_cart),
    path("remove/<cid>",views.remove),
    path("updateqty/<x>/<cid>",views.updateqty),
    path("placeorder/",views.placeorder),
    path("fetchorder/",views.fetchorder),
    path("makepayment/",views.makepayment),
    path('paymentsuccess/',views.paymentsuccess)
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
