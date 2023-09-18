from rest_framework import routers
from .views import *

router = routers.SimpleRouter()

# Router list
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product_relation', ProductUserRelationView)
router.register(r'wishlist_products', WishlistProductsView, basename='Product')
