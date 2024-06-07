from django.contrib import admin
from unfold.admin import ModelAdmin
from base.sites import app_admin_site
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)


admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


@admin.register(PeriodicTask, site=app_admin_site)
class PeriodicTaskAdmin(ModelAdmin):
    pass


@admin.register(IntervalSchedule, site=app_admin_site)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule, site=app_admin_site)
class CrontabScheduleAdmin(ModelAdmin):
    pass


@admin.register(SolarSchedule, site=app_admin_site)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule, site=app_admin_site)
class ClockedScheduleAdmin(ModelAdmin):
    pass
