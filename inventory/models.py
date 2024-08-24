import re
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

# Create your models here.

# CATEGORY TABLE 
class Category(MPTTModel):
    """
    Category Table implemented with MPTT
    """
    name = models.CharField(
        max_length=100,
        unique=False, verbose_name=_("category name"),
        help_text=_("Format: required, max-100")
    )
    slug = models.SlugField(
        blank=True, 
        max_length=100, unique=False,
        verbose_name=_("SAFE URL"),
        help_text=_("format: required, letter, numbers, underscore or hyphens")
    )
    is_active = models.BooleanField(default=True)

    parent = TreeForeignKey("self", on_delete=models.PROTECT,
    related_name="children", null=True, blank=True, unique=False,
    verbose_name=_("parent of category"),
    help_text=_("format: not required")
    )

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")


    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        name = self.name.lower()
        slug_name = re.sub(r"\s", "-", name)
        self.slug = slug_name
        super().save(*args, **kwargs)

    
    def num_children(self):
        """
        THIS METHOD FOR API HOW MANY CATEGORY'S CHILDREN HAVE SO ALSO OPTIMIZATION GOOD WHY BEACUSE 
        YOU CHECK OUT API VIEWS FOR CATEGORIES_API_VIEW FUNC HAS LIKE prefetch_related("children")
        """
        return self.children.all().count()
  

    
    def get_absolute_url(self):
        return reverse("inventory:products-by-category", kwargs={'slug': self.slug})  
# END CATEGORY TABLE



# PRODUCT TABLE 
class Product(models.Model):
    """
    Product Detail table
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_("Product name"),
        help_text=_("format: required, max-200")
    )

    slug = models.SlugField(
        max_length=200,
        verbose_name=_("Product safe URL"),
        help_text=_("format: required, letters, numbers etc")
    )
    description = models.TextField(
        verbose_name=_("Product description"),
        help_text=_("format: required")
    )

    category = TreeManyToManyField(Category)
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("product visibility"),
        help_text=_("format: true=product visible")
    )
    created_at = models.DateTimeField(
        auto_now_add= True,
        verbose_name=_("date product created"),
        help_text=_("format: Y-m-d H:M:S")
    )
    updated_at = models.DateTimeField(
        auto_now= True,
        verbose_name=_("date product last updated"),
        help_text=_("format: Y-m-d H:M:S")
    )


    def __str__(self):
        return self.name
# END PRODUCT TABLE 



# BRAND TABLE 
class Brand(models.Model):
    """
    Product brand tabel
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("brand name"),
        help_text=_("format: required, max-200")
    )

    def __str__(self):
        return self.name
# END BRAND TABLE 



# PRODUCTINVENTORY TABLE 
class ProductInventory(models.Model):
    """
    Product inventory table
    """
    upc = models.CharField( #upc --> bul shtrix code 
        max_length=12,
        unique=True,
        verbose_name=_("universal product code"),
        help_text=_("format: required, unique, max-12")
    )
    
    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.CASCADE
    )

    brand = models.ForeignKey(
        Brand, related_name="brand", on_delete=models.CASCADE
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("product visibility"),
        help_text=_("format: true=product visible")
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name=_("default selection"),
        help_text=_("format: true= sub product visible")
    )

    sale_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        verbose_name=_("sale price"),
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name":{
                "max_length": _("the price must be between 0 and 999.99")
            }
        }
    )

    quantity = models.IntegerField(
        default=1,
        verbose_name=_("product Quantity")
    )
    

    created_at = models.DateTimeField(
        auto_now_add= True,
        verbose_name=_("date sub-product created"),
        help_text=_("format: Y-m-d H:M:S")
    )

    updated_at = models.DateTimeField(
        auto_now= True,
        verbose_name=_("date sub-product last updated"),
        help_text=_("format: Y-m-d H:M:S")
    )


    def __str__(self):
        return self.product.name
# END PRODUCTINVENTORY TABLE


# MEDIA TABLE 
class Media(models.Model):
    """
    The Product image table
    """
    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.PROTECT,
        related_name="media_product_inventory"
    )
    image = models.ImageField(
        verbose_name=_("product image"),
        upload_to="images/",
        default="py.png",
        help_text=_("format: required"),
        blank=True
    )
    alt_text = models.CharField(
        max_length=255,
        verbose_name=_("alternative text"),
        help_text=_("format: required")
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name=_("product default image"),
        help_text=_("format: default=False, true=default image")
    )

    created_at = models.DateTimeField(
        auto_now_add= True,
        editable=False,
        verbose_name=_("date product image created"),
        help_text=_("format: Y-m-d H:M:S")
    )

    updated_at = models.DateTimeField(
        auto_now= True,
        editable=False,
        verbose_name=_("date product image last updated"),
        help_text=_("format: Y-m-d H:M:S")
    )

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")


    
    def __str__(self):
        return self.alt_text
# END MEDIA TABLE 



# PRODUCTATTRIBUTETABLE TABLE 
class ProductAttributeValue(models.Model):
    """
    Product attribute value table
    """
    product_inventory = models.ForeignKey(
        ProductInventory, 
        on_delete=models.CASCADE,
        related_name="attribute_name_values"
    )
    attribute_name = models.CharField(
        max_length=255,
        verbose_name=_("attribute name"),
        help_text=_("format: required, max-255")
    )
    attribute_value = models.CharField(
        max_length=255,
        verbose_name=_("attribute value"),
        help_text=_("format: required, max-255")
    )

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value}"
# END PRODUCTATTRIBUTETABLE TABLE 


# MOST SOLD PRODUCTS
class BestSellingProducts(models.Model):
    product = models.ForeignKey(ProductInventory, on_delete=models.PROTECT, related_name='best_selling_products')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product.name} {self.quantity}"
        
# END MOST SOLD PRODUCTS
