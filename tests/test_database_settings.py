from pathlib import Path

import pytest
from django.core.exceptions import ImproperlyConfigured

import django_cash_flow_manager.settings as project_settings


pytestmark = pytest.mark.unit


def test_env_bool_returns_default_for_missing_value(monkeypatch):
    # arrange
    monkeypatch.delenv('MISSING_BOOLEAN', raising=False)

    # act
    result = project_settings.env_bool('MISSING_BOOLEAN', default=True)

    # assert
    assert result is True


def test_env_bool_parses_truthy_values(monkeypatch):
    # arrange
    monkeypatch.setenv('FEATURE_ENABLED', 'yes')

    # act
    result = project_settings.env_bool('FEATURE_ENABLED')

    # assert
    assert result is True


def test_env_list_splits_comma_separated_values(monkeypatch):
    # arrange
    monkeypatch.setenv('HOSTS', 'localhost, 127.0.0.1,,example.com')

    # act
    result = project_settings.env_list('HOSTS')

    # assert
    assert result == ['localhost', '127.0.0.1', 'example.com']


def test_database_config_uses_sqlite_by_default(monkeypatch):
    # arrange
    monkeypatch.delenv('DATABASE_ENGINE', raising=False)

    # act
    database_config = project_settings.build_database_config(Path('/app'))

    # assert
    assert database_config == {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': Path('/app') / 'db.sqlite3',
        }
    }


def test_database_config_uses_postgres_when_requested(monkeypatch):
    # arrange
    monkeypatch.setenv('DATABASE_ENGINE', 'postgresql')
    monkeypatch.setenv('POSTGRES_DB', 'cash_flow_manager')
    monkeypatch.setenv('POSTGRES_USER', 'cash_flow_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'cash_flow_password')
    monkeypatch.setenv('POSTGRES_HOST', 'db')
    monkeypatch.setenv('POSTGRES_PORT', '5432')

    # act
    database_config = project_settings.build_database_config(Path('/app'))

    # assert
    assert database_config == {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'cash_flow_manager',
            'USER': 'cash_flow_user',
            'PASSWORD': 'cash_flow_password',
            'HOST': 'db',
            'PORT': '5432',
        }
    }


def test_database_config_rejects_unsupported_engine(monkeypatch):
    # arrange
    monkeypatch.setenv('DATABASE_ENGINE', 'mysql')

    # act
    with pytest.raises(ImproperlyConfigured) as exc_info:
        project_settings.build_database_config(Path('/app'))

    # assert
    assert 'Unsupported DATABASE_ENGINE' in str(exc_info.value)
