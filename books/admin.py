from django.contrib import admin
from books.models import *

class PublisherAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'city','state_province','country','website')
	list_filter =  ('name', 'address', 'city','state_province','country','website')
	search_fields = ('name', 'address', 'city','state_province','country','website')
	# filter_horizontal = ('authors',)

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'email')
	list_filter =  ('name', 'email')
	search_fields = ('name', 'email')
	# filter_horizontal = ('authors',)

class BookAdmin(admin.ModelAdmin):
	list_display = ('book_id','isbn','title','display_authors','publisher','publication_date','price','numbers')
	list_filter =  ('book_id','isbn','title','publisher','publication_date',)
	search_fields = ('book_id','isbn','title','publisher')
	# filter_horizontal = ('authors',)
		
class Book_OrderInline(admin.TabularInline):
    model = BookOrder
    extra = 0
	
class BookInfoAdmin(admin.ModelAdmin):
	list_display = ('book','price','numbers')
	list_filter =  ('book','price','numbers')
	search_fields = ('book','price','numbers')
	# filter_horizontal = ('authors',)

def make_order_done(modeladmin, request, queryset):
    for big_order in queryset:
        for book_order in BookOrder.objects.filter(order__id = big_order.id):
            book_order.state = DONE
            book_order.save()
make_order_done.short_description = "Mark selected orders as done."


def make_order_canceled(modeladmin, request, queryset):
    for big_order in queryset:
        for book_order in BookOrder.objects.filter(order__id = big_order.id):
            book_order.state = CANCELED
            book_order.save()
make_order_canceled.short_description = "Mark selected orders as canceled."


class OrderAdmin(admin.ModelAdmin):
	list_display = ('id','total_price', 'order_type','order_date')
	list_filter =  ('id','order_date','order_type',)
	search_fields = ('id','order_date','order_type',)
	inlines = [Book_OrderInline]
	actions = [make_order_done]
	actions += [make_order_canceled]
	# filter_horizontal = ('authors',)


def make_bookorder_done(modeladmin, request, queryset):
    for book_order in queryset:
         book_order.state = DONE
         book_order.save()
make_bookorder_done.short_description = "Mark selected book orders as done."


def make_bookorder_canceled(modeladmin, request, queryset):
    for book_order in queryset:
        book_order.state = CANCELED
        book_order.save()
make_bookorder_canceled.short_description = "Mark selected book orders as canceled."




class BookOrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'order','price','numbers','total_price_display','state',)
	list_filter  =  ('state',)
	search_fields = ('id', 'order','price','numbers','state',)
	actions = [make_bookorder_done, make_bookorder_canceled]
	# filter_horizontal = ('authors',)





admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(BookOrder,BookOrderAdmin)

