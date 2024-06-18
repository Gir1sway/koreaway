from django.contrib import admin

from home.models import Category, Product, Cart, CartItem, OrderItem, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'phone', 'confirmed')
    list_filter = ('confirmed', 'created_at')
    search_fields = ('user__username', 'first_name', 'last_name')
    inlines = [OrderItemInline]
    actions = ['confirm_orders']

    def confirm_orders(self, request, queryset):
        queryset.update(confirmed=True)

    confirm_orders.short_description = "Confirm selected orders"


admin.site.register(Order, OrderAdmin)
