# En el archivo urls.py de la aplicación api
from django.urls import include, path
from rest_framework.routers import SimpleRouter

# from rest_framework.authtoken.views import obtain_auth_token
from .views import Login, Logout, LotoApi, UserInfo

router = SimpleRouter()
# router.register(r"cinco", MiViewSet)


urlpatterns = []

urlpatterns = [
    # Define aquí tus rutas para la API general
    # path("players/", PlayerListView.as_view(), name="player-list"),
    # path('token/', obtain_auth_token, name='api_token_auth'),
    # path("cinco", UserApi.as_view(), name="api_create_user"),
    path("", include(router.urls)),
    path("loto/", LotoApi.as_view(), name="loto"),
    path("login/", Login.as_view(), name="login"),
    path("info/", UserInfo.as_view(), name="info"),

    path("logout/", Logout.as_view(), name="logout"),
]
