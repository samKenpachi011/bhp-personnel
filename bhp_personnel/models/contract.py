from django.db import models
from dateutil.relativedelta import relativedelta
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from ..choices import CONTRACT_STATUS, CONTRACT_LENGTH


class Contract(BaseUuidModel, SiteModelMixin, models.Model):

    identifier = models.CharField(
        verbose_name='Identifier',
        max_length=36,
        null=True,
        blank=True)

    duration = models.CharField(
        verbose_name='Contract Duration',
        max_length=30,
        choices=CONTRACT_LENGTH)

    start_date = models.DateField(
        verbose_name='Contract Start Date',
        help_text='Beginning of New Contract')

    end_date = models.DateField(
        verbose_name='Contract End Date',
        help_text='End Date of Contract')

    due_date = models.DateField()

    status = models.CharField(
        verbose_name='Contract Status',
        max_length=30,
        null=True,
        choices=CONTRACT_STATUS,
        default='active')

    leave_days = models.IntegerField(
        verbose_name='Number of leave days',
        default=0)

    leave_balance = models.IntegerField(
        verbose_name='Number of leave days',
        default=0)

    contract_ended = models.BooleanField(
        default=False,
        null=True,
        blank=True)

    def __str__(self):
        return f'{self.identifier}, {self.start_date} - {self.end_date}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.leave_balance = self.leave_days
        self.due_date = self.end_date - relativedelta(months=3)
        super().save(*args, **kwargs)


class ContractExtension(BaseUuidModel):

    contract = models.ForeignKey(Contract, on_delete=PROTECT)

    ext_duration = models.IntegerField(
        verbose_name='Extension time period (in months)',)

    end_date = models.DateField(
        verbose_name='New Contract End Date',
        help_text='End Date of contract after extension',)

    class Meta:
        app_label = 'bhp_personnel'
        verbose_name = 'Contract Extension'
        verbose_name_plural = 'Contract Extension'
