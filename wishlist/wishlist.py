from django.conf import settings
from django.contrib.sessions.models import Session
from inventory.models import ProductInventory


class WishList:
    is_message = True
    def __init__(self, request) -> None:
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_DATA)
        
        if settings.WISHLIST_SESSION_DATA not in self.session:
            wishlist = self.session[settings.WISHLIST_SESSION_DATA] = {}
        
        self.wishlist = wishlist

    

    def get_message(self):
        return self.is_message


    
    def add(self, product_id):
        productstr_id = str(product_id)
        if productstr_id not in self.wishlist:
            self.wishlist[productstr_id] = {'id': product_id}
            self.is_message = True
        else:
            del self.wishlist[productstr_id]
            self.is_message = False
            
        self.save()

    

    def remove(self, product_id):
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()

    
    def __len__(self):
        return len([i['id'] for i in self.wishlist.values()])



    def __iter__(self):
        product_ids = self.wishlist.keys()
        products = ProductInventory.objects.filter(id__in = product_ids)
        wishlist = self.wishlist.copy()
        
        for product in products:
            wishlist[str(product.id)]['product'] = product

        for item in self.wishlist.values():
            yield item

    


    def save(self):
        self.session.modified = True

        
