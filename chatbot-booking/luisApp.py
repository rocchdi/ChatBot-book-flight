# on définit une classe de configuration DefaultConfig depuis un fichier config. on définit ensuite une fonction getLuisResponse
# qui envoie une requête HTTP GET à l URL LUIS spécifiée dans la classe de configuration, avec un query fournie en argument.
# La réponse reçue est ensuite convertie en objet JSON, qui est retourné par la fonction.

from config import DefaultConfig
import json
import requests

def getLuisResponse(query):
    CONFIG = DefaultConfig()

    url = CONFIG.LUIS_APP_URL
    url = url + '"' + query + '"'
    print(url)
    response = requests.get(url)
    data = response.json()

    return data