import logging
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, EMPTY_VALUES
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import override as override_language, ngettext
from modeltrans.fields import TranslationField

from pragmatic.managers import EmailManager

from fees.querysets import PackageQuerySet, PlanQuerySet
from fees import settings as fees_settings
from fees import get_package_model
from .helpers import get_purchaser_model, invalidate_purchaser_cache

try:
    # older Django
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    # Django >= 3
    from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('fees')


class Quota(models.Model):
    """
    Single countable or boolean property of system (limitation).
    """
    codename = models.CharField(_('codename'), max_length=50, unique=True, db_index=True)
    name = models.CharField(_('name'), max_length=100)
    unit = models.CharField(_('unit'), max_length=100, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_boolean = models.BooleanField(_('is boolean'), default=False)
    order = models.PositiveSmallIntegerField(verbose_name=_('ordering'), help_text=_('to set order in pricing'), default=1)
    i18n = TranslationField(fields=('name', 'description'))

    class Meta:
        ordering = ('order',)
        verbose_name = _("Quota")
        verbose_name_plural = _("Quotas")

    def __str__(self):
        return "%s" % (self.name_i18n, )


class PackageQuotaManager(models.Manager):
    def get_query_set(self):
        return super(PackageQuotaManager, self).get_query_set().select_related('package', 'quota')


class PackageQuota(models.Model):
    package = models.ForeignKey(fees_settings.PACKAGE_MODEL, on_delete=models.CASCADE)
    quota = models.ForeignKey('Quota', on_delete=models.CASCADE)
    value = models.IntegerField(default=1, null=True, blank=True)
    objects = PackageQuotaManager()

    class Meta:
        verbose_name = _("Package quota")
        verbose_name_plural = _("Packages quotas")
        unique_together = (('package', 'quota'),)


class AbstractPackage(models.Model):
    title = models.CharField(_('title'), unique=True, max_length=50)
    description = models.TextField(_('description'), blank=True)
    order = models.PositiveSmallIntegerField(verbose_name=_('ordering'), help_text=_('to set order in pricing'), unique=True, default=1)
    trial_duration = models.PositiveSmallIntegerField(verbose_name=_('trial duration'), help_text=_('in days'), default=0)
    is_default = models.BooleanField(
        _('default'),
        help_text=_('Default package for new purchaser (useful for trial packages). Only 1 default package at a time can be set.'),
        default=False,
        db_index=True,
    )
    is_fallback = models.BooleanField(
        _('fallback'),
        help_text=_('Fallback package for purchaser when its subscription expires or trial ends (useful for freemium packages). Only 1 fallback package at a time can be set.'),
        default=False,
        db_index=True,
    )
    is_available = models.BooleanField(
        _('available'), default=False, db_index=True,
        help_text=_('Is still available for purchase')
    )
    is_visible = models.BooleanField(
        _('visible'), default=True, db_index=True,
        help_text=_('Is visible in pricing page')
    )
    quotas = models.ManyToManyField(Quota, through=PackageQuota)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    objects = PackageQuerySet.as_manager()
    i18n = TranslationField(fields=('title', 'description',))

    class Meta:
        abstract = True
        verbose_name = _('package')
        verbose_name_plural = _('packages')
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['is_fallback'], condition=models.Q(is_fallback=True), name='unique_fallback'),
        ]

    def __str__(self):
        return self.title_i18n

    def get_absolute_url(self):
        return reverse('fees:packages')

    @classmethod
    def get_default_package(cls):
        if fees_settings.MULTIPLE_PLANS:
            raise ImproperlyConfigured(
                "FEES_MULTIPLE_PLANS is configured to use multiple default packages"
            )
        try:
            return_value = cls.objects.get(is_default=True)
        except cls.DoesNotExist:
            return_value = None
        return return_value

    @classmethod
    def get_default_packages(cls):
        if not fees_settings.MULTIPLE_PLANS:
            raise ImproperlyConfigured(
                "FEES_MULTIPLE_PLANS is configured to use single default package"
            )
        try:
            return_value = cls.objects.filter(is_default=True)
        except cls.DoesNotExist:
            return_value = None
        return return_value

    @classmethod
    def get_fallback_package(cls):
        try:
            return_value = cls.objects.get(is_fallback=True)
        except cls.DoesNotExist:
            return_value = None
        return return_value

    @classmethod
    def get_current_package(cls, purchaser):
        """
        Get current package for purchaser.
        App should be responsible for creating purchaser's plan (after sign up for example).
        If plan is expired or not present, return fallback package if available else None.
        """
        # We need to handle both default package (new purchaser -> TRIAL) and expired plan -> fallback

        if fees_settings.MULTIPLE_PLANS:
            raise ImproperlyConfigured(
                "FEES_MULTIPLE_PLANS is configured to use multiple current packages"
            )

        is_anonymous = isinstance(purchaser, get_user_model()) and purchaser.is_anonymous

        # anonymous user
        if not purchaser or is_anonymous:
            # TODO: any other rules?
            return None

        plan_is_set = hasattr(purchaser, 'plan') and purchaser.plan is not None

        # currently, valid (not expired) package
        if plan_is_set and not purchaser.plan.is_expired():
            return purchaser.plan.package

        return get_package_model().__validate_and_return_fallback_package(plan_is_set)

    @classmethod
    def get_current_packages(cls, purchaser):
        """
        Get current packages for purchaser.
        App should be responsible for creating purchaser's plan (after sign up for example).
        If plan is expired or not present, return fallback package if available else None.
        """
        # We need to handle both default package (new purchaser -> TRIAL) and expired plan -> fallback

        if not fees_settings.MULTIPLE_PLANS:
            raise ImproperlyConfigured(
                "FEES_MULTIPLE_PLANS is configured to use single current package"
            )


        is_anonymous = isinstance(purchaser, get_user_model()) and purchaser.is_anonymous

        # anonymous user
        if not purchaser or is_anonymous:
            # TODO: any other rules?
            return None

        plans_are_set = hasattr(purchaser, 'plans') and purchaser.plans is not None
        not_expired_packages = [plan.package for plan in purchaser.plans if not plan.is_expired()]

        # currently, valid (not expired) packages
        if plans_are_set and not_expired_packages:
            return not_expired_packages

        return [get_package_model().__validate_and_return_fallback_package(plans_are_set)]

    def get_quotas(self):
        quota_dic = {}
        for package_quota in PackageQuota.objects.filter(package=self).select_related('quota'):
            if get_package_model().is_quota_available(package_quota):
                quota_dic[package_quota.quota.codename] = package_quota.value
        return quota_dic

    @staticmethod
    def is_quota_available(package_quota):
        value = package_quota['value'] if isinstance(package_quota, dict) else package_quota.value
        return value is None or value > 0

    def is_free(self):
        return not self.pricing_set.exists()
    is_free.boolean = True

    def monthly_plan(self):
        return self.pricing_set.filter(period=Pricing.PERIOD_MONTH).order_by('duration').first()

    is_free.boolean = True

    @staticmethod
    def __validate_and_return_fallback_package(plan_is_set):
        # fallback package
        fallback_package = get_package_model().get_fallback_package()

        # validation of fallback package price (fallback package can't be free)
        if fallback_package is not None and not fallback_package.is_free():
            if plan_is_set:
                raise ValidationError(_('Plan has expired and fallback package is not free'))
            else:
                raise ValidationError(_('Plan not found and fallback package is not free'))

        # fallback package for expired or not present plan
        return fallback_package


