from django.contrib import admin
from . import models

# Register your models here.

# Table Category
admin.site.register(models.Category)

# Table Product
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


# Table ProductInventory
@admin.register(models.ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'upc', 'is_active', 'is_default', 'sale_price', 'quantity')
    list_editable = ('is_default', 'is_active', 'sale_price')
    list_filter = ('is_active', 'sale_price', 'quantity')


# Table Brand
admin.site.register(models.Brand)


# Table Media
@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'alt_text', 'is_feature')
    list_editable = ('is_feature',)
    list_filter = ('is_feature',)


# Table ProductAttributeValue
admin.site.register(models.ProductAttributeValue)


admin.site.register(models.BestSellingProducts)
