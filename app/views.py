from django.shortcuts import render,redirect
from app.models import User,Book,Cart,Rating,Category,Report
from django.db.models import Avg

# Create your views here.
def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        fullname = request.POST.get('fullname')
        age =request.POST.get('age')

        user = User()
        user.username = username
        user.password = password
        user.fullname = fullname
        user.age = age

        user.save()
        return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.fullname
            request.session['is_admin'] = user.is_admin
            return redirect('/')
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def home(request):
    search =request.GET.get('search', '')
    user = request.session.get('user_name')
    if search:
        books = Book.objects.filter(
            is_active=True,
            is_blocked=False,
            name__icontains=search
        ).annotate(
            avg_rating=Avg('rating__rating')
        )
        return render(request, 'home.html', {"books": books, "user":user})
    books = Book.objects.filter(
                is_active=True,
                is_blocked=False,
            ).annotate(
                avg_rating=Avg('rating__rating')
            )
    return render(request, 'home.html', {"books": books, "user":user})

def book_view(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'book-view.html', {'book':book})
    
def cart(request):
    user = request.session.get('user_id')
    if user:
        cart = Cart.objects.filter(user=user, is_deleted=False)
        return render(request, 'cart.html', {'cart_items':cart})
    return redirect('/login/')

def add_to_cart(request):
    user = request.session.get('user_id')
    if not user:
        return redirect('/login')
    
    book = request.POST.get('book')
    cart = Cart()
    cart.user = User.objects.get(id=user)
    cart.book = Book.objects.get(id=book)
    cart.save()
    return redirect('/cart/')

def remove_from_cart(request, id):
    item = Cart.objects.get(id=id)
    item.is_deleted = True
    item.save()
    return redirect('cart')

def rating(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login')

    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        book_id = request.POST.get('book_id')

        Rating.objects.update_or_create(
                user=user_id,
                book=book_id,
                defaults={'rating': int(rating_value)}
            )
        
    return redirect('/')


def add_book(request):
    user = request.session.get('user_id')
    categories = Category.objects.all()
    if not user:
        return redirect('/login/')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        file = request.FILES.get('file')

        book = Book()
        book.name = name
        book.description = description
        book.category = Category.objects.get(id=category)
        book.price = price
        book.image = image
        book.file = file
        book.author = User.objects.get(id=user)

        book.save()
        return redirect('/')
    
    return render(request, 'add-book.html', {'category':categories})
def update_book(request, id):
    user = request.session.get('user_id')

    if not user:
        return redirect('/login/')

    book = Book.objects.get(id=id, author_id=user)
    categories = Category.objects.all()

    if request.method == 'POST':

        book.name = request.POST.get('name')
        book.description = request.POST.get('description')

        category_id = request.POST.get('category')
        book.category = Category.objects.get(id=category_id)

        book.price = request.POST.get('price')

        if request.FILES.get('image'):
            book.image = request.FILES.get('image')

        if request.FILES.get('file'):
            book.file = request.FILES.get('file')

        book.save()

        return redirect('/profile/')

    return render(request, 'book-update.html', {
        'book': book,
        'category': categories
    })


def profile(request):
    user = request.session.get('user_id')
    if not user:
        return redirect('/login/')
    user_name = request.session.get('user_name')
    books=Book.objects.filter(author=user)
    total_books= Book.objects.filter(author=user).count()
    active_books= Book.objects.filter(author=user, is_active=True).count()
    blocked_books= Book.objects.filter(author=user, is_blocked=True).count()
    reports = Report.objects.filter(book__author=user)
    return render(request, 'profile.html', {
        'books':books, 
        'user':user_name,
        'total_books':total_books,
        'active_books':active_books,
        'blocked_books':blocked_books,
        'reports':reports
    })

# def report(request):
#     user = request.session.get('user_id')
#     if not user:
#         return redirect('/login/')
#     reports = Report.objects.filter(book__author=user)
#     return render()