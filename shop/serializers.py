from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, Article


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "description", "date_created", "date_updated", "active"]


class ProductSerializer(ModelSerializer):

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
        ]


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
