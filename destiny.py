import urllib


class API:
    """
    class for interacting with the api
    """

    def __init__(self, token, session):
        self.token = token
        self.base_url = 'https://www.bungie.net/Platform/Destiny2/'
        self.headers = {'X-API-Key': token}
        self.session = session

    async def get_bungie_id_from_battlenet(self, battlenet):
        battlenet_encoded = urllib.parse.quote(battlenet)
        url = f'{self.base_url}SearchDestinyPlayer/4/{battlenet_encoded}'
        resp = await self.session.get(url, headers=self.headers)
        json = await resp.json()
        if not json['Response']:
            raise UserNotFound()
        return json['Response'][0]['membershipId']

    async def get_user_from_battlenet(self, battlenet):
        membership_id = await self.get_bungie_id_from_battlenet(battlenet)
        url = f'{self.base_url}4/Account/{membership_id}/Stats/'
        resp = await self.session.get(url, headers=self.headers)
        json = await resp.json()
        return User(json['Response'])


class User:
    def __init__(self, json):
        self.json = json
        self.time_played = json['mergedAllCharacters']['merged']['allTime']['secondsPlayed']['basic']['displayValue']
        self.highest_light = json['mergedAllCharacters']['merged']['allTime']['highestLightLevel']['basic'][
            'displayValue']
        self.kda = json['mergedAllCharacters']['results']['allPvP']['allTime']['efficiency']['basic']['displayValue']
        self.suicides = json['mergedAllCharacters']['merged']['allTime']['suicides']['basic']['displayValue']


class UserNotFound(Exception):
    pass