class Package(AbstractPackage):
    class Meta(AbstractPackage.Meta):
        swappable = "FEES_PACKAGE_MODEL"


class Pricing(models.Model):
    PERIOD_DAY = 'DAY'
    PERIOD_MONTH = 'MONTH'
    PERIOD_YEAR = 'YEAR'
    PERIODS = [
        (PERIOD_DAY, _('day')),
        (PERIOD_MONTH, _('month')),
        (PERIOD_YEAR, _('year')),
    ]
    PERIODS_PLURALIZE = [
        (PERIOD_DAY, (_('day'), _('days'))),
        (PERIOD_MONTH, (_('month'), _('months'))),
        (PERIOD_YEAR, (_('year'), _('years'))),
    ]

    package = models.ForeignKey(fees_settings.PACKAGE_MODEL, on_delete=models.CASCADE)
    period = models.CharField(_('period'), choices=PERIODS, max_length=5)
    duration = models.PositiveSmallIntegerField(verbose_name=_('duration'), help_text=_('in period'),
                                           blank=True, null=True, default=None)
    price = models.DecimalField(_('price'), help_text=fees_settings.CURRENCY, max_digits=10, decimal_places=2, db_index=True, validators=[MinValueValidator(0.01)])
    # is_default = models.BooleanField(
    #     help_text=_('Default pricing for package'),
    #     default=False,
    #     db_index=True,
    # )
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    # objects = PricingQuerySet.as_manager()

    class Meta:
        verbose_name = _('pricing')
        verbose_name_plural = _('pricings')
        ordering = ['price']
        unique_together = (['package', 'period', 'duration'],)

    @classmethod
    def distinct_period_durations(cls):
        period_durations = cls.objects.order_by('period', 'duration').values('period', 'duration').distinct()

        for period_duration in period_durations:
            period_duration['display'] = Pricing.period_duration_display(
                period=period_duration['period'],
                duration=period_duration['duration']
            )

        return period_durations

    @staticmethod
    def period_duration_display(period, duration):
        if period == Pricing.PERIOD_DAY:
            return ngettext(
                '%(duration)d day',
                '%(duration)d days',
                duration,
            ) % {'duration': duration, }
        elif period == Pricing.PERIOD_MONTH:
            return ngettext(
                '%(duration)d month',
                '%(duration)d months',
                duration,
            ) % {'duration': duration, }
        elif period == Pricing.PERIOD_YEAR:
            return ngettext(
                '%(duration)d year',
                '%(duration)d years',
                duration,
            ) % {'duration': duration, }
        else:
            period_localize = dict(Pricing.PERIODS_PLURALIZE).get(period)
            period_display = period_localize[0] if duration == 1 else period_localize[1]
            return f'{duration} {period_display}'

    def __str__(self):
        return f'{self.package} ({self.get_duration_display()})'

    def get_absolute_url(self):
        return reverse('fees:pricing')

    def get_duration_display(self):
        return Pricing.period_duration_display(self.period, self.duration)

    def get_price_display(self):
        return f'{self.price} {fees_settings.CURRENCY}'

    # TODO: remove commerce
    def get_add_to_cart_url(self):  # TODO: move to ProductMixin, template tag?
        if 'commerce' in settings.INSTALLED_APPS:
            content_type = ContentType.objects.get_for_model(self)
            return reverse('commerce:add_to_cart', args=(content_type.id, self.id))  # TODO: human readable URL
        return '#'

    # TODO: remove commerce, add product availability handler to commerce
    # @property
    # def availability(self):
    #     from commerce.models import AbstractProduct
    #     return AbstractProduct.AVAILABILITY_DIGITAL_GOODS

    @property
    def price_per_month(self):
        price = self.price

        if self.period == self.PERIOD_DAY:
            price = self.price * 30 / self.duration  # approximately

        if self.period == self.PERIOD_MONTH:
            price = self.price / self.duration

        if self.period == self.PERIOD_YEAR:
            price = self.price / 12 / self.duration

        return round(price, 2)

    # TODO: remove commerce
    def get_price_per_month_display(self):
        return f'{self.price_per_month} {fees_settings.CURRENCY}'

    @property
    def timedelta(self):
        if self.period == self.PERIOD_DAY:
            return timedelta(days=self.duration)

        if self.period == self.PERIOD_MONTH:
            return relativedelta(months=self.duration)

        if self.period == self.PERIOD_YEAR:
            return relativedelta(years=self.duration)


