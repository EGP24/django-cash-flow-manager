from rest_framework import serializers

from django_cash_flow_manager.cashflows.models import Category, Subcategory


class CategoryOptionSerializer(serializers.ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SubcategoryOptionSerializer(serializers.ModelSerializer[Subcategory]):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']


class CategoryOptionsQuerySerializer(serializers.Serializer[dict[str, int]]):
    type = serializers.IntegerField(required=False)


class SubcategoryOptionsQuerySerializer(serializers.Serializer[dict[str, int]]):
    category = serializers.IntegerField(required=False)
