Title: Présentation de la librairie requests
Date: 2019-01-31 16:00
Modified: 2019-01-31 16:00
Category: Tutoriels
Tags: requests
Slug: presentation-requests
Author: Cédric Migazzi

# Présentation de la librairie requests.

### Présentation

`requests` est une librairie Python qui permet de gérer facilement les requêtes HTTP. Elle utilise la librairie standard `urllib3` et en simplifie l'utilisation pour la rendre plus "humaine" ([*HTTP for humans*](http://docs.python-requests.org/en/master/)).

Pour cet article, nous allons voir un usage basique de dialogue avec  l'API d'[OpenFoodFacts](https://fr.openfoodfacts.org/).

>*"OpenFoodFacts est une base de données sur les produits alimentaires faite par tout le monde, pour tout le monde"*
>
Le site dispose d’une API dont la documentation se trouve [ici](https://en.wiki.openfoodfacts.org/API). Il est ainsi possible de faire toutes sortes de recherches, de récupérer les données avec `requests` et de les exploiter avec Python.

### Installation
`pipenv install requests`

### Une simple requête

Pour réaliser une requête:

avec `urllib3`...
```
import urllib3

http = PoolManager()
res = http.request("GET", "https://fr.openfoodfacts.org/")
```
... et pour obtenir le même résultat avec `requests`:
```
import requests

res = requests.get("https://fr.openfoodfacts.org/ ")
```
C'est effectivement beaucoup plus simple, mais que se passe-t-il ?

Dans les 2 cas, `res` contient la réponse du serveur HTTP.

Avec `requests`, l’import de `http` et l’instanciation de `PoolManager()` est transparent pour l’utilisateur, ce qui économise du code. Les méthodes HTTP sont des méthodes de `requests` au lieu d'être des paramètres dans `urllib3`. 

On peut aussi faire de même avec les autres méthodes HTTP :
```
res = request.post("https://mon-url.de/post", data={key:value})
res = request.put("https://mon-url.de/put", data={key:value})
res = request.delete("https://mon-url.de/delete")
res = request.head("https://mon-url.de/get")
res = request.head("https://mon-url.de/get")
```

**Et qu'est-ce qu'on en fait ?**

`requests` renvoie un objet `Response` qui possède les attributs suivants:
```
# le code HTTP de la réponse
>>> res.status_code
200

# l'url
>>> res.url
'https://fr.openfoodfacts.org/'

# les headers HTTP.
>>> res.headers # dictionnaire

#l'encodage
>>> res.encoding
'UTF-8'
```
Et quelques méthodes de base:

```
# le code html
>>> res.text # chaine de charactère

# Si la réponse est au format json, on peut la convertir en dictionnaire
>>> res.json()
```

### Un premier exemple:

Petit exemple avec du Nutella que l’on peut retrouver grâce à son code barre : 3017620425400.
```
>>>res = requests.get("https://world.openfoodfacts.org/api/v0/product/3017620425400.json")
```
Comme la réponse est au format json, on peut le transformer en dictionnaire:
```
>>>results = res.json()

# voir toutes les clés
>>>results.keys()
dict_keys(['code', 'status_verbose', 'product', 'status'])

# faire un dictionnaire du produit
>>> product = results["product"]

# voir le nombre d'attributs du produit
>>> len(prodcut)
191

# et par exemple, voir les catégories qui lui sont associé
>>>product["categories"]
'Petit-déjeuners, Produits à tartiner, Produits à tartiner sucrés, Pâtes à tartiner, Pâtes à tartiner au chocolat, Pâtes à tartiner aux noisettes et au cacao, Pâtes à tartiner aux noisettes'
```

### Ajouter des paramètres

Pour des requêtes plus claires, il est possible de passer une liste d'objets  clé/valeur en paramètre de la requête.

Avec l'API d'OpenFoodFacts, il est possible de le mettre en pratique grâce à son url de recherche:

*Vous trouverez toutes les options de recherche sur la [doc officielle](https://en.wiki.openfoodfacts.org/API/Read/Search#Parameters)*

```
>>>payload = {"search_terms": "Lindt, "json":1}
>>>res = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)

# Pour voir l'url correspondante
>>>res.url
'https://fr.openfoodfacts.org/cgi/search.pl?search_terms=Lindt&json=1'

# pour voir le nombre de résultats
>>> results = res.json()
>>> results["count"]
802
```
Si on veut retrouver les 50 produits les plus populaires de la marque Lindt, on pourra faire:
```
>>>payload = {"search_terms": "Lindt",
...           "search_tag": "brands", 
...	          "sort_by": "unique_scans_n",
...	          "page_size": 50, 
...	          "json": 1}
>>>res = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)

# l'url correspondante
>>>res.url
'https://fr.openfoodfacts.org/cgi/search.pl?search_terms=Lindt&search_tag=brands&sort_by=unique_scans_n&page_size=50&json=1'

# on peut ensuite récupérer les produits
>>>results = res.json()
>>>products = results["products"]
 
# Et afficher leurs noms
>>>for product in products:
	print(product["product_name"])
```
### Pour aller plus loin

Nous avons vu un usage basique de `requests`, mais il est aussi possible de:

- vérifier si la réponse HTTP est valide:
```
>>> res = requests.get('https://fr.openfoodfacts.org')
>>> res.status_code == requests.codes.ok
True
```
- voir et gérer les redirections (HTTP vers HTTPS) avec l'attribut `history`:

```
res = requests.get("http://fr.openfoodfacts.org/")
>>> res.status_code
200
>>> res.history
[<Response [301]>]

# Poosibilité de désactiver les redirections
res = requests.get("http://fr.openfoodfacts.org/", allow_redirects=False)
>>> res.status_code
301
>>> res.history
[]
```

- personnaliser les headers d'une requête en passant un dictionnaire:
```
url = "http://fr.openfoodfacts.org/"
headers = {"user-agent": "python-app/0.0.1"}
>>>res = requests.get(url, headers=headers)
```
- retrouver facilement la valeur d'un header:
```
>>>res.headers["content-type"]
'text/html; charset=UTF-8'
```

- Et pleins d'autres choses avec les cookies, les certificats SSL ou encore les requêtes préparées que vous retrouveregit checkz sur la [doc officielle](http://docs.python-requests.org/en/master/user/advanced/)

### Conclusion
`requests`  est une librairie simple d'utilisation et très complète. Que ce soit pour un usage basique (comme on vient de voir) ou plus avancé, c'est la librairie conseillée pour effectuer des requêtes HTTP.

