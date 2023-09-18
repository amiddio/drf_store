from django.contrib import admin

from catalog.models import Category, Product, ProductUserRelation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'qty', 'active')


@admin.register(ProductUserRelation)
class ProductUserRelationAdmin(admin.ModelAdmin):
    pass
