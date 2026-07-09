from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django_cash_flow_manager.cashflows.api.serializers import (
    CategoryOptionSerializer,
    CategoryOptionsQuerySerializer,
    SubcategoryOptionSerializer,
    SubcategoryOptionsQuerySerializer,
)
from django_cash_flow_manager.cashflows.models import Category, Subcategory


class CategoryOptionsViewSet(ViewSet):
    def list(self, request: Request) -> Response:
        query_serializer = CategoryOptionsQuerySerializer(data=request.query_params)
        type_id = query_serializer.validated_data.get('type') if query_serializer.is_valid() else None
        categories = self.get_queryset(type_id)
        serializer = CategoryOptionSerializer(categories, many=True)
        return Response({'results': serializer.data})

    def get_queryset(self, type_id: int | None) -> QuerySet[Category]:
        if type_id:
            return Category.objects.filter(type_id=type_id).order_by('pk')
        return Category.objects.none()


class SubcategoryOptionsViewSet(ViewSet):
    def list(self, request: Request) -> Response:
        query_serializer = SubcategoryOptionsQuerySerializer(data=request.query_params)
        category_id = query_serializer.validated_data.get('category') if query_serializer.is_valid() else None
        subcategories = self.get_queryset(category_id)
        serializer = SubcategoryOptionSerializer(subcategories, many=True)
        return Response({'results': serializer.data})

    def get_queryset(self, category_id: int | None) -> QuerySet[Subcategory]:
        if category_id:
            return Subcategory.objects.filter(category_id=category_id).order_by('name')
        return Subcategory.objects.none()
