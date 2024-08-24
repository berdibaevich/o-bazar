from django.conf import settings
from decimal import Decimal
from inventory.models import ProductInventory
from django.contrib.sessions.models import Session
from checkout.models import Delivery

class Basket:
    def __init__(self, request) -> None:

        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_DATA)

        if not settings.BASKET_SESSION_DATA in self.session:
            basket = self.session[settings.BASKET_SESSION_DATA] = {}
        
        self.basket = basket


    def add(self, product_inventory, quantity):
        """
        This method add product info in the basket session
        """
        product_id = str(product_inventory.id)

        if product_id in self.basket:
            self.basket[product_id]['quantity'] = quantity

        else:
            self.basket[product_id] = {
                'price': str(product_inventory.sale_price),
                'quantity': quantity
            }
        
        self.save()


    def update_basket(self, product_id, qty):
        """
        This method updated session basket
        """
        if product_id in self.basket:
            self.basket[product_id]['quantity'] = qty

        self.save()



    def remove(self, product_id):
        """
        This method remove product info from session basket
        """
        if product_id in self.basket:
            del self.basket[product_id]

        self.save()
    
    
    def clear(self):
        """
        if payment stripe succeeded basket session removed
        """
        del self.session[settings.BASKET_SESSION_DATA]
        self.save()


    def basket_update_delivery(self, delivery_price = 0):
        sub_total = sum([Decimal(obj['price']) * obj['quantity'] for obj in self.basket.values()])
        total = sub_total + delivery_price
        return total


    def get_total_and_delivery_price(self):
        """
        This method get us all total price delivery and product total
        """
        new_price = 0
        subtotal = self.get_total_price()
        if 'purchase' in self.session:
            new_price = Delivery.objects.get(id = self.session['purchase']['delivery_id']).delivery_price
        
        return new_price + subtotal


    def get_delivery_price(self):
        """
        This method allow us to get delivery price
        """
        if 'purchase' in self.session:
            return Delivery.objects.get(id = self.session['purchase']['delivery_id']).delivery_price
        
        return 0



    def __len__(self):
        """
        This method gives us product quantity
        """
        return sum([obj.get('quantity') for obj in self.basket.values()])


    def __iter__(self):
        product_ids = self.basket.keys()
        products = ProductInventory.objects.filter(id__in = product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    
    def get_total_price(self):
        return sum([obj['quantity'] * Decimal(obj['price']) for obj in self.basket.values()])

        





    def save(self):
        """
        This method saved data in the session 
        """
        self.session.modified = True