from django.contrib import admin
from Store.models import *
from django.utils.html import format_html

class SizeVariantConfiguration(admin.TabularInline):
    model = SizeVariant

class TshirtConfiguration(admin.ModelAdmin):
    inlines = [SizeVariantConfiguration]

class CartConfiguration(admin.ModelAdmin):
    model = Cart
    list_display = ['quantity','size','tshirt','user','username']
    fieldsets = (
        ('Cart Info',{'fields':('user','get_sizeVariant','quantity','get_tshirt')}),
    )
    readonly_fields = ('quantity','user','get_sizeVariant','get_tshirt')

    def get_tshirt(self,obj):
        tshirt = obj.sizeVariant.tshirt
        tshirt_id = tshirt.id
        name = tshirt.name
        return format_html(f'<a href="/admin/Store/tshirt/{tshirt_id}" target="_blank">{name}</a>')
    get_tshirt.short_description = 'Tshirt'

    def get_sizeVariant(self,obj):
        return obj.sizeVariant.size
    get_sizeVariant.short_description = 'Size'

    def size(self,obj):
        return obj.sizeVariant.size
    
    def tshirt(self,obj):
        return obj.sizeVariant.tshirt.name
    
    def username(self,obj):
        return obj.user.first_name

# Register your models here.
admin.site.register(Tshirt, TshirtConfiguration)
admin.site.register(Occasion)
admin.site.register(NeckType)
admin.site.register(IdealFor)
admin.site.register(Brand)
admin.site.register(Sleeve)
admin.site.register(Color)
admin.site.register(SizeVariant)
admin.site.register(Cart,CartConfiguration)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)