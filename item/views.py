from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import NewItemForm, EditItemForm, ReviewForm
from .models import Category, Item, Review

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    price_order = request.GET.get('price_order', '')
    items = Item.objects.filter(is_sold=False).order_by('-created_at','-featured', 'name')
    # item1 = Item.objects.filter(featured=True).filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if price_order == 'asc':
        items = items.order_by('price')
    elif price_order == 'desc':
        items = items.order_by('-price')

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        # 'item1': item1,
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    reviews = Review.objects.filter(item=item).order_by('-time')[:6]
    review_count = reviews.count()
    stars = range(1, 6)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            return redirect('item:detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'reviews': reviews,
        'form': form,
        'stars': stars,
        'review_count': review_count,
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
        form.fields['category'].queryset = Category.objects.all()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })



@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.pk)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect(reverse('dashboard:index'))

def all_reviews(request,pk):
    item = get_object_or_404(Item, pk=pk)
    reviews = Review.objects.filter(item=item).order_by('-time')
    stars = range(1, 6)
    return render(request, 'item/reviews.html', {'reviews': reviews,'stars': stars,})
