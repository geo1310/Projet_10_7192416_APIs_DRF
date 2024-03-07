from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from shop.models import Category, Product, Article

from shop.serializers import (
    CategoryDetailSerializer,
    CategoryListSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ArticleSerializer,
)


class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):

        return Category.objects.filter(active=True)
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk): # pk : clé primaire
        self.get_object().disable()
        return Response() # réponse vide c est a dire 200


class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
    
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
 
    def get_queryset(self):
        return Category.objects.all()


class ProductViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):

        return Product.objects.filter(active=True)
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk): # pk : clé primaire
        self.get_object().disable()
        return Response() # réponse vide c est a dire 200


class ArticleViewset(ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(active=True)


class AdminArticleViewset(ModelViewSet):
    
    serializer_class = ArticleSerializer
 
    def get_queryset(self):
        return Article.objects.all()
