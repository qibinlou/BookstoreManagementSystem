#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect ,HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from  books.models import *
from django.db.models import Q
import datetime
from django.core.context_processors  import *
import django.contrib.auth.context_processors
from django.template import RequestContext
import json



def homepage(request):
    head = 'Book Company Management Website'
    title = 'HomePage'
    user = request.user.username
    return render_to_response('base.html', locals())


def login(request):
    c = {}
    c.update(csrf(request))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page
        return  HttpResponseRedirect("/home/",)
    else:
        # Show an error page
        return render_to_response('login.html',{"error":True,"csrf_token":c['csrf_token']})

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/home/")

   
def home(request):
    
    # fixed vars #
    title = 'Welome to Excurtion'
    user = request.user.username
    return render_to_response('base.html',locals())



@login_required(login_url="/home/login/")
def  order(request):
    title = "Order"
    user = request.user.username
    if 'type' in request.GET and request.GET['type']:
        order_type = request.GET['type']
        if order_type == "In":
            state = '0'
        else:
            state = '1'
        p = Order()
        p.order_date = datetime.datetime.now()
        p.order_type = state
        p.operator = user
        p.save()
        return HttpResponse(p.id)

    total_income = total_outgo = decimal.Decimal(0)

    Orderqueryset = Order.objects.all()
    if 'start_time' in request.GET and request.GET['start_time']:
        Orderqueryset=Orderqueryset.filter(order_date__gte=request.GET.get('start_time'))
        print "start_time",request.GET.get('start_time'),Orderqueryset.count()
    if 'end_time' in request.GET and request.GET['end_time']:
        Orderqueryset=Orderqueryset.filter(order_date__lte=request.GET.get('end_time'))
        print "end_time",request.GET['end_time'],Orderqueryset.count()
    orders = []
    for item in Orderqueryset:
        order = {}
        order["id"] = item.id
        order["date"] = item.display_order_date()
        if item.order_type == '0':
            order["type"] = "In"
        else:
            order["type"] = "Out"
        order["info"] = item.total_price().split('/')[-1].split('$')[-1 ]
        order['operator'] = item.operator
        orders.append(order)

    for order in Orderqueryset:
        if order.order_type == BUY:
            total_outgo += order.turnover()
        elif order.order_type == SELL:
            total_income += order.turnover()
    return render_to_response('order.html', locals())

@login_required(login_url="/home/login/")
def  bookorder(request):
    title = "Book Order"
    user = request.user.username

    if 'order' in request.GET and request.GET['order']:
        order_id = request.GET['order']
        order_type = Order.objects.get(id=order_id).order_type
        order_state = '0'
        for item in BookOrder.objects.filter(order__id=order_id):
            if  item.state == '1':
                order_state = '1'
                break

        print "Order Type",order_state
    else:
        return HttpResponse("Order doesn't exist!")
    books = []
    state_choices = {'0':'processing','1':'done','2':'cancled'}
    for item in BookOrder.objects.filter(order__id=order_id).order_by("state"):
        book = {}
        book["id"] = item.book_item.id
        book["number"] = item.numbers
        book["title"] = item.book_item.title
        book["price"] = item.display_price()
        book["state"] = state_choices[item.state]
        book["numbers"] = Book.objects.get(id=item.book_item.id).stock
        books.append(book)
    return render_to_response("bookorder.html",locals())


@login_required(login_url="/home/login/")
def  updateorder(request):

    if 'order' in request.GET and request.GET['order']:
        order = request.GET['order']
        order_type = Order.objects.get(id=order).order_type
        # print "updateorder",order,order_type
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
                
                if order_type == '0':
                    print "fuck you !!!!"
                    p.price = book['price']
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


@login_required(login_url="/home/login/")
def  submitorder(request):
    if 'order' in request.GET and request.GET['order']:
        order = request.GET['order']
        order_type = Order.objects.get(id=order).order_type
    else:
        return HttpResponse("Order doesn't exist!")

    books = BookOrder.objects.filter(order__id=order,state='0')
    for book in books:
        book.state = '1'
        item = Book.objects.get(id=book.book_item.id)
        if order_type == '0':
            item.stock = item.stock + book.numbers
        else:
            item.stock = item.stock - book.numbers    
        
        item.save()
        book.save()
    return HttpResponse("Submit Order Successfully!");


@login_required(login_url="/home/login/")
def  addbook(request):
    title = "Add Book"
    user = request.user.username

    if 'order' in request.GET and request.GET['order']:
        order_id = request.GET['order']
        order_type = Order.objects.get(id=order_id).order_type

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
        booklist = Book.objects.filter(Q(isbn__icontains=keyword) |  Q(title__icontains=keyword) | Q(publisher__name__icontains=keyword) | Q(authors__name__icontains=keyword) )
    else:
        booklist = Book.objects.all()


    erro = None
    # print booklist.count()
    if booklist.count() >  100 or booklist.count() == 0:
        if booklist.count() != 0:
            error = "The Resultset is too large to fetch! Please be more accurate!"
        else:
            error = "There is no such book! Please retry!"
        print error
        return render_to_response("addbook.html",locals())
    books = []
    for book in booklist:
        item = {}
        item["id"] = book.id
        if BookOrder.objects.filter(order__id=order_id,book_item__id=book.id,state='0').count() > 0:
            item["checked"] = True
            # item["number"] = BookOrder.objects.filter(order__id=order_id,book_item__id=book.id)[0].numbers
            # if item["number"]  == 0:
            #     item["checked"] = False
        # else:
        #     item["number"] = 0    
        item["isbn"] = book.isbn
        item["title"] = book.title
        item["price"] = book.display_price()
        item["numbers"] = book.stock

        item["authors"] = book.display_authors()
        item["publisher"] = book.publisher.name
        item["date"] = book.display_publication_date()
        books.append(item)


    return render_to_response("addbook.html",locals())


