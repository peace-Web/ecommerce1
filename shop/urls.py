from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.home, name="home"),
    path("description/<str:id>/", views.description, name="description"),
    path("addtocart", views.addcart, name="addcart"),
    path("cartview", views.cartview, name="cartview"),
    path("deleteitem", views.deleteitem, name="deleteitem"),
    path("checkout", views.checkout, name="checkout"),
    path("placeorder", views.placeorder, name="placeorder"),


    path("register", views.register, name="register"),
    path("loginpage", views.loginpage, name="login"),
    path("logOut", views.logOut, name="logOut"),


    path("search", views.search, name="search"),
    path("getproductsnames", views.getproducts, name="getproducts"),


    path("dashboard", views.dashboard, name="dashboard"),
    path("editprofile", views.editprofile, name="editprofile")
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)