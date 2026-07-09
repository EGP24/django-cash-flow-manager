from django.core.exceptions import ValidationError


def validate_transaction_dependencies(
    *,
    type_id: int | None,
    category_id: int | None,
    category_type_id: int | None,
    subcategory_category_id: int | None,
) -> None:
    errors: dict[str, str] = {}

    if category_id and type_id and category_type_id != type_id:
        errors['category'] = 'Категория не относится к выбранному типу'

    if subcategory_category_id and category_id and subcategory_category_id != category_id:
        errors['subcategory'] = 'Подкатегория не относится к выбранной категории'

    if errors:
        raise ValidationError(errors)