class Plan(models.Model):
    """
    Currently selected plan for purchaser.
    """
    purchaser = models.ForeignKey(
        get_purchaser_model(), verbose_name=_('purchaser'),
        on_delete=models.CASCADE,
    )
    package = models.ForeignKey(fees_settings.PACKAGE_MODEL, verbose_name=_('package'), on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, help_text=_('pricing'), default=None,
                                null=True, blank=True, on_delete=models.CASCADE)
    activation = models.DateField(_('activation'), auto_now_add=True)
    expiration = models.DateField(_('expires'), help_text=_('keep blank to calculate automatically by pricing period'),
        default=None, blank=True, null=True, db_index=True)
    # is_active = models.BooleanField(_('active'), default=True, db_index=True)
    # is_recurring = models.BooleanField(_('active'), default=True, db_index=True)  # TODO: can be turned on/turned off
    modified = models.DateTimeField(_('modified'), auto_now=True)
    objects = PlanQuerySet.as_manager()

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")
        ordering = ['-activation']
        get_latest_by = 'expiration'

    def __str__(self):
        if self.pricing:
            return "%s [%s] (%s)" % (self.purchaser, self.package, self.pricing)
        return "%s [%s]" % (self.purchaser, self.package)

    def clean(self):
        existing_plans_with_package = Plan.objects.filter(purchaser=self.purchaser, package=self.package).active().exclude(pk=self.pk)

        if existing_plans_with_package.exists():
            raise ValidationError(_("There is already an active plan with this package"))

    def save(self, **kwargs):
        # update expiration date by pricing period
        if self.expiration in EMPTY_VALUES and self.pricing:
            from_date = self.activation or now().date()  # TODO: now().date() vs date.today()
            self.expiration = from_date + self.pricing.timedelta

        invalidate_purchaser_cache(self.purchaser)
        return super().save(**kwargs)

    # def is_active(self):
    #     return self.active

    def is_expired(self):
        if self.expiration is None:
            return False
        else:
            return self.expiration < date.today()

    @property
    def days_left(self):
        if self.expiration is None:
            return None
        else:
            return (self.expiration - date.today()).days

    def expires_soon(self):
        days_left = self.days_left
        return days_left is not None and days_left <= 7  # TODO: add to settings

    # def clean_activation(self):
    #     errors = plan_validation(self.purchaser)
    #     if not errors['required_to_activate']:
    #         plan_validation(self.purchaser, on_activation=True)
    #         self.activate()
    #     else:
    #         self.deactivate()
    #     return errors
    #
    # def activate(self):
    #     if not self.active:
    #         self.active = True
    #         self.save()
    #         account_activated.send(sender=self, purchaser=self.purchaser)
    #
    # def deactivate(self):
    #     if self.active:
    #         self.active = False
    #         self.save()
    #         account_deactivated.send(sender=self, purchaser=self.purchaser)

    # def initialize(self):
    #     """
    #     Set up purchaser plan for first use
    #     """
    #     if not self.is_active():
    #         # Plans without pricings don't need to expire
    #         if self.expiration is None and self.plan.pricing_set.count():
    #             self.expiration = now() + timedelta(
    #                 days=getattr(settings, 'PLANS_DEFAULT_GRACE_PERIOD', 30))
    #         self.activate()  # this will call self.save()

    def get_extended_from(self, package):
        if package.is_free():
            return None
        if not self.is_expired() and self.expiration is not None and self.package == package:
            return self.expiration
        return date.today()

    def get_extended_until(self, package, pricing):
        if package.is_free():
            return None
        # if not self.package.is_free() and self.expiration is None:
        #     return None  # TODO: why? which use case?
        # if pricing is None:  # TODO: why? which use case?
        #     return self.expiration
        # return self.get_extended_from(package) + pricing.timedelta
        from_date = self.get_extended_from(package)
        return from_date + pricing.timedelta

    def plan_autorenew_at(self):
        """
        Helper function which calculates when the plan autorenewal will occur
        """
        if self.expiration:
            plans_autorenew_before_days = getattr(settings, 'FEES_AUTORENEW_BEFORE_DAYS', 0)
            plans_autorenew_before_hours = getattr(settings, 'FEES_AUTORENEW_BEFORE_HOURS', 0)
            return self.expiration - timedelta(days=plans_autorenew_before_days, hours=plans_autorenew_before_hours)

    # def set_plan_renewal(self, order, has_automatic_renewal=True, **kwargs):
    #     """
    #     Creates or updates plan renewal information for this plan with given order
    #     """
    #     if hasattr(self, 'recurring'):
    #         # Delete the plan to populate with default values
    #         # We don't want to mix the old and new values
    #         self.recurring.delete()
    #     recurring = RecurringPlan.objects.create(
    #         plan=self,
    #         pricing=order.pricing,
    #         amount=order.amount,
    #         tax=order.tax,
    #         currency=order.currency,
    #         has_automatic_renewal=has_automatic_renewal,
    #         **kwargs,
    #     )
    #     return recurring

    def extend(self, package, pricing):
        """
        Manages extending plan after package/pricing order
        :param package:
        :param pricing: if pricing is None then plan will be only upgraded
        :return:
        """

        if pricing and pricing.package != package:
            raise ValueError(f'Extending by package {package} by invalid pricing {pricing}!')

        status = False  # flag; if extending account was successful?
        new_expiration = self.get_extended_until(package, pricing)

        if pricing is None:
            # Process a plan change request (downgrade or upgrade)
            # No account activation or extending at this point
            self.package = package

            # if self.expiration is not None and not plan.pricing_set.count():
            #     # Assume no expiry date for plans without pricing.
            #     self.expiration = None

            self.expiration = new_expiration
            self.save()

            purchaser_change_package.send(sender=self, purchaser=self.purchaser)
            # if getattr(settings, 'FEES_SEND_EMAILS_PACKAGE_CHANGED', True):
            #     mail_context = {'purchaser': self.purchaser, 'plan': self, 'plan': plan}
            #     send_template_email([self.purchaser.email], 'mail/change_plan_title.txt', 'mail/change_plan_body.txt',
            #                         mail_context, get_user_language(self.purchaser))
            logger.info(
                "Account '%s' [id=%d] package changed to '%s' [id=%d]" % (self.purchaser, self.purchaser.pk, package, package.pk))
            status = True

        else:
            # Processing standard account extending procedure
            if self.package == package:
                status = True
                if self.pricing != pricing:
                    self.pricing = pricing
            else:
                # This should not ever happen (as this case should be managed by plan change request)
                # but just in case we consider a case when user has a different plan
                if not self.package.is_free() and self.expiration is None:
                    status = True
                elif not self.package.is_free() and self.expiration > date.today():
                    status = False
                    logger.warning("Purchaser '%s' [id=%d] package NOT changed to '%s' [id=%d]" % (
                        self.purchaser, self.purchaser.pk, package, package.pk))
                else:
                    status = True
                    purchaser_change_package.send(sender=self, purchaser=self.purchaser)
                    self.package = package
                    self.pricing = pricing

            if status:
                self.expiration = new_expiration
                self.save()
                logger.info("Purchaser '%s' [id=%d] has been extended by %d days using package '%s' [id=%d]" % (
                    self.purchaser, self.purchaser.pk, pricing.timedelta.days, package, package.pk))
                # if getattr(settings, 'PLANS_SEND_EMAILS_PLAN_EXTENDED', True):
                # mail_context = {'purchaser': self.purchaser,
                #                 'plan': self,
                #                 'package': package,
                #                 'pricing': pricing}
                # TODO: get purchaser email
                # send_template_email([self.purchaser.email], 'mail/extend_account_title.txt',
                #                     'mail/extend_account_body.txt',
                #                     mail_context, get_user_language(self.user))

        # if status:
        #     self.clean_activation()

        return status

    # def expire(self):
    #     """manages expiration"""
    #
    #     self.deactivate()
    #
    #     logger.info(
    #         "Purchaser '%s' [id=%d] has expired" % (self.purchaser, self.purchaser.pk))
    #
    #     mail_context = {'purchaser': self.purchaser, 'plan': self}
    #     send_template_email([self.purchaser.email], 'mail/expired_account_title.txt', 'mail/expired_account_body.txt',
    #                         mail_context, get_user_language(self.purchaser))
    #
    #     account_expired.send(sender=self, user=self.purchaser)

    def send_reminder(self):
        if self.is_expired():
            return

        # TODO: get language of purchaser
        with override_language(self.purchaser.preferred_language):
            EmailManager.send_mail(self.purchaser, 'fees/mails/subscription_reminder', _('Your subscription is going to expire soon'), data={'plan': self}, request=None)

    # def remind_expire_soon(self):
    #     """reminds about soon account expiration"""
    #
    #     mail_context = {
    #         'purchaser': self.purchaser,
    #         'plan': self,
    #         'days': self.days_left
    #     }
    #     send_template_email([self.user.email], 'mail/remind_expire_title.txt', 'mail/remind_expire_body.txt',
    #                         mail_context, get_user_language(self.user))

    @classmethod
    def create_for_purchaser(cls, purchaser, pricing=None):
        if pricing:
            package = pricing.package
            expiration = now() + pricing.timedelta
        else:
            if fees_settings.MULTIPLE_PLANS:
                plans = []
                packages = get_package_model().get_default_packages()

                # check if default packages is available
                if not packages:
                    return

                for package in packages:
                    expiration = None if package.is_free() else now() + timedelta(days=package.trial_duration)
                    plans.append(Plan.objects.create(purchaser=purchaser, package=package, pricing=pricing, expiration=expiration))
                return plans
            else:
                package = get_package_model().get_default_package()

                # check if default packages is available
                if not package:
                    return

                expiration = None if package.is_free() else now() + timedelta(days=package.trial_duration)

        return Plan.objects.create(purchaser=purchaser, package=package, pricing=pricing, expiration=expiration)


    @classmethod
    def create_for_purchasers_without_plan(cls):
        purchasers = get_purchaser_model().objects.filter(plan=None).only('pk')

        for purchaser in purchasers:
            Plan.create_for_purchaser(purchaser)

        return purchasers


