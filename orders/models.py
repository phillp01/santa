from django.db import models
from shop.models import Product

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    address3 = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    COUNTRY_CHOICES = (('option 1','UK'),('option 2','USA'),)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, default='UK')

    child_first_name = models.CharField(max_length=50)
    child_last_name = models.CharField(max_length=50)
    child_address = models.CharField(max_length=250)
    child_address2 = models.CharField(max_length=250, blank=True, null=True)
    child_address3 = models.CharField(max_length=250, blank=True, null=True)
    child_postal_code = models.CharField(max_length=20)
    child_city = models.CharField(max_length=100)
    
    COUNTRY_CHOICES = (('option 1','UK'),('option 2','USA'),)
    child_country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, default='UK')    
    
    SEX_CHOICES = (('M','Boy'),('F','Girl'),)
    child_boy_girl = models.CharField(max_length=10, choices=SEX_CHOICES, default='Boy')    

    child_age = models.IntegerField()
    child_birth_year = models.IntegerField(default=2013)

    MONTH_CHOICES = (('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December'))
    child_birth_month = models.CharField(max_length=10, choices=MONTH_CHOICES, default=1)    

    DAY_CHOICES = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31'))
    child_birth_day = models.CharField(max_length=10, choices=DAY_CHOICES, default=1)    

    AGE_TIME_CHOICES = (('YS','Years'),('Y','Year'),('MS','Months'),('M','Month'),('D','Days'),)
    child_age_time = models.CharField(max_length=10, choices=AGE_TIME_CHOICES, default='Years')    

    child_relative_name = models.CharField(max_length=50)
    child_friend_name = models.CharField(max_length=50)

    child_present = models.CharField(max_length=200)
    child_achievement = models.CharField(max_length=200)

    LETTER_DESIGN_CHOICES = (('1','letter1'),('2','letter2'),('3','letter3'),('4','letter4'),('5','letter5'),)
    letter_design = models.CharField(max_length=10, choices=LETTER_DESIGN_CHOICES, default='1')    

    DELIVERY_DATE_CHOICES = (('1','Monday 6th Nov 2017'),('2','Monday 13th Nov 2017'),('3','Monday 20th Nov 2017'),('4','Monday 27th Nov 2017'),('5','Monday 04th Dec 2017'),('6','Monday 11th Dec 2017'),('7','Monday 18th Dec 2017'))
    delivery_date = models.CharField(max_length=10, choices=DELIVERY_DATE_CHOICES, default='1')    

    pdf_download = models.BooleanField(default=False)

    agree_terms = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, 
                                related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity