from django.contrib import admin
from .models import Game,Publisher,Cart,CartItem,Order,OrderItem,Category,WishList,WishListItem,Library,LibraryItem

admin.site.register(Game)
admin.site.register(Publisher)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(WishList)
admin.site.register(WishListItem)
admin.site.register(Library)
admin.site.register(LibraryItem)


