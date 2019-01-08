Title: Les mocks avec unittest
Date: 2018-07-14 14:00
Category: Articles
Tags: python, unittest
Slug: les-mocks-avec-unittest
Author: Julien Nuellas

# Les Mocks avec Unittest

Malgré les blagues et les débats que l'on peut lire concernant les tests unitaires (si vous ne les avez pas encore vu, voici quelques [exemples](https://twitter.com/thepracticaldev/status/687672086152753152) qui donne le [sourire](https://twitter.com/MonkeyTestIt/status/958661917375172609)), les test unitaires sont largement utilisés et s'intègrent directement dans l'approche [TDD](https://fr.wikipedia.org/wiki/Test_driven_development).

Les test unitaires servent donc à tester un bout de son code de façon isolée et vérifier que ce dernier fasse bien le travail qui lui a été demandé.
Prenons l'exemple suivant, je dois créer un algorithme qui reçoit en entrée une liste de tuples composée d'un prénom, d'un âge et d'une taille et je dois le retourner sous forme d'un dictionnaire.

Pour tester ce code, je vais donc dans la réalisation de mon test simuler une fausse entrée (une liste de tuple) et indiquer le résultat attendu (le dictionnaire que je souhaiterais renvoyer). Je vais appliquer mon algorithme avec cette fausse entrée et comparer la sortie avec le résultat attendu. Si c'est pareil, le test est validé et si c'est pas pareil, faut retourner travailler.
C'est logique, c'est propre, c'est net. Malheureusement que faire si l'entrée en question provient d'une source externe comme une API par exemple ? Dans ce cas-là, on va avoir un peu plus de difficulté à simuler l'entrée. Autre point, comment fait-on si la sortie de l'algorithme consiste à envoyer un mail à l'utilisateur ? Pas évident non plus de comparer les résultats attendus.

Mais ne vous inquiétez pas pour autant, car vous n'êtes pas le premier à être confronté à ce type de problématiques et des solutions ont été trouvées pour y répondre. Et c'est justement l'objectif de cet article qui va vous présenter la magie des Mocks !

## Qu'est-ce qu'un Mock ?

Un Mock, comme son nom l'indique (et oui c'est de l'anglais) est un objet qui consiste à imiter un autre objet.
Conceptuel n'est-ce pas ? Tout simplement, un mock c'est ce qui va vous permettre de simuler un retour API sans vraiment appeler une API ou simuler un envoi d'email sans vraiment envoyer un email. Cela permet d'imiter pas mal de choses afin de vous permettre de réaliser vos tests unitaires de façon indépendante.

## Dans la pratique, ça donne quoi ?

