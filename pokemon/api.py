import requests

from pokemon.models import Pokemon, Stat, Type, PokemonStats, Evolution

API_URL = "https://pokeapi.co/api/v2"


def create_pokemon(id):
    response = requests.get("{api_url}/{node}/{id}".format(api_url=API_URL, node="pokemon", id=id)).json()
    pokemon_data = {
        'name': response.get('name'),
        'height': response.get('height'),
        'weight': response.get('weight'),
        'id_pokedex': response.get('id')
    }
    pokemon, _ = Pokemon.objects.get_or_create(
        **pokemon_data
    )
    for stat in response.get('stats'):
        name = stat.get('stat').get('name')
        value = stat.get('base_stat')
        stat, _ = Stat.objects.get_or_create(
            name=name,
        )
        if not pokemon.stats.filter(stats__name=name).exists():
            pokemon_stat = PokemonStats(stats=stat, value=value, pokemon=pokemon)
            pokemon_stat.save()

    for poke_type in response.get('types'):
        name = poke_type.get('type').get('name')
        pokemon_type, _ = Type.objects.get_or_create(
            name=name,
        )
        if not pokemon.types.filter(name=name).exists():
            pokemon.types.add(pokemon_type)
    pokemon.save()
    return pokemon


def create_evolves_chain(pokemon, evolves_to):
    evolution_chain = []
    for species in evolves_to:
        new_pokemon = create_pokemon(species.get('species').get('name'))
        method = species.get('evolution_details')
        evolution_data = {
            'evolution_method': method[0].get('trigger').get('name'),
            'evolution_object': (method[0].get('item') or {}).get('name', ""),
            'level': method[0].get('min_level')
        } if method else {}
        evolution_chain += create_evolves_chain(new_pokemon, species.get('evolves_to'))
        if not Evolution.objects.filter(preevolution_id=pokemon.id, evolution_id=new_pokemon.id).exists():
            evolution_chain.append(
                {
                    'preevolution_id': pokemon.id,
                    'evolution_id': new_pokemon.id,
                    **evolution_data
                }
            )

    return evolution_chain


def retrieve_and_create_pokemon(identifier):
    response = requests.get("{api_url}/{node}/{id}".format(api_url=API_URL, node="pokemon", id=identifier))
    response = requests.get(
        "{api_url}/{node}/{id}".format(api_url=API_URL, node="pokemon-species", id=response.json().get('id')))
    evolution_chain = requests.get(response.json().get('evolution_chain').get('url')).json().get('chain')
    pokemon = create_pokemon(evolution_chain.get('species').get('name'))
    chain = [Evolution(**data) for data in create_evolves_chain(pokemon, evolution_chain.get('evolves_to'))]
    Evolution.objects.bulk_create(chain)


if __name__ == '__main__':
    retrieve_and_create_pokemon("magikarp")
