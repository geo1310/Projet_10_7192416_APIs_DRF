from rest_framework.serializers import ModelSerializer, SerializerMethodField

from shop.models import Category, Product, Article


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "date_created", "date_updated", "name"]


class ProductDetailSerializer(ModelSerializer):

    articles = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "date_created",
            "date_updated",
            "active",
            "articles",
        ]

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "date_created", "date_updated", "name"]


class CategoryDetailSerializer(ModelSerializer):

    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'products'
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "date_created", "date_updated", "name", "products"]

    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductDetailSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = [
            "id",
            "name",
            "description",
            "price",
            "product",
            "date_created",
            "date_updated",
            "active",
        ]
