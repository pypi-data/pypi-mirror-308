from django.conf import settings

PACKAGE_MODEL = getattr(settings, 'FEES_PACKAGE_MODEL', 'fees.Package')
PURCHASER_MODEL = getattr(settings, 'FEES_PURCHASER_MODEL', settings.AUTH_USER_MODEL)
CURRENCY = getattr(settings, 'FEES_CURRENCY', 'EUR')
SCHEDULE_SUBSCRIPTION_REMINDERS = getattr(settings, 'FEES_SCHEDULE_SUBSCRIPTION_REMINDERS', False)
MIGRATION_DEPENDENCIES = getattr(settings, 'FEES_MIGRATION_DEPENDENCIES', [])
MULTIPLE_PLANS = getattr(settings, 'FEES_MULTIPLE_PLANS', False)
CACHE_EXPIRATION = getattr(settings, 'FEES_CACHE_EXPIRATION', 43200000) # half day as default
