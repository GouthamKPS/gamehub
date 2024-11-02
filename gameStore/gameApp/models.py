from django.db import models
from django.contrib.auth.models import User

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    rating = models.PositiveIntegerField(default=0)
    price = models.IntegerField()
    publisher = models.ForeignKey(Publisher,on_delete = models.CASCADE,related_name="games")
    size = models.PositiveIntegerField(default=0)
    about = models.TextField(default="")
    image = models.TextField(blank=True,null=True)
    categories = models.ManyToManyField(Category,related_name="games")
    featured = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"The cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Game,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in {self.cart}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('P','Pending'),
        ('C','Completed'),
        ('F','Failed'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='C')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Game,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in Order {self.order.id}"

class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"


class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Game, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} in {self.wishlist}"

class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='libraries')

    def __str__(self):
        return f"{self.user.username}'s library"
        
class LibraryItem(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)  
    playtime = models.IntegerField(default=0)  

    class Meta:
        unique_together = ('library', 'game')

    def __str__(self):
        return f"{self.library.user.username}'s item: {self.game.title}"
