# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from pokemon.models import Pokemon, Stat, Evolution
from pokemon.serializers import PokemonSerializer
from pokemon.tasks import create_pokemon


class PokemonDetailCreateView(generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    lookup_field = "name"

    def create(self, request, *args, **kwargs):
        pokemon = Pokemon.objects.filter(name=request.data.get('name')).first()
        if pokemon:
            return Response(PokemonSerializer(instance=pokemon).data)
        create_pokemon.delay(request.data.get('name'))
        return Response({'result': "creating"})
