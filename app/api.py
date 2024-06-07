from django.urls import re_path, path
from app.games.urls import GameViewSet
from app.users.views import UserViewSet
from app.files.views import FilesViewset
from rest_framework.routers import SimpleRouter

router = SimpleRouter()



router.register(r"games", GameViewSet)
router.register(r'users', UserViewSet)
router.register(r'files', FilesViewset)

urlpatterns = router.urls