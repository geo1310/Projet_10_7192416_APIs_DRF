from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer


class CategoryViewset(ReadOnlyModelViewSet):

    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)


class ProductViewset(ModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        # Nous récupérons tous les produits dans une variable nommée queryset
        queryset = Product.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        category_id = self.request.GET.get('category_id')
        not_active = self.request.GET.get('not_active')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        elif not_active:
            queryset = Product.objects.filter(active=False)
        return queryset
