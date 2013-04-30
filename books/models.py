from django.db import models
import datetime, decimal


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=60,blank=True)
    state_province = models.CharField(max_length=30,blank=True)
    country = models.CharField(max_length=50,blank=True)
    website = models.URLField(blank=True)
    class Meta:
        # db_table = 'Publisher'
        pass
    def __unicode__(self):
        return unicode(self.name)

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    
    def __unicode__(self):
        return unicode(self.name)


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(blank=True, null=True)
    
    price = models.DecimalField(max_digits=15,decimal_places=2)
    stock = models.PositiveIntegerField()

    def __unicode__(self):
        return unicode(self.title) 

    def  display_authors(self):
        return ' / '.join([a.name for a in self.authors.all() ])
    display_authors.short_description = 'authors'

PROCESSING = '0'
DONE = '1'
CANCELED = '2'
BUY = '0'
SELL = '1'
class Order(models.Model):
    ORDER_CHOICES = ((BUY,'buy'),(SELL,'sell'))
    order_date = models.DateTimeField(default=datetime.datetime.now())
    order_type = models.CharField(max_length=1, choices=ORDER_CHOICES)
    def total_price(self):
        paid = pending = decimal.Decimal(0)
        for item in BookOrder.objects.filter(order__id = self.id):
            if item.state == PROCESSING:
                pending += item.total_price()
            elif item.state == DONE:
                paid += item.total_price()
        return '$%.2f / $%.2f' %(pending, paid)
    total_price.short_description = 'pending / paid'
    def __unicode__(self):
        return unicode(self.id)


class BookOrder(models.Model):
    STATE_CHOICES = ((PROCESSING,'processing'),(DONE,'done'),(CANCELED,'canceled'))
    order = models.ForeignKey(Order)
    book_item = models.ForeignKey(Book)
    price = models.DecimalField(max_digits=15,decimal_places=2,blank=False, default=-1)
    numbers = models.PositiveIntegerField()
    state = models.CharField(blank=False,default='0',max_length=1,choices=STATE_CHOICES)
    def save(self, *args, **kwargs):
        if self.price == -1:
            self.price = self.book_item.price
        super(BookOrder, self).save(*args, **kwargs)
    def total_price(self):
        return self.price * self.numbers
    def total_price_display(self):
        paid = pending = decimal.Decimal(0)
        if self.state == PROCESSING:
            paid, pending = 0, self.total_price()
        elif self.state == DONE:
            paid, pending = self.total_price(), 0
        elif self.state == CANCELED:
            paid, pending = 0, 0
        return '$%.2f / $%.2f' %(pending, paid)
    total_price_display.short_description = 'pending / paid'
    def str_total_price(self):
        return '$%.2f' %self.price * self.numbers
    def __unicode__(self):
        return unicode(self.order)

