from import_export import resources

from app.users.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
