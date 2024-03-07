from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from shop.models import Category, Product, Article


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "date_created", "date_updated", "name", "active"]


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
        fields = ["id", "date_created", "date_updated", "name", "description", "active"]

    def validate_name(self, value):
        # Controle sur un champ unique
        # Nous vérifions que la catégorie existe
        if Category.objects.filter(name=value).exists():
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise ValidationError('Category already exists')
        return value
    
    def validate(self, data):
        # Controle global sur tous les champs
        # Effectuons le contrôle sur la présence du nom dans la description
        if data['name'] not in data['description']:
        # Levons une ValidationError si ça n'est pas le cas
            raise ValidationError('Name must be in description')
        return data



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

    #product = SerializerMethodField()

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

    def get_product(self, instance):
        # Assurez-vous que 'product' est une instance de modèle valide
        if instance.product:

            serializer = ProductListSerializer(instance.product)
            return serializer.data
        
        return None  # ou une autre valeur par défaut si nécessaire
    
    def validate(self, data):
        # Controle global sur tous les champs
        
        if data['price'] <= 1:
        # Levons une ValidationError si ça n'est pas le cas
            raise ValidationError('Prix trop bas ( inférieur à 1€ )')
        elif not data['product'].active:
            raise ValidationError("Le produit n'est pas actif.")
        return data




