Title: Améliorez votre front-end avec Webpack
Date: 2019-03-28 13:00
Modified: 2019-03-28 13:00
Tags: web, front-end
Slug: ameliorez-votre-front-end-avec-webpack
Author: Mikael Briolet

# Django + Webpack : le front-end niveau supérieur

![webpakc logo](https://i0.wp.com/blog.js-republic.com/wp-content/uploads/2018/02/logo-webpack.png?fit=491%2C497)

Le front-end ne se limite pas à une utilisation basique de HTML, CSS et Javascript. Il existe une infinité de bibliothèques Javascript qui nous facilitent la vie ouvrent le champ des possibles.  
Ces bibliothèques Javascript sont aujourd'hui rendues accessibles via le gestionnaire de package [`npm`, ou "Node Package Manager"](https://www.npmjs.com/).  
Webpack vient ensuite en renfort, pour automatiser l'environnement front-end en transformant et assemblant les dépendances JS et les différents modules en un fichier unique. Ses possibilités sont d'ailleurs bien plus grandes, et il permet aussi d'intégrer le css, les images, les fonts...

## NPM, le pip du Javascript

NPM est le gestionnaire de packages Javascript le plus utilisé aujourd'hui. A la base concu pour gérer les modules Node.js, [une intégration backend du Javascript](https://nodejs.org/en/), des paquets comme Webpack ou Browserify ont permis de gérer les l'environnement front-end de manière élégante.
[Webpack est cependant plus populaire que browserify](https://stackshare.io/stackups/browserify-vs-webpack).

## Mise en place du projet

Dans le cadre de ce guide, nous allons créer un nouveau projet Django que nous appellerons "setupwebpack".

> Notez que si nous allons nous concentrer sur le framework Django, webpack s'intègre tout aussi bien dans d'autres configurations, comme Flask ou Pelican.

### Installation des dépendances

Nous utiliserons Python 3.6, ainsi que le gestionnaire d'environnement poetry.

> Note : poetry s'utilise comme pipenv, aussi si vous êtes plus à l'aise avec pipenv (ou un autre gestionnaire d'environnement virtuel), libre à vous d'utiliser le votre.

Nous auront aussi besoin de NodeJs et son gestionnaire de paquets npm, [à installer depuis cette adresse](https://nodejs.org/en/).

Créez enfin un nouveau dossier "setupwebpack" et ouvrez votre shell à sa racine. Lancez ensuite ce commandes :
```bash
poetry init # génère un nouvel environnement virtuel.
poetry add django # installe django.
poetry add -D pylint pydocstyle flake8 # parce que vous êtes des gens bien.
npm init -y # génère une fichier package.json ('-y' pour une configuration par défaut).
```

## La mise en place de Django

Nous allons initialiser django et créer deux vues simples, pour tester notre environnement front-end.  

Commencons par initialiser le projet Django :

```bash
poetry shell # On lance le shell dans l'environnement virtuel.
django-admin.py startproject project .
# N'oubliez pas le '.' pour éviter de créer un nouveau dossier.
mkdir apps # On crée un dossier apps pour ranger nos applications django.
```

> Note : Je nomme *project* le répertoire de base Django. Ce n'est pas une convention.

Comme nous rangeront nos applications dans le dossier `apps`, nous intégrons le chemin du dossier dans le fichier `project/settings.py` :

```python
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.realpath(os.path.join(BASE_DIR, 'apps'))
sys.path.append(APPS_DIR)

# ...
```

Ce qui nous permet d'ajouter nos applications dans `INSTALLED_APPS` sans avoir à préfixer le chemin par `apps/`.  
Continuons en initialisant notre première application :

```bash
poetry shell # Si ce n'est pas déjà fait.
cd apps
touch __init__.py
django-admin startapp home
cd ..
```

Ensuite :

```python
# settings.py

# ...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # my apps
    'home',
]

# ...
```

```python
# urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
]
```

Occupons nous maintenant de l'application `home` :

```bash
touch apps/home/urls.py
mkdir apps/home/templates
touch apps/home/templates/base.html
touch apps/home/templates/home.html
```

```python
# apps/home/urls.py

"""Home urls."""

from django.urls import path

from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
```

```python
# apps/home/views.py

"""Home views."""

from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    """Return the Home page."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """Return the context."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Home sweet home"
        return context
```

```html
<!-- apps/home/templates/base.html -->

<!doctype html>

<html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>SetupWebpack | {{ title }}</title>
    </head>

    <body>
        {% block content %}
        {% endblock %}

        {% load static %}
        <script src="{% static 'bundle.js' %}"></script>
    </body>

</html>
```

```html
<!-- apps/home/templates/home.html -->

{% extends "base.html" %}

{% block content %}

    <h1>Hello Webpack !</h1>

{% endblock %}
```

Et lançons les commandes d'initalisation du serveur :

```bash
python manage.py migrate
python manage.py runserver
```

Le résultat dans la console :

```bash
Performing system checks...

System check identified no issues (0 silenced).
March 28, 2019 - 16:40:58
Django version 2.1.7, using settings 'project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Parfait, le serveur tourne ! :)  
Allons voir sur [http://127.0.0.1:8000/](http://127.0.0.1:8000/) :

Un beau "Hello Webpack" s'affiche en guise d'acceuil.

> La mise en place de Django est terminé. Prenez toujours le temps de bien construire votre projet, même pour des projets de teste.

## La mise en place de webpack

On passe maintenant à webpack ! Dans le cadre de ce guide, nous allons utiliser le langage Typescript et SCSS. Nous allons aussi installer la bibliothèque Jest pour tester notre Typescript, ainsi que [chart.js](https://www.chartjs.org/docs/latest/), que j'ai choisi de tester pour l'occasion. ;)

> L'intérêt de webpack est, entre autre, de profiter des langages dit "surcouche" comme le SCSS ou le typescript. En effet, Webpack se chargera de transpiler ces surcouches en CSS et JS avant de les intégrer dans un seul fichier Js.

On commence donc par l'installation de webpack :

```bash
npm install webpack webpack-cli
touch webpack.config.js
```

Webpack se configure à partir d'un fichier appelé `webpack.config.js`. Nous allons donc créer la structure de base de ce fichier :

```javascript
// webpack.congig.js

var path = require('path');

module.exports = {
  entry: './assets/js/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'assets/dist')
  }
};
```

Dans ce début de configuration :

- on importe le module `path` pour gérer les chemins de fichiers.
- on exporte un object contenant plusieurs attributs dont :
    - `entry` : le chemin du fichier javascript qu'on fait lire à webpack.
    - `ouptut` : un objet qui renvoit le nom du fichier de sortie et son emplacement dans le projet.

On a ici la base de la structure de webpack. **Webpack, c'est juste un script qui prend un fichier en entrée et qui en génère un autre en sortie.**  

Appelons le module webpack :

```bash
npx webpack
# npx est la commande npm pour appeler un module.
```

On obtient en sortie :

```bash
Insufficient number of arguments or no entry found.
Alternatively, run 'webpack(-cli) --help' for usage info.

Hash: 8cba692fdb1abc7fcae0
Version: webpack 4.29.6
Time: 108ms
Built at: 2019-03-29 11:31:23

WARNING in configuration
The 'mode' option has not been set, webpack will fallback to 'production' for this value. Set 'mode' option to 'development' or 'production' to enable defaults for each environment.
You can also set it to 'none' to disable any default behavior. Learn more: https://webpack.js.org/concepts/mode/

ERROR in Entry module not found: Error: Can't resolve './assets/dev/index.js' in 'your\path\setupwebpack'
```

Webpack s'est bien lancé. Un message de vigilance nous informe qu'on a pas spécifié de "mode" pour le lancement, et Webpack utilise donc le mode "production". Les modes permettent de créer des comportement différents entre le developpement et la production. Par défaut, le code en mode production est "minifié", pour gagner de la mémoire.  
Enfin, un message d'erreur nous informe que le fichier d'entrée spécifié n'a pas été trouvé. Et en effet, on a spécifié dans la configuration un fichier qu'on a pas encore crée, réglons ça tout de suite :

```bash
mkdir assets
mkdir assets/dev
touch assets/dev/index.js
mkdir assets/dist
```

On a crée un dossier `assets` à la racine du projet qui va contenir les fichiers d'entrée et de sortie pour webpack, rangés dans les dossiers `dev` (pour développement) et `dist` (pour distribution).

Maintenant quand on lance

```bash
npx webpack
```

On observe que la compilation se passe sans soucis, et un fichier `bundle.js` est visible dans le dossier `assets/dist`. Quand on ouvre ce fichier, on y voit du code javascript minifié :

```javascript
!function(e){var t={};function r(n){if(t[n])return t[n].exports;var o=t[n]={i:n,l:!1,exports:{}};return e[n].call(o.exports,o,o.exports,r),o.l=!0,o.exports}r.m=e,r.c=t,r.d=function(e,t,n){r.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},r.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},r.t=function(e,t){if(1&t&&(e=r(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)r.d(n,o,function(t){return e[t]}.bind(null,o));return n},r.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return r.d(t,"a",t),t},r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},r.p="",r(r.s=0)}([function(e,t){}]);
```

C'est le code généré de base par Webpack. Attachons maintenant ce fichier `bundle.js` à notre template de base :

```html
<!-- apps/home/templates/base.html -->

...

    <body>
        <h1>Hello Webpack !</h1>
        <!-- Le reste du contenu -->

        {% load static %}
        <script src="{% static 'bundle.js' %}"></script>
    </body>

...
```

Et d'intégrer la récupération du fichier `bundle.js` avec la commande `collecstatic` de django

```python
# project/settings.py

# ...

STATICFILES_DIRS = [os.path.join('assets', 'dist'),]
```

### L'automatisation des tâches

Quand on utilise webpack, on a tendance à automatiser les commandes de lancement en passant par les scripts npm. Modifions notre fichier`package.json` :

```json
// package.json

{
  "name": "setupwebpack",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "dev": "webpack --mode=development",
    "build": "webpack --mode=production",
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "webpack": "^4.29.6",
    "webpack-cli": "^3.3.0"
  }
}
```

Ainsi quand on voudra lancer les commandes webpack, il nous suffira d'écrire :

- `npm run dev` pour une génération en mode développement.
- `npm run build` pour une génération en mode production.

> Astuce : la commande `npm run dev` va générer du code pour le développement, qui ne sera pas minifié. Aussi, vous pourrez vérifier vos modules JS séparemment depuis le navigateur (onglet "source" dans l'outil de développement de Chrome) avec l'apparition d'un dossier "webpack", ce qui reste très pratique pour débugguer.