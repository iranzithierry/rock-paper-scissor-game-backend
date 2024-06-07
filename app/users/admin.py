from django.contrib import admin
from app.users.models import User
from unfold.admin import ModelAdmin
from base.sites import app_admin_site
from django.shortcuts import redirect
from django.contrib import admin, messages
from django.contrib.auth.models import Group
from app.unfold.resources import UserResource
from unfold.decorators import action, display
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm


admin.site.unregister(Group)
# admin.site.unregister(BaseUser)

@admin.register(User, site=app_admin_site)
class UserAdmin(UserAdmin, ModelAdmin, ImportExportModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    resource_classes = [UserResource]    


    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'email',
                )
            },
        ),
        (_('Profile image'), {'fields': ('profile_picture',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ["display_header", "is_staff", 'date_joined','profile_picture',]

    import_form_class = ImportForm
    export_form_class = ExportForm

    @display(description=_("User"), header=True)
    def display_header(self, instance: User):
        return instance.username, instance.email

    actions_list = ["custom_actions_list"]
    actions_row = ["custom_actions_row"]
    actions_detail = ["custom_actions_detail"]
    actions_submit_line = ["custom_actions_submit_line"]

    @action(description="Custom list action", url_path="actions-list-custom-url")
    def custom_actions_list(self, request):
        messages.success(request, "List action has been successfully executed.")
        return redirect(request.META["HTTP_REFERER"])

    @action(description="Custom row action", url_path="actions-row-custom-url")
    def custom_actions_row(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(request.META["HTTP_REFERER"])

    @action(description="Custom detail action", url_path="actions-detail-custom-url")
    def custom_actions_detail(self, request, object_id):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {object_id}",
        )
        return redirect(request.META["HTTP_REFERER"])

    @action(description="Custom submit line action")
    def custom_actions_submit_line(self, request, obj):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {obj.pk}",
        )

@admin.register(Group, site=app_admin_site)
class GroupAdmin(GroupAdmin, ModelAdmin,):
    pass