@login_required(login_url="/home/login/")
def book(request):
    from math import ceil

    title = "Book"
    user = request.user.username

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
    
    pagelength = 20
    page = 1
    bookcount = Book.objects.count()
    pages = int(ceil(bookcount/pagelength)) 
    if 'p' in request.GET and request.GET['p']:
        page = int(request.GET['p'])
    paginations = """
    <div class='pagination-block'>
        <div class='pagination'>
            <ul>"""
    for i in range(8,0,-1):
        if page-i > 0:
            paginations += "<li><a href='?p=%d'>%d</a></li>"%(page-i,page-i,)
    paginations += "<li class='active'><a href='?p=%d'>%d</a></li>"%(page,page)

    for i in range(1,8):
        if page+i < pages:
            paginations += "<li><a href='?p=%d'>%d</a></li>"%(page+i,page+i,)
            
    paginations += """
    </ul>
        </div>
        <div class="pagination-info muted">
           %d - %d
            of total %d
            books
    
        </div>
    </div>
        """%((page-1)*pagelength+1,page*pagelength,bookcount)
    

    booklist = Book.objects.filter(id__gt=(page-1)*pagelength,id__lte=page*pagelength)
    # booklist = Book.objects.order_by("stock","id")
    books = []
    for book in booklist:
        item = {}
        item["id"] = book.id
        item["isbn"] = book.isbn
        item["title"] = book.title
        item["price"] = book.display_price()
        item["numbers"] = book.stock
        item["authors"] = book.display_authors()
        item["publisher"] = book.publisher.name
        item["date"] = book.display_publication_date()
        item["sold"] = 0
        for bookorder in BookOrder.objects.filter(state='1',order__order_type='0',book_item__id=book.id):
            item["sold"] += bookorder.numbers
        books.append(item)

    return render_to_response("book.html",locals())

	

@login_required(login_url="/home/login/")
def account(request):
    t = loader.get_template('account.html')
    start_time = request.GET.get('start_time')
#    start_time = datetime.datetime(2006, 11, 21, 16, 30)
    end_time = request.GET.get('end_time')
    total_income = total_outgo = decimal.Decimal(0)
#    end_time = datetime.datetime.now()
    print Order.objects.filter(order_date__gte=start_time, order_date__lte=end_time).count()
    for order in Order.objects.filter(order_date__gte=start_time, order_date__lte=end_time):
        if order.order_type == BUY:
            total_outgo += order.turnover()
        elif order.order_type == SELL:
            total_income += order.turnover()
    return render_to_response('account.html', locals())









# importbooks

def importbooks(request):
    from django.core.files import File
    import os
    import urllib
    import urllib2
    from os.path import *
    from random import randint

    

    fp = file(os.path.join(os.path.dirname(__file__),"static/files/booklist.txt"))
    # print os.path.join(os.path.dirname(__file__),"/static/files/booklist.txt")
    myfile = File(fp)
    # query_args = {'alt':'json'}
    count = 0
    for isbn in myfile:
        
        # count += 1
        # if count > 10:
        #     break
        print "isbn: ",isbn
        try:
            url = "https://api.douban.com/v2/book/isbn/%s"%(str(isbn).strip())
            # print url
            response = urllib2.urlopen(url)

            data = json.loads(response.read())
            title = data['title']
            publisher = data['publisher']
            author = data['author'][0]
            price = float(data['price'][0:-2])
            pubdate = data['pubdate']
            if title and publisher and author and price and pubdate:
                
                stock = randint(0,100)
                if Publisher.objects.filter(name=publisher).count() == 0:
                    pass

                if Author.objects.filter(name=author).count() == 0:
                    a = Author(name=author)
                    a.save()
                if Publisher.objects.filter(name=publisher).count() == 0:
                    p = Publisher(name=publisher)
                    p.save()
                a = Author.objects.filter(name=author)
                p = Publisher.objects.get(name=publisher)
                b = Book()
                b.isbn = isbn
                b.title = title
                b.price = price
                b.publication_date = pubdate+"-10"
                b.stock = stock
                
                b.publisher = p
                b.save()
                b.authors  = a
                b.save()
            else:
                continue
            

            print title,publisher,author,price,pubdate,stock
        except Exception, e:
            print e
        else:
            pass
        finally:
            pass
        url = "http://api.douban.com/book/subject/isbn/%s/?alt=json"%(str(isbn).strip())
        
    
    myfile.close()
    fp.close()

    
    # a = Author.objects.filter(name=u'王杏元')
    # p = Publisher.objects.get(name=u'中共党史出版社')
    # b = Book()
    # b.isbn = "12121"
    # b.title = "232"
    # b.price = 23.33
    # b.publication_date = "2013-5-12"
    # b.stock = 12
    # b.author = a
    # b.publisher = p
    # b.save()
        


    print "File Closed!"
    # print "os.path:  ",os.path
    # print "os.path.dirname:  ",os.path.dirname(__file__)
    # print "os.path.abspath:  ",os.path.abspath(__file__)
    # print "os.path.join: ",os.path.join(os.path.dirname(__file__),"booklist.txt")
    return HttpResponse("Fuck you!")


