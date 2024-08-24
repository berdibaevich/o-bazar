from django.urls import reverse
from django.db.models import Count
from rest_framework import serializers
from account.models import Address, Customer
from inventory.models import (
    Category,
    Product,
    ProductInventory,
    Brand,
    Media,
    ProductAttributeValue
)
from account.models import (
    Customer,
    Address
)
from checkout.models import Delivery
from orders.models import Order, OrderItem

#        INVENTORY APP

# CATEGORY CHILDREN NAME SERIALIZERS
class CategoryChildSerializers(serializers.Serializer):
    name = serializers.CharField(read_only = True)
    products = serializers.HyperlinkedIdentityField(
        view_name="api:product-detail-by-categorychild",
        lookup_field = 'slug'
    )
# END CATEGORY CHILDREN NAME SERIALIZERS



# GET CATEGORY SERIALIZERS
class CategorySerializers(serializers.ModelSerializer):
    children = CategoryChildSerializers(read_only = True, many = True)
    products_url = serializers.HyperlinkedIdentityField(
        view_name="api:products-by-category",
        lookup_field = 'slug'
    )
    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
            "products_url",
            "num_children",
            "children",
        ]


    # BELLOW OLD ASLO BAD BECAUSE THIS HITS TO DATABASE SO MANY  OK :) :) 

    #children = serializers.SerializerMethodField(read_only = True)
    # def get_children(self, obj):
    #     """
    #     THE METHOD GIVES US CATEGORY PARENT'S CHILDREN
    #     """
    #     categories = obj.children.all()
    #     request = self.context.get("request")
    #     if request is None:
    #         return None
    #     return CategoryChildSerializers(categories, many = True, context={'request': request}).data


# END GET CATEGORY SERIALIZERS


# CATEGORY SERIALIZERS FOR NAME
class CategoryNameSerializers(serializers.Serializer):
    name = serializers.CharField(read_only = True)
# END CATEGORY SERIALIZERS FOR NAME


# PRODUCT TABLE SERIALIZERS 
class ProductSerializer(serializers.ModelSerializer):
    #category = CategoryNameSerializers(read_only = True)
    category = serializers.SerializerMethodField(read_only = True)
    product_detail = serializers.HyperlinkedIdentityField(
        view_name="api:product-detail",
        lookup_field = "slug"
    )
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "category",
            "product_detail"
        ]

    # BELOW OLD AND BAD OK
    #category = serializers.SerializerMethodField(source = "category")
    def get_category(self, obj):
        """
        The method gives us obj's category name
        """
        category = Category.objects.get(product__name = obj.name)
        return CategoryNameSerializers(category).data
# END PRODUCT TABLE SERIALIZERS 

# BRAND SERIALIZERS
class BrandSerializers(serializers.Serializer):
    name = serializers.CharField(read_only = True)
# END BRAND SERIALIZERS


# PRODUCT ATTRIBUTE VALUES SERIALIZERS
class ProductAttributeValueSerializer(serializers.Serializer):
    attribute_name = serializers.CharField(read_only = True)
    attribute_value = serializers.CharField(read_only = True)
# END PRODUCT ATTRIBUTE VALUES SERIALIZERS


# PRODUCT INVENTORY TABLE SERIALIZERS
class ProductInventorySerializers(serializers.ModelSerializer):
    brand = BrandSerializers(read_only = True)
    features = ProductAttributeValueSerializer(read_only = True, source = "attribute_name_values", many = True)
    images = serializers.HyperlinkedIdentityField(
        view_name="api:media-images",
        lookup_field = "id"
    )
    
    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "upc",
            "is_active",
            "sale_price",
            "quantity",
            "images",
            "brand",
            "features",
            
        ]
# END PRODUCT INVENTORY TABLE SERIALIZERS



# MEDIA SERIALIZERS
class MediaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "image",
            "alt_text",
            "is_feature"
        ]
# END MEDIA SERIALIZERS

#       END INVENTORY APP


#       ACCOUNT APP API

# CUSTOMER TABLE SERIALIZERS 
class CustomerSerializers(serializers.ModelSerializer):
    addresses_url = serializers.HyperlinkedIdentityField(
        view_name="api:customer-addresses",
        lookup_field = 'id'
    )
    customer_orders_url = serializers.HyperlinkedIdentityField(
        view_name="api:orders",
        lookup_field = "id"
    )
    class Meta:
        model = Customer
        fields = [
            'id',
            'user_name',
            'email',
            'addresses_url',
            "customer_orders_url"
        ]
# END CUSTOMER TABLE SERIALIZERS

# ADDRESS TABLE SERIALIZERS
class AddressesSerializers(serializers.ModelSerializer):
    address_detail_url = serializers.HyperlinkedIdentityField(
        view_name="api:address-detail",
        lookup_field = "id"
    )
    class Meta:
        model = Address
        fields = [
            "id",
            "full_name",
            "town_city",
            "default",
            "address_detail_url",
            
        ]
# END ADDRESS TABLE SERIALIZERS

# ADDRESS TABLE FOR DETAIL SERIALIZERS
class AddressDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
# ADDRESS TABLE FOR DETAIL SERIALIZERS

#       END ACCOUNT APP API



#       CHECKOUT APP API

# DELIVERY LIST SERIALIZERS
class DeliveryListSerializers(serializers.ModelSerializer):
    delivery_detail_url = serializers.HyperlinkedIdentityField(
        view_name="api:delivery-detail",
        lookup_field = 'id'
    )
    class Meta:
        model = Delivery
        fields = [
            "id",
            "delivery_name",
            "delivery_detail_url"
        ]
# END DELIVERY LIST SERIALIZERS


# DELIVERY DETAIL SERIALIZERS
class DeliveryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"
# END DELIVERY DETAIL SERIALIZERS

#       END CHECKOUT APP API


#       ORDERS APP API

# ORDERS TABLE SERIALIZERS LIST
class OrderListSerializers(serializers.ModelSerializer):
    order_detail_url = serializers.HyperlinkedIdentityField(
        view_name="api:order-detail",
        lookup_field = 'id'
    )
    class Meta:
        model = Order
        fields = [
            "id",
            "order_key",
            "order_detail_url"
        ]
# END ORDERS TABLE SERIALIZERS LIST


# ORDERS TABLE SERIALIZERS DETAIL
class OrderDetailSerializers(serializers.ModelSerializer):
    customer_full_name = serializers.CharField(read_only = True, source = "address.full_name")
    customer_email = serializers.EmailField(source = "user.email", read_only = True)
    order_items_url = serializers.HyperlinkedIdentityField(
        view_name="api:order-items",
        lookup_field = "id"
    )
    class Meta:
        model = Order
        fields = [
            "id",
            "total_paid",
            "billing_status",
            "customer_full_name",
            "customer_email",
            "order_items_url",
            "address",
            "created_at",
            "updated_at"
        ]
# END ORDERS TABLE SERIALIZERS DETAIL


# ORDER ITEMS SERIALIZERS LIST
class OrderItemListSerializers(serializers.ModelSerializer):
    product = serializers.CharField(read_only = True, source = "product.product.name")
    item_detail_url = serializers.HyperlinkedIdentityField(
        view_name="api:item-detail",
        lookup_field = "id"
    )
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'item_detail_url'
        ]
# END ORDER ITEMS SERIALIZERS LIST


# ORDER ITEMS SERIALIZERS DETAIL
class OrderItemDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__" 
# END ORDER ITEMS SERIALIZERS DETAIL


#       END ORDERS APP API







