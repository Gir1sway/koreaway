from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .forms import OrderForm, ContactForm


class HomePageView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_selling_products = Product.objects.annotate(num_cart_items=Count('cartitem')).order_by('-num_cart_items')[:2]
        for product in top_selling_products:
            product.description_lines = product.description.split('\n')
        context['top_selling_products'] = top_selling_products
        return context


class ProductListView(ListView):
    template_name = 'home/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        context['contact_form'] = ContactForm()
        return context

    def get_queryset(self):
        self.category = None
        self.products = Product.objects.all()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            self.products = self.products.filter(category=self.category)
        return self.products

    def post(self, request, *args, **kwargs):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['message']

            send_mail(
                f"Новое сообщение от {name}",
                message,
                email,
                ['azaliyakad@gmail.com'],
                fail_silently=False,
            )

            return redirect('product_list')

        return self.get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'home/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['product'].image:
            context['product'].image = 'path/to/default/image.jpg'
        return context


class CartView(View):
    template_name = "home/cart.html"

    @method_decorator(login_required)
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        return render(request, self.template_name, {'cart': cart, 'total_price': total_price})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')


def search(request):
    query = request.GET.get('q')
    product_results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.none()
    context = {
        'query': query,
        'product_results': product_results,
    }
    return render(request, 'home/search_results.html', context)


class UserProfileDetailView(DetailView):
    model = User
    template_name = 'home/user_profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        return self.request.user


class AboutView(TemplateView):
    template_name = 'home/about.html'


class CheckoutView(View):
    template_name = "home/checkout.html"

    @method_decorator(login_required)
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        form = OrderForm()
        return render(request, self.template_name, {'cart': cart, 'total_price': total_price, 'form': form})

    @method_decorator(login_required)
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart.cartitem_set.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            cart.delete()
            return redirect('order_success')
        total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        return render(request, self.template_name, {'cart': cart, 'total_price': total_price, 'form': form})

class OrderSuccessView(TemplateView):
    template_name = "home/order_success.html"
