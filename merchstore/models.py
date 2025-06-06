from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ProductType(models.Model):
    '''
    The class represents a category or type of product.
    '''
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchstore:product-list', args=[str(self.name)])

    def get_products(self):
        return self.products.all()

    class Meta:
        ordering = ['name']
        verbose_name = 'Product Type'


class Product(models.Model):
    '''
    The class represents a product available for sale.
    It has foreign keys to its corresponding owner and product type.
    '''
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=100,
                                decimal_places=2,
                                default=1)
    productType = models.ForeignKey(ProductType,
                                    on_delete=models.SET_NULL,
                                    related_name='products',
                                    null=True)
    stock = models.IntegerField(default=1)
    owner = models.ForeignKey(Profile,
                              on_delete=models.CASCADE,
                              related_name='products',
                              null=True,
                              )

    STATUS_CHOICES = {
        'Available': 'Available',
        'On sale': 'On sale',
        'Out of stock': 'Out of stock',
    }
    status = models.CharField(max_length=255,
                              choices=STATUS_CHOICES,
                              default='AVAILABLE')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchstore:item', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        '''
        The save() function is overrided
        to automatically update the intance's status
        based on changes in stock.
        '''
        if self.stock <= 0:
            self.status = 'Out of stock'
        else:
            if (not self.status=='On sale'):
                self.status = 'Available'
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'


class Transaction(models.Model):
    '''
    The class represents the transaction of certain product between owner and buyer.
    It has foreign keys to the product being sold and the interested buyer.
    '''
    buyer = models.ForeignKey(Profile,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='transactions')
    product = models.ForeignKey(Product,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='transactions')
    amount = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    STATUS_CHOICES = {
        'On cart': 'On cart',
        'To pay': 'To pay',
        'To ship': 'To ship',
        'To receive': 'To receive',
        'Delivered': 'Delivered'
    }
    status = models.CharField(max_length=255,
                              choices=STATUS_CHOICES,
                              null=True)

    def get_absolute_url(self):
        return reverse('merchstore:transaction', args=[str(self.pk)])

    class Meta:
        ordering = ['buyer', 'created_on']
        verbose_name = 'Transaction'
    
