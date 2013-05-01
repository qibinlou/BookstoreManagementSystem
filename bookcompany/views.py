from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect ,HttpResponse
from  books.models import *
from django.db.models import Q
import datetime
import json


def homepage(request):
    head = 'Book Company Management Website'
    title = 'HomePage'
    return render_to_response('base.html', locals())


def home(request):
	
	# fixed vars #
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/admin/")
	title = 'Welome to Excurtion'

	# conditions #
	if 'neworder' in request.GET:
		p = Order(order_date=datetime.datetime.now(),order_type='0')
		p.save()
		order  = p.id
		booklist = Book.objects.all()
	else:
		if 'order' in request.GET and request.GET['order']:
			order = request.GET['order']
		else:
			order = 0
			# order = Order.objects.filter(order_type='0')[0].id
		if 'keyword' in request.GET and request.GET['keyword']:
			keyword = request.GET['keyword']
			booklist = Book.objects.filter(Q(isbn__icontains=keyword) |  Q(title__icontains=keyword)   )
		else:
			booklist = Book.objects.all()

	books = []
	for book in booklist:
		item = {}
		item["id"] = book.id
		if BookOrder.objects.filter(order__id=order,book_item__id=book.id).count() > 0:
			item["checked"] = True
			item["number"] = BookOrder.objects.filter(order__id=order,book_item__id=book.id)[0].numbers
		else:
			item["number"] = 0	
		item["isbn"] = book.isbn
		item["title"] = book.title
		item["price"] = book.price
		item["numbers"] = book.stock

		item["authors"] = book.display_authors()
		item["publisher"] = book.publisher.name
		item["date"] = book.display_publication_date()
		books.append(item)

	# return HttpResponseRedirect("/home/") 
	return render_to_response('home.html',locals())


def  order(request):
	title = "Order"
	if 'type' in request.GET and request.GET['type']:
		order_type = request.GET['type']
		if order_type == "In":
			state = '0'
		else:
			state = '1'
		p = Order()
		p.order_date = datetime.datetime.now()
		p.order_type = state
		p.save()

	orders = []
	for item in Order.objects.all():
		order = {}
		order["id"] = item.id
		order["date"] = item.display_order_date()
		if item.order_type == '0':
			order["type"] = "In"
		else:
			order["type"] = "Out"
		order["info"] = item.total_price().split('/')[-1].split('$')[-1	]
		orders.append(order)
	return render_to_response("order.html",locals())
	# return HttpResponse("order")

def  bookorder(request):
	title = "Book Order"
	if 'order' in request.GET and request.GET['order']:
		order_id = request.GET['order']
	else:
		return HttpResponse("Order doesn't exist!")
	books = []
	state_choices = {'0':'processing','1':'done','2':'cancled'}
	for item in BookOrder.objects.filter(order__id=order_id).order_by("state"):
		book = {}
		book["id"] = item.book_item.id
		book["number"] = item.numbers
		book["title"] = item.book_item.title
		book["price"] = item.price
		book["state"] = state_choices[item.state]
		book["numbers"] = Book.objects.get(id=item.book_item.id).stock
		books.append(book)
	return render_to_response("bookorder.html",locals())

def  updateorder(request):

	if 'order' in request.GET and request.GET['order']:
		order = request.GET['order']
	else:
		return HttpResponse("Order doesn't exist!")
	if  'bookorder' in request.GET and request.GET['bookorder']:
		bookorder = json.loads(request.GET['bookorder'])
	else:
		return HttpResponse("Bookorder doesn't exist!")

	# text = ""
	for book in bookorder:
		ps = BookOrder.objects.filter(order__id=order,book_item__id=book['id'])
		print ps
		if ps.count() > 0:
			for p in ps:
				if p.state == '1':
					continue
				if book['state'] == True and p.state == '2':
					p.state = '0'

				if  book['numbers'] == 0  or book['state'] == False:
					p.state =  '2'
					p.numbers = 0
					print "Bookorder",book['numbers'],p.state
				else :
					p.numbers = book['numbers']
				
				p.save()
		
		else:
			p = BookOrder()
			p.order = Order.objects.get(id=order)
			p.book_item = Book.objects.get(id=book['id'])
			p.numbers = book['numbers']
			p.state = '0'
			# p = BookOrder(order__id=order,state='0',book_item__id=book['id'],numbers=book['numbers'])
			p.save()
			# text += "out "

	return HttpResponse("Update Success!")

