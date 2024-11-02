from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from .forms import signupForm
from django.contrib import messages
from .models import Game,Publisher,Cart,CartItem,Order,OrderItem,Category,WishList,WishListItem,Library,LibraryItem
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def home(request):
    from django.shortcuts import render
from .models import Game, Category

def home(request):
    categories = Category.objects.all()
    
    featured_games = Game.objects.filter(featured=True)[:6]  # Show top 6 featured games
    
    context = {
        'categories': categories,
        'featured_games': featured_games,
    }
    
    return render(request, 'gameApp/home.html', context)


def user_register(request):
    if request.method == "POST":
        form = signupForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']

            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"Registration successful.")
                return redirect('home')
        else:
            messages.success(request,"Please register again. Error occured.")
            return redirect('user-register')
    else:
        form = signupForm()
        return render(request,'gameApp/register.html',{"form":form})
        

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged in.")
            return redirect('home')
        else:
            messages.success(request,"Login failed. Please try again.")
            return redirect('user-login')
    else:
        return render(request,'gameApp/login.html',{})

def user_logout(request):
    logout(request)
    messages.success(request,"Successfully logged out.")
    return redirect('user-login')

def games(request):
    games = Game.objects.all()
    return render(request,'gameApp/games.html',{"games":games})

def publishers(request):
    publishers = Publisher.objects.all()
    
    publishers_with_games = {
        publisher: Game.objects.filter(publisher=publisher) for publisher in publishers
    }
    
    context = {
        'publishers_with_games': publishers_with_games,
    }
    return render(request, 'gameApp/publishers.html', context)

def custom_game(request, game_title):
    game = get_object_or_404(Game, title=game_title)
    categories = game.categories.all()
    
    items_in_cart = []
    items_in_wishlist = []
    is_bought = False
    if request.user.is_authenticated:
        library,created = Library.objects.get_or_create(user=request.user)
        cart, created = Cart.objects.get_or_create(user=request.user)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        items_in_cart = CartItem.objects.filter(cart=cart).values_list('product__id', flat=True)
        items_in_wishlist = WishListItem.objects.filter(wishlist=wishlist).values_list('product__id', flat=True)
        
        if LibraryItem.objects.filter(library=library,game=game).exists():
            is_bought = True

    is_wishlisted = game.id in items_in_wishlist

    return render(request, 'gameApp/custom_game.html', {
        "game": game,
        "items": items_in_cart,
        "categories": categories,
        "wishlisted": is_wishlisted,
        "bought":is_bought,
    })


def custom_publisher(request,publisher_name):
    publisher = Publisher.objects.get(name=publisher_name)
    return render(request,'gameApp/custom_publisher.html',{"publisher":publisher})

@login_required(login_url="/login")
def cart(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    
    total_price = sum(item.product.price * item.quantity for item in items)  # Calculate total price

    return render(request, 'gameApp/cart.html', {
        "items": items,
        "total_price": total_price  
    })


@login_required(login_url="/login")
def add_to_cart(request,game_title):
    game_product = get_object_or_404(Game,title=game_title)
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_item,created = CartItem.objects.get_or_create(cart=cart,product=game_product)

    wishlist, _ = WishList.objects.get_or_create(user=request.user)
    wishlist_item = WishListItem.objects.filter(wishlist=wishlist, product=game_product)
    if wishlist_item.exists():
        wishlist_item.delete()
    
    if not created:
        cart_item.quantity+=1
        cart_item.save()

    
    return redirect('custom-game', game_title=game_title)

def remove_from_cart(request,game_title):
    game_product = Game.objects.get(title=game_title)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart,product=game_product).delete()

    messages.success(request,"Item successfully removed.")
    return redirect('cart')

@login_required(login_url="/login")
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,'gameApp/orders.html',{"orders":orders})

@login_required(login_url="/login")
def order_add(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    if items.exists(): 
        order = Order.objects.create(user=request.user)
        library, _ = Library.objects.get_or_create(user=request.user)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,  
                price=item.product.price
            )
            if not LibraryItem.objects.filter(library=library, game=item.product).exists():
                LibraryItem.objects.create(library=library, game=item.product)
        
        items.delete()
        messages.success(request, "Order successfully placed!")
        
        
    else:
        messages.warning(request, "Your cart is empty.")
    
    return redirect('orders')

def search(request):
    if request.method == "POST":
        search_term = request.POST['searchterm']
        games = Game.objects.filter(Q(title__icontains=search_term))
        return render(request,'gameApp/search.html',{"search_term":search_term,"games":games})

def category(request,category_id):
    category = get_object_or_404(Category, id=category_id)
    games = category.games.all()
    all_categories = Category.objects.all()

    selected_category_id = request.GET.get("category")
    if selected_category_id and int(selected_category_id) != category_id:
        return redirect("categories", category_id=selected_category_id)

    return render(request, "gameApp/category.html", {
        "category": category,
        "games": games,
        "all_categories": all_categories
    })
@login_required(login_url="/login")
def wishlist_detail(request):
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    items = wishlist.items.all()
    return render(request,"gameApp/wishlist.html",{'wishlist': wishlist, 'items': items})

@login_required(login_url="/login")
def add_to_wishlist(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    WishListItem.objects.get_or_create(wishlist=wishlist, product=game)

    return redirect('custom-game' ,game_title=game.title) 

@login_required(login_url="/login")
def remove_from_wishlist(request, game_id):
    game = get_object_or_404(Game,id=game_id)
    wishlist = get_object_or_404(WishList,user=request.user)
    wishlist_item = get_object_or_404(WishListItem,wishlist=wishlist,product=game)
    wishlist_item.delete()

    return redirect('wishlist-detail') 

@login_required(login_url="/login")
def library_view(request):
    library = Library.objects.filter(user=request.user).first()
    
    if library:
        library_items = library.items.select_related('game') 

        context = {
            'library_items': library_items,
        }
    else:
        context = {
            'library_items': [],
        }
    
    return render(request, 'gameApp/library.html', context)

@login_required(login_url="/login")
def add_to_library(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    library, created = Library.objects.get_or_create(user=request.user)
    
    if not LibraryItem.objects.filter(library=library, game=game).exists():
        LibraryItem.objects.create(library=library, game=game)
    
    return redirect('home')  