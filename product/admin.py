from django.contrib import admin
from .models import Category, City, District, Estate, Image


admin.site.register(Category)
admin.site.register(City)
admin.site.register(District)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 3
    fields = ['image']
    max_num = 10


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [ImageInline]
