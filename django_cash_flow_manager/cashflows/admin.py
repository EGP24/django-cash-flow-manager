from django.contrib import admin

from django_cash_flow_manager.cashflows.models import (
    CashFlowStatus,
    CashFlowTransaction,
    CashFlowType,
    Category,
    Subcategory,
)


@admin.register(CashFlowStatus)
class CashFlowStatusAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(CashFlowType)
class CashFlowTypeAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ('name', 'type', 'created_at', 'updated_at')
    list_filter = ('type',)
    search_fields = ('name', 'type__name')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ('name', 'category', 'created_at', 'updated_at')
    list_filter = ('category__type', 'category')
    search_fields = ('name', 'category__name')


@admin.register(CashFlowTransaction)
class CashFlowTransactionAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ('date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment')
    list_filter = ('date', 'status', 'type', 'category', 'subcategory')
    search_fields = ('comment', 'category__name', 'subcategory__name')
    autocomplete_fields = ('status', 'type', 'category', 'subcategory')
