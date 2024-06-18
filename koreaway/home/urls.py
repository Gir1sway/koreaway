from django.conf.urls.static import static
from django.urls import path
from Computer_market import settings
from .views import ProductListView, ProductDetailView, CartView, add_to_cart, remove_from_cart, search, \
    UserProfileDetailView, AboutView, HomePageView, CheckoutView, OrderSuccessView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('list/', ProductListView.as_view(), name='product_list'),
    path('about/', AboutView.as_view(), name='about'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('search/', search, name='search'),
    path('user/<int:pk>/', UserProfileDetailView.as_view(), name='user-detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-success/', OrderSuccessView.as_view(), name='order_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
