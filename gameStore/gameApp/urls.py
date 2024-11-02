from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('games/',views.games,name="games"),
    path('publishers/',views.publishers,name="publishers"),
    path('login/',views.user_login,name="user-login"),
    path('logout/',views.user_logout,name="user-logout"),
    path('register/',views.user_register,name="user-register"),
    path('games/<str:game_title>',views.custom_game,name="custom-game"),
    path('publishers/',views.custom_publisher,name="custom-publisher"),
    path('cart/',views.cart,name="cart"),
    path('cart/add/<str:game_title>',views.add_to_cart,name="add-to-cart"),
    path('cart/remove/<str:game_title>',views.remove_from_cart,name="remove-from-cart"),
    path('orders/',views.orders,name="orders"),
    path('orders/add',views.order_add,name="order-add"),
    path('search/',views.search,name="search"),
    path('categories/<int:category_id>/',views.category,name='categories'),
    path('wishlist/',views.wishlist_detail,name="wishlist-detail"),
    path('wishlist/add/<int:game_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:game_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('library/',views.library_view,name="library-view"),
    path('library/add/<int:game_id>',views.add_to_library,name="add-to-library"),

    

]