Rien de mieux qu'un exemple pour appréhender un peu mieux ce concept.
Imaginons le besoin suivant : je développe un site qui a pour objectif d'identifier des produits de substitution meilleur pour la santé par rapport à un produit donné. Pour cela, je souhaite interroger via l'[API OpenFoodFacts](https://fr.openfoodfacts.org/data) les produits liés à une marque et compter le nombre de produits ayant une bonne note alimentaire.
Voici le code de ma classe (fichier app.py) :

```python
import urllib.error
import json

class OpenFoodFactsAPI:
    """
    Cette classe a pour objectif de récupérer les produits associée à une marque
    via l'API d'OpenFoodFacts et de compter le nombre de produits ayant une bonne
    note alimentaire.
    """

    def _get_product_from_api(self, brand):
        """
        Cette méthode a pour objectif de récupérer les 150 premiers produits liés
        à une marque via l'API OpenFoodFacts
        """

        payload = {
            'action' : 'process',
            'json' : '1',
            'tagtype_0' : 'brands',
            'tag_contains_0' : 'contains',
            'tag_0' : brand,
            'page_size' : '150',
            'page' : '1'
        }

        parameters = urllib.parse.urlencode(payload)
        url = "http://fr.openfoodfacts.org/cgi/search.pl"
        parameters = parameters.encode('utf-8')
        req = urllib.request.Request(url, parameters)

        try:
            response = urllib.request.urlopen(req)
            response_body = response.read().decode("utf-8")
            data = json.loads(response_body)
            return data
        except urllib.error.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except urllib.error.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)

    def count_product_numb(self, brand):
        """
        Cette méthode a pour objectif de dénombrer le nombre de produits ayant
        une bonne note alimentaire
        Il s'agit de la méthode à tester pour cette exercice
        """

        data = self._get_product_from_api(brand)
        healthy_product = 0
        for product in data["products"]:
            try:
                if product["nutrition_grade_fr"] == "a":
                    healthy_product += 1
            except:
                pass
        
        return healthy_product
```

### Objectif de mon test

Je souhaite tester ma méthode **count_product_numb()** afin de m'assurer que cette dernière me renvoie bien le bon nombre de produits ayant une bonne note alimentaire.
Dans notre cas, l'algorithme est censé travailler sur la donnée provenant de l'API récupérée via la méthode **_get_product_from_api()**. Hors, j'y vois deux problèmes pour mon test :
* D'un point de vue performance, si j'ai 150 tests qui font tous des appels externes, je ne suis pas prêt de visualiser les résultats de ces derniers.
* Je n'ai aucune idée du nombre de produits (dont des produits avec une bonne note alimentaire) que l'API va me renvoyer. Je pourrais bien évidemment faire le test à coté et les compter mais qui me dit que dans le temps, des produits ne seront pas rajouté ou supprimé ?

Du coup, pour tester ma méthode, il faudrait que je puisse simuler ce retour d'API pour avoir une donnée similaire à celle-ci.
Et bien, c'est tout l'intérêt des mocks justement.

### Mise en place de mon test

Pour mettre en place ce test, je vais utiliser le module unittest. L'avantage de ce module, c'est qu'il est directement intégré dans Python et qu'il dispose de la possibilité de mettre en place des mocks, et même de plusieurs façons différentes !

Je mets donc en place la structure de test suivante (fichier test_app.py) :

```python
from app import OpenFoodFactsAPI
from unittest import TestCase

class TestOpenFoodFactsAPI(TestCase):

    def test_count_product_numb(self):
        """
        La méthode qui doit tester le fonctionnement de ma méthode
        count_product_numb()
        """
        
        test_api = OpenFoodFactsAPI()
        result = 2
        self.assertEqual(self.test_api.count_product_numb('nutella'), result)

```

Il y déja quelques informations avec la structure de test présentée au-dessus. En effet, que se passe-t-il déjà ?
1. On importe dans une variable locale la classe **OpenFoodFactsAPI** afin de pouvoir l'utiliser dans notre test
2. On importe dans une variable locale la classe **TestCase** du module unittest dont notre classe de test va hériter afin de pouvoir notamment utiliser les méthodes de comparaison
3. On définit une méthode de test où :
    * on instancie un objet de la classe OpenFoodFactsAPI
    * on définie un résultat (ici 2)
    * on utilise la méthode assertEqual de la classe TestCase pour comparer le résultat renvoyé par la méthode **count_product_numb()** avec le résultat que l'on attend

Ne criez pas au scandale ! J'entend d'ici votre question. Pourquoi 2 comme résultat ? Comment sait-on que l'API va nous renvoyer deux produits avec une bonne note alimentaire ?
Et bien oui, on ne le sait pas... Vous voyez un peu l'impasse ? Pourtant, cette méthode doit absolument être testée car ce qu'elle renvoie sera utilisée à l'extérieur de la classe et il est donc important que cette dernière fasse bien le travail qui lui a été demandé.

Comment faire alors ?... Il faut que je puisse tester cette méthode en lui donnant en entrée un json similaire à ce qui est renvoyé par la méthode **_get_product_from_api()** comportant donc 2 produits avec une bonne note alimentaire. (J'aurais bien évidemment pu en choisir 3, 5 ou 10000). Voyons dans la suite de l'article comment faire.

### La solution sans utilisation d'un mock

Comment ??? On parle d'un sujet sur les mocks et on propose une solution sans mock ? Oui, je l'admets, c'est un peu culotté de ma part mais je pense que ce n'est pas inutile de la décrire car ça aide à comprendre un peu la logique de fonctionnement.

Regardons déjà la solution :

```python
from app import OpenFoodFactsAPI
from unittest import TestCase

class TestOpenFoodFactsAPI(TestCase):
    
    def test_count_product_numb(self):

        # On instancie un object de la classe OpenFoodFactsAPI
        healthy_product = OpenFoodFactsAPI()

        # On crée une méthode au sein de la méthode de test
        # Il définit juste un exemple de retour de la méthode _get_product_from_api()
        def fake_api_result(self):
            result = {
            "count": 6,
            "skip": 0,
            "page_size": "150",
            "page": 1,
            "products": [
                {
                    "product_name_fr" : "Ferrero boite de 30",
                    "nutrition_grade_fr": "a",
                },
                {
                    "product_name_fr" : "Ferrero Light sans sucre et sans goût",
                    "nutrition_grade_fr": "b",
                },
                {
                    "product_name_fr" : "Ferrero Rocher",
                    "nutrition_grade_fr": "e",
                },
                {
                    "product_name_fr" : "Ferrero couscous",
                    "nutrition_grade_fr": "a",
                },
                {
                    "product_name_fr" : "Ferrero chocolat praliné",
                    "nutrition_grade_fr": "d",
                },
                {
                    "product_name_fr" : "Ferrero à la fraise",
                    "nutrition_grade_fr": "c",
                },
                ]
            }
            return result

        # On assigne ensuite ce retour à la méthode ciblée
        healthy_product._get_product_from_api = fake_api_result

        # On fait le test de comparaison
        self.assertEqual(healthy_product.count_product_numb("ferrero"), 2)
```

Et voilà le travail ! On utilise ici le caractère dynamique de Python ainsi que ces règle de portées de variables pour "forcer" le retour de la méthode **_get_product_from_api**. De cette façon, la méthode **count_product_numb()** va utiliser le dictionnaire défini et retourné par la méthode **fake_api_result()** pour compter le nombre de produit ayant une bonne note.

Alors c'est super et ça fonctionne mais imaginons maintenant que l'on ait à mocker plusieurs éléments, cela risque de rendre le code difficilement lisible et il doit y avoir une méthode plus sympa que de créer des méthodes imbriquées.
Et bien oui, c'est le cas. Voyons maintenant deux autres façons de faire en utilisant l'object **Mock** du module unittest, puis de son décorateur **patch**.

### Utilisation de la classe Mock

Unittest propose une classe Mock permettant de "mocker" facilement une classe, un objet ou une méthode. Cela permet d'indiquer au processus de test que cet objet est une imitation et on va pouvoir agir dessus par l'intermédiaire des méthodes de la classe Mock (comme par exemple lui retourner une valeur !).

Voyons ce que cela donne :

```python
from app import OpenFoodFactsAPI
from unittest import TestCase
from unittest.mock import Mock

class TestOpenFoodFactsAPI(TestCase):

    def test_count_product_numb(self):

        api_response = {
            "count": 6,
            "skip": 0,
            "page_size": "150",
            "page": 1,
            "products": [
                {
                    "product_name_fr" : "Ferrero boite de 30",
                    "nutrition_grade_fr": "a",
                },
                {
                    "product_name_fr" : "Ferrero Light sans sucre et sans goût",
                    "nutrition_grade_fr": "b",
                },
                {
                    "product_name_fr" : "Ferrero Rocher",
                    "nutrition_grade_fr": "e",
                },
                {
                    "product_name_fr" : "Ferrero couscous",
                    "nutrition_grade_fr": "a",
                },
                {
                    "product_name_fr" : "Ferrero chocolat praliné",
                    "nutrition_grade_fr": "d",
                },
                {
                    "product_name_fr" : "Ferrero à la fraise",
                    "nutrition_grade_fr": "c",
                },
            ]
        }

        healthy_product = OpenFoodFactsAPI()
        healthy_product._get_product_from_api = Mock()
        healthy_product._get_product_from_api.return_value = api_response

        self.assertEqual(healthy_product.count_product_numb("ferrero"), 2)
```

Il y a plusieurs étapes derrière ce code :
1. On importe tout d'abord la classe Mock du module unittest
2. On définit la valeur de retour de l'API représentée ici par la variable api_response
3. On mock la méthode get_product_from_api de l'objet healthy_product
4. On lui associe la valeur de retour via la méthode return.value
5. On utilise la méthode assertEqual() de la classe TestCase afin de comparer le retour de la méthode que l'on teste avec le résultat attendu

A noter qu'il est possible de fusionner le point 3 et 4 en une seule fois en utilisant l'argument return_value lorsque la méthode est mockée :

```python
healthy_product._get_product_from_api = Mock(return_value=api_response)
```

### Utilisation du décorateur patch

Une des autres façons de mettre en place un mock avec unittest est d'utiliser son décorateur patch.
Ce décorateur permet - comme son nom l'indique - de 'patcher' un objet uniquement au sein de la fonction à laquelle elle est appelée. En effet, cela gère automatiquement le 'dé-patching' même si des exceptions sont levées.

Voyons un peu ce que cela donne :

```python
from app import OpenFoodFactsAPI
from unittest import TestCase
from unittest.mock import patch

class TestOpenFoodFactsAPI(TestCase):

    @patch('app.OpenFoodFactsAPI._get_product_from_api')
    def test_count_product_numb(self, mock_get_product_from_api):

        mock_get_product_from_api.return_value = {
            "count": 6,
            "skip": 0,
            "page_size": "150",
            "page": 1,
            "products": [
                {
                    "product_name_fr" : "Ferrero boite de 30",
                    "nutrition_grade_fr": "a",
                },
                {
                    "product_name_fr" : "Ferrero Light sans sucre et sans goût",
                    "nutrition_grade_fr": "b",
                },
                {
                    "product_name_fr" : "Ferrero Rocher",
                    "nutrition_grade_fr": "e",
                },
                {
                    "product_name_fr" : "Ferrero couscous",
                    "nutrition_grade_fr": "a",
                },
                {
                    "product_name_fr" : "Ferrero chocolat praliné",
                    "nutrition_grade_fr": "d",
                },
                {
                    "product_name_fr" : "Ferrero à la fraise",
                    "nutrition_grade_fr": "c",
                },
                ]
        }

        healthy_product = OpenFoodFactsAPI()
        self.assertEqual(healthy_product.count_product_numb("ferrero"), 2)
```

Décrivons également les différentes étapes :
1. On importe le décorateur patch du module unittest
2. On met en place le décorateur qui prend en argument l'objet à mocker
3. Le décorateur injecte l'objet mocker au sein de la fonction comme un argument de la méthode. Le nom de l'argument est libre de choix. Ici, il s'agit de l'argument **mock_get_product_from_api**.
4. On utilise la méthode return_value pour associer la valeur de retour souhaitée au mock.
5. On instancie un objet via la classe OpenFoodFactsAPI()
6. On utilise la méthode assertEqual de la classe TestCase pour comparer la valeur renvoyée par la méthode que l'on teste avec le résultat attendu

Petite remarque supplémentaire, attention à ne patcher uniquement que la méthode que l'on souhaite mocker et non la classe entière.
En effet, en faisant comme ceci :

```python
...
class TestOpenFoodFactsAPI(TestCase):

    @patch('app.OpenFoodFactsAPI')
    def test_count_product_numb(self, mock_OpenFoodFactsAPI):
        mock_OpenFoodFactsAPI._get_product_from_api.return_value = {
            "count": 6,
            "skip": 0,
            "page_size": "150",
            ...
```

Le mock ne fonctionnera pas. En effet, unittest va créer un grand objet mock sur l'ensemble de la classe et ne dissociera pas la partie de la classe qui doit être imitée et celle qui ne le doit pas.
Du coup, lors du lancement du test, l'appel à l'API sera réalisé et la méthode **count_product_numb** sera appliquée sur la donnée renvoyée par l'API et non celle que l'on a configurée. 

Attention donc à bien mocker le périmètre que l'on souhaite imiter.

## Quelle solution choisir au final ?

Et bien, de mon côté, j'ai une préférence pour l'utilisation du décorateur **patch** car je trouve que le code est plus lisible et cela m'assure surtout que le mock ne sera actif que durant le test de ma méthode car comme indiqué plus haut, il gère automatiquement la destruction du mock à la fin du test.
En revanche, l'utilisation de la classe Mock n'est pas dénué d'intérêt lorsque plusieurs tests (donc plusieurs méthodes) doivent faire appel au même objet à mocker. J'aurais plus tendance à utiliser cette solution dans ce type de cas en définissant mon objet mockée dans une méthode *SetUp*.

Mais au final, il n'appartient qu'à vous de choisir. Les goûts et les couleurs, ça ne se discute pas !

## Pour faire quelques tests

Si vous souhaitez faire quelques tests sur l'exemple de l'article, vous pouvez retrouver le code source à cette adresse :
<https://github.com/JN-Lab/Test-Mock-Unittest>

Il y a différents fichiers de tests avec différentes méthodes appliquées dont une qui ne fonctionnent pas et qui faitréférence au danger expliqué plus haut.

J'espère en tout cas que cet article vous aura permis d'y voir un peu plus clair sur la façon de mettre en place des mocks avec le module unittest.

Bon codage à tous !
