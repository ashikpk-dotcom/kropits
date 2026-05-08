#!/usr/bin/env python
"""Test script to verify KROPITS project setup"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kropits.settings')

import django
django.setup()

from django.conf import settings

print("Testing KROPITS MVP Setup...")
print("=" * 50)

# Check installed apps
print("\n1. Checking installed apps:")
required_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_simplejwt',
    'accounts',
    'farmers',
    'buyers',
    'logistics',
    'optimizer',
    'adminpanel',
]

for app in required_apps:
    if app in settings.INSTALLED_APPS:
        print(f"  ✓ {app}")
    else:
        print(f"  ✗ {app} - NOT FOUND")

# Check middleware
print("\n2. Checking middleware:")
if 'django.middleware.locale.LocaleMiddleware' in settings.MIDDLEWARE:
    print("  ✓ LocaleMiddleware is configured")
else:
    print("  ✗ LocaleMiddleware is MISSING")

# Check language settings
print("\n3. Checking language settings:")
print(f"  USE_I18N: {settings.USE_I18N}")
print(f"  LANGUAGES: {settings.LANGUAGES}")
print(f"  LOCALE_PATHS: {settings.LOCALE_PATHS}")

# Check models
print("\n4. Checking models:")
try:
    from accounts.models import User
    print("  ✓ User model imported")
    print(f"    AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
except Exception as e:
    print(f"  ✗ User model error: {e}")

try:
    from farmers.models import FarmerProduct
    print("  ✓ FarmerProduct model imported")
except Exception as e:
    print(f"  ✗ FarmerProduct model error: {e}")

try:
    from buyers.models import BuyerRequest
    print("  ✓ BuyerRequest model imported")
except Exception as e:
    print(f"  ✗ BuyerRequest model error: {e}")

try:
    from logistics.models import Order, DeliveryPartner, DeliveryAssignment
    print("  ✓ Logistics models imported")
except Exception as e:
    print(f"  ✗ Logistics models error: {e}")

# Check URLs
print("\n5. Checking URL configuration:")
try:
    from kropits.urls import urlpatterns
    print(f"  ✓ URLs loaded: {len(urlpatterns)} patterns")
    for pattern in urlpatterns:
        print(f"    - {pattern}")
except Exception as e:
    print(f"  ✗ URL configuration error: {e}")

print("\n" + "=" * 50)
print("Setup test complete!")
