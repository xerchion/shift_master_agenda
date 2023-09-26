from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import DecimalField, F, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from rest_framework import generics, status  # viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes
# from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated  # AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from calendario4.models import MyUser
from loto.controllers.LotoController import LotoController
from loto.controllers.PlayerTurn import PlayerTurn
from loto.models import Player

# En api/views.py
from .serializers import (BetsSerializer, RankingSerializer, TurnsSerializer,
                          UserSerializer)

# @api_view(["POST"])  # Esto permite tanto GET como POST
# def user_profile(request):
#     user = request.user
#     serializer = UserSerializer(user)
#     return Response(serializer.data)


# codigo de pruebas pero no integrado en API real
class UserApi(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request)
        if serializer.is_valid():
            # user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# codigo de pruebas, pero no integrado en api real
class PlayersViewApi(generics.ListCreateAPIView):
    queryset = Player.objects.annotate(
        total_prize=Coalesce(
            Sum(F("prize__amount"), output_field=DecimalField()),
            Value(0, output_field=DecimalField()),
        )
    ).values("name", "total_prize")

    # queryset = Player.objects.all()
    # serializer_class = PlayerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = TokenAuthentication
    # basename = "Player"  # Especifica el basename manualmente


# @authentication_classes([TokenAuthentication])
# class PlayerListView(APIView):
#     permission_classes = [AllowAny]  # Esto permitirá el acceso sin autenticación

#     def get(self, request):
#         players = Player.objects.all()
#         serializer = PlayerSerializer(players, many=True)
#         return Response(serializer.data)


# funciona
@authentication_classes([TokenAuthentication])
class LotoApi(APIView):
    def get(self, request, format=None):
        print("llega al metodo de get de LotoApi")
        # Aquí puedes acceder al token con self.request.auth
        # Tu lógica para la vista protegida aquí
        date_now = datetime.now()
        ranking = LotoController().get_players_prizes()
        bets = LotoController().get_bets()
        turns = PlayerTurn(date_now).generate_list_turns()
        from loto.models import Prize

        jackpot = Prize.calculate_total_prizes()
        ranking_serialized = RankingSerializer(ranking, many=True).data
        bets_serialized = BetsSerializer(bets).data
        turns_serialized = TurnsSerializer(turns).data
        jackpot_serialized = jackpot

        all_loto_data = {
            "ranking": ranking_serialized,
            "bets": bets_serialized,
            "turns": turns_serialized,
            "jackpot": jackpot_serialized,
        }
        return Response(all_loto_data)


# Login bueno
class Login(APIView):
    def post(self, request, format=None):
        print("llega al post")
        username = request.data.get("username")
        password = request.data.get("password")

        print("usuario entrando", username, password)
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(self.request, user)
            print("usuario logeado con exito", user.is_authenticated)

            # TODO haz la logica de creacion de token si created es True, el usuario es nuevo
            """  Si created es True, significa que el objeto fue recién creado en la base de datos.
                 Si created es False, significa que el objeto ya existía en la base de datos."""
            return Response({"token": token.key})

        else:
            print("entra en el else")
            return Response({"error": "Credenciales no válidas"})


# login antiguo, con su propio html y form
class xLogin(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("api:persona-list")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        token, _ = Token.objects.get_or_create(user=user)
        if token:
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)
        else:
            print("usuario sin token")


# sin aplicar aun en vue
class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)


# Codigo para devolver datos del user
# ver si con el token se autentica


# funciona
# Aplicalo a la lista de premiados
@authentication_classes([TokenAuthentication])
class UserInfo(APIView):
    def get(self, request, format=None):
        print("llega al metodo de get de UserInfo")
        usuario = self.request.user
        print(type(usuario), "este es el tipo de usuario")
        print(usuario.password)
        print("Usuario: ", usuario)
        # Aquí puedes acceder al token con self.request.auth
        # token = self.request.auth
        # Tu lógica para la vista protegida aquí
        team = MyUser.objects.get(name=usuario).team
        return Response({"team": f"{team}"})
