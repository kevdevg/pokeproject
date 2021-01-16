from rest_framework import serializers

from pokemon.models import Pokemon, PokemonStats


class TypeSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_name(instance):
        return instance.name

    class Meta:
        fields = ['name']


class StatSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_name(instance):
        return instance.stats.name

    class Meta:
        fields = ['name', 'value']
        model = PokemonStats


class BasePokemonSerializer(serializers.ModelSerializer):
    @staticmethod
    def get_preevolution(instance):
        preevolution = instance.preevolutions.all().first()
        if preevolution:
            return {
                'level': preevolution.level,
                'evolution_method': preevolution.evolution_method,
                'evolution_object': preevolution.evolution_object,
                'pokemon': PrevolutionSerializer(preevolution.preevolution).data
            }
        return None

    @staticmethod
    def get_evolutions(instance):
        evolutions = instance.evolutions.all()
        return [
            {
                'level': evolution.level,
                'evolution_method': evolution.evolution_method,
                'evolution_object': evolution.evolution_object,
                'pokemon': EvolutionSerializer(evolution.evolution).data
            } for evolution in evolutions
        ]


class PrevolutionSerializer(BasePokemonSerializer):
    preevolution = serializers.SerializerMethodField()
    types = TypeSerializer(many=True)
    class Meta:
        model = Pokemon
        fields = ['name', 'height', 'weight', 'id_pokedex', 'preevolution', 'types']


class EvolutionSerializer(BasePokemonSerializer):
    evolutions = serializers.SerializerMethodField()
    types = TypeSerializer(many=True)
    class Meta:
        model = Pokemon
        fields = ['name', 'height', 'weight', 'id_pokedex', 'evolutions', 'types']


class PokemonSerializer(BasePokemonSerializer):
    preevolution = serializers.SerializerMethodField()
    evolutions = serializers.SerializerMethodField()
    stats = StatSerializer(many=True)
    types = TypeSerializer(many=True)

    class Meta:
        model = Pokemon
        fields = ['name', 'height', 'weight', 'id_pokedex', 'preevolution', 'evolutions', 'stats', 'types']
