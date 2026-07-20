from django.shortcuts import render, get_object_or_404, redirect
from app.models import Category, Product, Comment
from app.forms import CommentModelForm, OrderModelForm
from django.contrib import messages
from django.db.models import Q, Avg

def home(request, category_id=None):
    categories = Category.objects.all()
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
        
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    sort_by = request.GET.get('sort')
    if sort_by == 'expensive':
        products = products.order_by('-price') 
    elif sort_by == 'cheap':
        products = products.order_by('price')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('comments__rating')).order_by('-avg_rating')
        
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'app/home.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating', 1)  
        message = request.POST.get('message')
        file = request.FILES.get('file')  

        Comment.objects.create(
            name=name,
            email=email,
            rating=int(rating),
            message=message,
            file=file,
            product=product  
        )
        
        return redirect('detail', pk=product.pk)

    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'app/detail.html', context)


def add_comment(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    if request.method == 'POST':
        print("POST ma'lumotlari:", request.POST)
        form = CommentModelForm(request.POST, request.FILES)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            
            parent_id = request.POST.get('parent')
            if parent_id:
                parent_obj = Comment.objects.filter(id=parent_id).first()
                if parent_obj:
                    if parent_obj.parent is None or parent_obj.parent.parent is None:
                        comment.parent = parent_obj
            
            comment.save()
            print("URAA! Sharh muvaffaqiyatli saqlandi.")
            return redirect('detail', pk=pk)
        else:
            print("FORM XATOLIKLARI:", form.errors.as_data())
            
    return redirect('detail', pk=pk)


def order_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.stock < order.quantity:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Buyurtmalar soni Skladdagi productlar sonidan ortiq"
                )
                print('-----------------')
            else:
                product.stock -= order.quantity
                product.save()
                order.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"{order.id} Buyurtma muvaffaqiyatli amalga oshirildi."
                )
                print('++++++++++++++')
        else:
            messages.error(request, "Telefon raqamini to'g'ri kiriting: +998XXXXXXXXX")

    return redirect('detail', pk=pk)