def  submitorder(request):
	if 'order' in request.GET and request.GET['order']:
		order = request.GET['order']
	else:
		return HttpResponse("Order doesn't exist!")

	books = BookOrder.objects.filter(order__id=order,state='0')
	for book in books:
		book.state = '1'
		item = Book.objects.get(id=book.book_item.id)
		item.stock = item.stock - book.numbers
		item.save()
		book.save()
	return HttpResponse("Submit Order Successfully!");

def  addbook(request):
	title = "Add Book"
	if 'order' in request.GET and request.GET['order']:
		order_id = request.GET['order']
		print "OrderID",order_id
		if 'book' in request.GET and request.GET['book']:
			book_id = request.GET['book']
			state = request.GET['type']
			print order_id,book_id,state
			if state == 'true':
				if BookOrder.objects.filter(order__id=order_id,book_item__id=book_id,state='0').count() > 0:
					pass
				elif  BookOrder.objects.filter(order__id=order_id,book_item__id=book_id,state='2').count() > 0:
					BookOrder.objects.filter(order__id=order_id,book_item__id=book_id,state='2').update(state='0')
				else:
					p = BookOrder(state='0',numbers=0)
					p.order = Order.objects.get(id=order_id)
					p.book_item = Book.objects.get(id=book_id)
					p.save()
			else:
				if BookOrder.objects.filter(order__id=order_id,book_item__id=book_id,state='0').count() > 0:
					BookOrder.objects.filter(order__id=order_id,book_item__id=book_id,state='0').delete()
					BookOrder.objects.filter(order__id=order_id,book_item__id=book_id,state='2').delete()	
			# print order_id,book_id,state
			return HttpResponse("Add book Successfully!")
	else:
		return HttpResponse("Order doesn't exist!")
	if 'keyword' in request.GET and request.GET['keyword']:
		keyword = request.GET['keyword']
		booklist = Book.objects.filter(Q(isbn__icontains=keyword) |  Q(title__icontains=keyword)   )
	else:
		booklist = Book.objects.all()

	books = []
	for book in booklist:
		item = {}
		item["id"] = book.id
		if BookOrder.objects.filter(order__id=order_id,book_item__id=book.id,state='0').count() > 0:
			item["checked"] = True
			# item["number"] = BookOrder.objects.filter(order__id=order_id,book_item__id=book.id)[0].numbers
			# if item["number"]  == 0:
			# 	item["checked"] = False
		# else:
		# 	item["number"] = 0	
		item["isbn"] = book.isbn
		item["title"] = book.title
		item["price"] = book.price
		item["numbers"] = book.stock

		item["authors"] = book.display_authors()
		item["publisher"] = book.publisher.name
		item["date"] = book.display_publication_date()
		books.append(item)


	return render_to_response("addbook.html",locals())


def book(request):

	title = "Book"
	if  'isbn' in request.GET and request.GET['isbn']:
		if Book.objects.filter(isbn=request.GET['isbn']).count() == 0:
			authors = request.GET['authors']
			publisher = request.GET['publisher']
			if Author.objects.filter(name=authors).count() == 0:
				a = Author(name=authors)
				a.save()
			if Publisher.objects.filter(name=publisher).count() == 0:
				p = Publisher(name=publisher)
				p.save()
			a = Author.objects.filter(name=authors)
			p = Publisher.objects.get(name=publisher)
			b = Book()
			b.isbn = request.GET['isbn']
			b.title = request.GET['title']
			
			b.publication_date = request.GET['pubdate']
			b.price = request.GET['price']
			b.stock = request.GET['numbers']
			b.publisher_id = p.id
			b.save()
			b.authors = a
			b.publisher = p
			b.save()
		
	booklist = Book.objects.order_by("stock","id")
	books = []
	for book in booklist:
		item = {}
		item["id"] = book.id
		item["isbn"] = book.isbn
		item["title"] = book.title
		item["price"] = book.price
		item["numbers"] = book.stock
		item["authors"] = book.display_authors()
		item["publisher"] = book.publisher.name
		item["date"] = book.display_publication_date()
		item["sold"] = 0
		for bookorder in BookOrder.objects.filter(state='1',order__order_type='0',book_item__id=book.id):
			item["sold"] += bookorder.numbers
		books.append(item)

	return render_to_response("book.html",locals())