# class RecurringPlan(models.Model):
#     """
#     OneToOne model associated with Plan that stores information about the plan recurrence.
#     More about recurring payments in docs.
#     """
#     plan = models.OneToOneField('Plan', on_delete=models.CASCADE, related_name='recurring')
#     token = models.CharField(
#         _('recurring token'),
#         help_text=_('Token, that will be used for payment renewal. Depends on used payment provider'),
#         max_length=255,
#         default=None,
#         null=True,
#         blank=True,
#     )
#     payment_provider = models.CharField(
#         _('payment provider'),
#         help_text=_('Provider, that will be used for payment renewal'),
#         max_length=255,
#         default=None,
#         null=True,
#         blank=True,
#     )
#     pricing = models.ForeignKey('Pricing', help_text=_('Recurring pricing'), default=None,
#                                 null=True, blank=True, on_delete=models.CASCADE)
#     amount = models.DecimalField(
#         _('amount'), max_digits=7, decimal_places=2, db_index=True, null=True, blank=True)
#     tax = models.DecimalField(_('tax'), max_digits=4, decimal_places=2, db_index=True, null=True,
#                               blank=True)  # Tax=None is when tax is not applicable
#     currency = models.CharField(_('currency'), max_length=3)
#     has_automatic_renewal = models.BooleanField(
#         _('has automatic plan renewal'),
#         help_text=_(
#             'Automatic renewal is enabled for associated plan. '
#             'If False, the plan renewal can be still initiated by user.',
#         ),
#         default=False,
#     )
    # card_expire_year = models.IntegerField(null=True, blank=True)
    # card_expire_month = models.IntegerField(null=True, blank=True)
    # card_masked_number = models.CharField(null=True, blank=True, max_length=255)
    #
    # def create_renew_order(self):
    #     """
    #     Create order for plan renewal
    #     """
    #     plan = self.user_plan
    #     return Order.objects.create(
    #         user=plan.user,
    #         plan=plan.plan,
    #         pricing=plan.recurring.pricing,
    #         amount=plan.recurring.amount,
    #         tax=plan.recurring.tax,
    #         currency=plan.recurring.currency,
    #     )

# class PlanPricingManager(models.Manager):
#     def get_query_set(self):
#         return super(PlanPricingManager, self).get_query_set().select_related('plan', 'pricing')


# class PlanPricing(models.Model):
#     plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
#     pricing = models.ForeignKey('Pricing', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=7, decimal_places=2, db_index=True)
#     order = models.IntegerField(default=0, null=False, blank=False)
#     has_automatic_renewal = models.BooleanField(
#         _('has automatic renewal'),
#         help_text=_('Use automatic renewal if possible?'),
#         default=False,
#     )
#
#     objects = PlanPricingManager()
#
#     class Meta:
#         ordering = ('order', 'pricing__period', )
#         verbose_name = _("Plan pricing")
#         verbose_name_plural = _("Plans pricings")
#
#     def __str__(self):
#         return "%s %s" % (self.plan.name, self.pricing)

from .signals import *
