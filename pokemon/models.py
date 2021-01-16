from django.db import models


class Stat(models.Model):
    name = models.CharField(max_length=100)


class Type(models.Model):
    api_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    double_damage_from = models.ForeignKey
    double_damage_to = models.ManyToManyField('self')
    half_damage_from = models.ManyToManyField('self')
    half_damage_to = models.ManyToManyField('self')
    no_damage_to = models.ManyToManyField('self')


class Pokemon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    height = models.FloatField()
    weight = models.FloatField()
    id_pokedex = models.IntegerField()
    types = models.ManyToManyField(Type)


class PokemonStats(models.Model):
    stats = models.ForeignKey(Stat, on_delete=models.CASCADE)
    value = models.IntegerField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='stats')


class Evolution(models.Model):
    preevolution = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="evolutions")
    evolution = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="preevolutions")
    level = models.IntegerField(null=True)
    evolution_method = models.CharField(max_length=100)
    evolution_object = models.CharField(max_length=100)
