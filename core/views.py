from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignupForm
from django.contrib.auth import logout


def index(request):
    items = Item.objects.all()
    item1 = Item.objects.filter(featured=True).filter(is_sold=False)
    categories = Category.objects.all()
    return render(request, 'item/items.html', {
        'categories': categories,
        'items': items,
        'item1': item1,
    })

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

def term(request):
    return render(request, 'core/term.html')

def logout_view(request):
    logout(request)
    return redirect('core:index')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })