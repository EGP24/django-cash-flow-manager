from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from django_cash_flow_manager.cashflows.models import (
    CashFlowStatus,
    CashFlowTransaction,
    CashFlowType,
    Category,
    Subcategory,
)


DEFAULT_USERNAME = 'admin'
DEFAULT_EMAIL = 'admin@example.com'
DEFAULT_PASSWORD = 'admin'


class Command(BaseCommand):
    help = 'Create idempotent mock data for manual local testing.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--username', default=DEFAULT_USERNAME)
        parser.add_argument('--email', default=DEFAULT_EMAIL)
        parser.add_argument('--password', default=DEFAULT_PASSWORD)

    @transaction.atomic
    def handle(self, *args: object, **options: object) -> None:
        username = str(options['username'])
        email = str(options['email'])
        password = str(options['password'])

        self.create_demo_admin(username, email, password)
        self.create_cashflow_demo_data()

    def create_demo_admin(self, username: str, email: str, password: str) -> None:
        user, created = get_user_model().objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            },
        )

        if created:
            user.set_password(password)
            user.save(update_fields=['password'])
            self.stdout.write(self.style.SUCCESS(f'Created demo admin user: {username}/{password}'))
            return

        changed_fields = []
        if user.email != email:
            user.email = email
            changed_fields.append('email')
        if not user.is_staff:
            user.is_staff = True
            changed_fields.append('is_staff')
        if not user.is_superuser:
            user.is_superuser = True
            changed_fields.append('is_superuser')

        if changed_fields:
            user.save(update_fields=changed_fields)

        self.stdout.write(self.style.SUCCESS(f'Demo admin user already exists: {username}/{password}'))

    def create_cashflow_demo_data(self) -> None:
        status_business = self.get_status('Бизнес')
        status_personal = self.get_status('Личное')
        status_tax = self.get_status('Налог')
        income_type = self.get_type('Пополнение')
        outcome_type = self.get_type('Списание')

        marketing = self.get_category('Маркетинг', outcome_type)
        infrastructure = self.get_category('Инфраструктура', outcome_type)
        taxes = self.get_category('Налоги', outcome_type)
        sales = self.get_category('Продажи', income_type)

        avito = self.get_subcategory('Avito', marketing)
        farpost = self.get_subcategory('Farpost', marketing)
        vps = self.get_subcategory('VPS', infrastructure)
        tax_payment = self.get_subcategory('УСН', taxes)
        direct_sales = self.get_subcategory('Прямые продажи', sales)

        self.get_transaction(
            transaction_date=date(2025, 1, 10),
            status=status_business,
            cashflow_type=outcome_type,
            category=marketing,
            subcategory=avito,
            amount=Decimal('12500.00'),
            comment='Тестовая оплата Avito',
        )
        self.get_transaction(
            transaction_date=date(2025, 1, 12),
            status=status_business,
            cashflow_type=outcome_type,
            category=marketing,
            subcategory=farpost,
            amount=Decimal('8200.00'),
            comment='Тестовая оплата Farpost',
        )
        self.get_transaction(
            transaction_date=date(2025, 1, 15),
            status=status_business,
            cashflow_type=outcome_type,
            category=infrastructure,
            subcategory=vps,
            amount=Decimal('3400.00'),
            comment='Тестовая оплата VPS',
        )
        self.get_transaction(
            transaction_date=date(2025, 1, 20),
            status=status_business,
            cashflow_type=income_type,
            category=sales,
            subcategory=direct_sales,
            amount=Decimal('50000.00'),
            comment='Тестовое пополнение от продаж',
        )
        self.get_transaction(
            transaction_date=date(2025, 1, 25),
            status=status_tax,
            cashflow_type=outcome_type,
            category=taxes,
            subcategory=tax_payment,
            amount=Decimal('6000.00'),
            comment='Тестовая уплата налога',
        )
        self.get_transaction(
            transaction_date=date(2025, 1, 28),
            status=status_personal,
            cashflow_type=income_type,
            category=sales,
            subcategory=direct_sales,
            amount=Decimal('15000.00'),
            comment='Тестовый личный перевод',
        )

        self.stdout.write(self.style.SUCCESS('Cash flow mock data is ready'))

    def get_status(self, name: str) -> CashFlowStatus:
        status, _created = CashFlowStatus.objects.get_or_create(name=name)
        return status

    def get_type(self, name: str) -> CashFlowType:
        cashflow_type, _created = CashFlowType.objects.get_or_create(name=name)
        return cashflow_type

    def get_category(self, name: str, cashflow_type: CashFlowType) -> Category:
        category, _created = Category.objects.get_or_create(name=name, type=cashflow_type)
        return category

    def get_subcategory(self, name: str, category: Category) -> Subcategory:
        subcategory, _created = Subcategory.objects.get_or_create(name=name, category=category)
        return subcategory

    def get_transaction(
        self,
        transaction_date: date,
        status: CashFlowStatus,
        cashflow_type: CashFlowType,
        category: Category,
        subcategory: Subcategory,
        amount: Decimal,
        comment: str,
    ) -> CashFlowTransaction:
        transaction, _created = CashFlowTransaction.objects.get_or_create(
            comment=comment,
            defaults={
                'date': transaction_date,
                'status': status,
                'type': cashflow_type,
                'category': category,
                'subcategory': subcategory,
                'amount': amount,
            },
        )
        return transaction
