Title: Django + Webpack : le front-end niveau supérieur
Date: 2019-03-28 13:00
Modified: 2019-03-28 13:00
Tags: web, front-end
Slug: ameliorez-votre-front-end-avec-webpack
Author: Mikael Briolet

![webpakc logo](https://i0.wp.com/blog.js-republic.com/wp-content/uploads/2018/02/logo-webpack.png?fit=491%2C497)

Le front-end ne se limite pas à une utilisation basique de HTML, CSS et Javascript. Il existe une infinité de bibliothèques Javascript qui nous facilite la vie, ouvre le champ des possibles.  
Ces bibliothèques Javascript sont aujourd'hui rendues accessibles via le gestionnaire de package [`npm`, ou "Node Package Manager"](https://www.npmjs.com/).  
Webpack vient ensuite en renfort, pour automatiser l'environnement front-end en transformant et en assemblant les dépendances JS et les différents modules en un fichier unique. Ses possibilités sont d'ailleurs bien plus grandes, et il permet aussi d'intégrer le CSS, les images, les fonts...

# NPM, le pip du Javascript

NPM est le gestionnaire de packages Javascript le plus utilisé aujourd'hui. Au départ conçu pour gérer les modules Node.js, [une intégration backend du Javascript](https://nodejs.org/en/), des paquets comme Webpack ou Browserify ont permis de gérer l'environnement front-end de manière élégante.
[Webpack est cependant plus populaire que browserify](https://stackshare.io/stackups/browserify-vs-webpack).

# Mise en place du projet

Dans le cadre de ce guide, nous allons créer un nouveau projet Django que nous appellerons "setupwebpack".

> Notez que si nous allons nous concentrer sur le framework Django, Webpack s'intègre tout aussi bien dans d'autres configurations, comme Flask ou Pelican.

## Installation des dépendances

Nous utiliserons Python 3.6, ainsi que le gestionnaire d'environnement Poetry.

> Note : Poetry s'utilise comme Pipenv. Aussi, si vous êtes plus à l'aise avec Pipenv (ou un autre gestionnaire d'environnement virtuel), libre à vous d'utiliser le vôtre.

Nous aurons aussi besoin de NodeJs et son gestionnaire de paquets npm, [à installer depuis cette adresse](https://nodejs.org/en/).

Créez enfin un nouveau dossier "setupwebpack" et ouvrez votre shell à sa racine. Lancez ensuite ces commandes :

```bash
poetry init # génère un nouvel environnement virtuel.
poetry add django # installe django.
poetry add -D pylint pydocstyle flake8 # on installe les Linters.
npm init -y # génère une fichier package.json ('-y' pour une configuration par défaut).
```

# La mise en place de Django

Nous allons initialiser Django et créer une vue simple, pour tester notre environnement front-end.

Commencons par initialiser le projet Django :

```bash
poetry shell # On lance le shell dans l'environnement virtuel.
django-admin.py startproject project .
# N'oubliez pas le '.' pour éviter de créer un nouveau dossier.
mkdir apps # On créé un dossier apps pour ranger nos applications Django.
```

> Note : Je nomme _project_ le répertoire de base Django. Ce n'est pas une convention.

Comme nous rangerons nos applications dans le dossier `apps`, nous intégrons le chemin du dossier dans le fichier `project/settings.py` :

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

<!DOCTYPE html>

<html lang="fr">
  <head>
    <meta charset="utf-8" />
    <title>SetupWebpack | {{ title }}</title>
  </head>

  <body>
    <div class="banner">{% block banner %}{% endblock %}</div>

    <div class="content">{% block content %}{% endblock %}</div>
  </body>
</html>
```

```html
<!-- apps/home/templates/home.html -->

{% extends "base.html" %} {% block banner %}

<h1>Hello Webpack !</h1>

{% endblock %} {% block content %} {% lorem 5 %} {% endblock %}
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
<a href="{static}../extra/images/django_webpack/base.png" target="_blank">
<img src="{static}../extra/images/django_webpack/base.png" style="height: 100%; width: 100%; display: block;"></a>

Un beau "hello Webpack", suivi de [plusieurs paragraphes en latin](https://docs.djangoproject.com/fr/2.1/ref/templates/builtins/#lorem) s'affichent. Attention ceci-dit, ce tuto ne portera pas sur ces deux langages. Je vous laisse vous documenter pour en apprendre plus sur eux. ;)

# La mise en place de Webpack

On passe maintenant à Webpack ! Dans le cadre de ce guide, nous allons utiliser le langage [Typescript](https://www.typescriptlang.org/) et [SCSS](https://sass-lang.com/). Nous allons aussi installer [chart.js](https://www.chartjs.org/docs/latest/), que j'ai choisi de tester pour l'occasion.

> Note : l'intérêt de Webpack est, entre autres, de profiter des langages dits de "surcouche" comme le SCSS ou le typescript. En effet, Webpack se chargera de transpiler ces surcouches en CSS et JS avant de les intégrer dans un seul fichier Js.

> Note sur l'utilisation de Typescript : On aurait aussi pu utiliser Javascript ES6.

On commence donc par l'installation de Webpack :

```bash
npm install webpack webpack-cli --save-dev
# Le module "webpack" gère les fonctionnalités de Webpack,
# et le module "webpack-cli" gère l'affichage dans le shell.
touch webpack.config.js
```

Webpack se configure à partir d'un fichier appelé `webpack.config.js`. Nous allons donc créer la structure de base de ce fichier :

```javascript
// webpack.congig.js

const path = require("path");

module.exports = {
  entry: path.resolve(__dirname, "assets/dev/index.js"),
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "assets/dist")
  }
};
```

Dans ce début de configuration :

- on importe le module `path` pour gérer les chemins de fichiers.
- on exporte un object contenant plusieurs attributs dont :
  - `entry` : le chemin du fichier Javascript qu'on fait lire à Webpack.
  - `ouptut` : un objet qui renvoie le nom du fichier de sortie et son emplacement dans le projet.

On a ici la base de la structure de Webpack.  
**En fait Webpack, c'est juste un script qui prend un fichier en entrée et qui en génère un autre en sortie.**

Appelons le module "webpack" :

```bash
npx webpack
# npx est la commande npm pour appeler un module dans le shell.
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

Webpack s'est bien lancé. Un message de vigilance nous informe qu'on n'a pas spécifié de "mode" pour le lancement, et Webpack utilise donc le mode "production". Les modes permettent de créer des comportement différents entre le developpement et la production. Par défaut, le code en mode production est "minifié", pour gagner de la mémoire.  
Enfin, un message d'erreur nous informe que le fichier d'entrée spécifié n'a pas été trouvé. Et en effet, on a spécifié dans la configuration un fichier qu'on n'a pas encore créé, réglons cela tout de suite :

```bash
mkdir assets
mkdir assets/dev
touch assets/dev/index.js
mkdir assets/dist
```

On a crée un dossier `assets` à la racine du projet qui va contenir les fichiers d'entrée et de sortie pour Webpack, rangés dans les dossiers `dev` (pour développement) et `dist` (pour distribution).

Maintenant quand on lance :

```bash
npx webpack
```

On observe que la compilation se passe sans souci, et un fichier `bundle.js` est visible dans le dossier `assets/dist`. Quand on ouvre ce fichier, on y voit du code Javascript minifié :

```javascript
!(function(e) {
  var t = {};
  function r(n) {
    if (t[n]) return t[n].exports;
    var o = (t[n] = { i: n, l: !1, exports: {} });
    return e[n].call(o.exports, o, o.exports, r), (o.l = !0), o.exports;
  }
  (r.m = e),
    (r.c = t),
    (r.d = function(e, t, n) {
      r.o(e, t) || Object.defineProperty(e, t, { enumerable: !0, get: n });
    }),
    (r.r = function(e) {
      "undefined" != typeof Symbol &&
        Symbol.toStringTag &&
        Object.defineProperty(e, Symbol.toStringTag, { value: "Module" }),
        Object.defineProperty(e, "__esModule", { value: !0 });
    }),
    (r.t = function(e, t) {
      if ((1 & t && (e = r(e)), 8 & t)) return e;
      if (4 & t && "object" == typeof e && e && e.__esModule) return e;
      var n = Object.create(null);
      if (
        (r.r(n),
        Object.defineProperty(n, "default", { enumerable: !0, value: e }),
        2 & t && "string" != typeof e)
      )
        for (var o in e)
          r.d(
            n,
            o,
            function(t) {
              return e[t];
            }.bind(null, o)
          );
      return n;
    }),
    (r.n = function(e) {
      var t =
        e && e.__esModule
          ? function() {
              return e.default;
            }
          : function() {
              return e;
            };
      return r.d(t, "a", t), t;
    }),
    (r.o = function(e, t) {
      return Object.prototype.hasOwnProperty.call(e, t);
    }),
    (r.p = ""),
    r((r.s = 0));
})([function(e, t) {}]);
```

C'est le code généré de base par Webpack. Attachons maintenant ce fichier `bundle.js` à notre template de base :

```html
<!-- apps/home/templates/base.html -->

...

<body>
  <div class="banner">{% block banner %}{% endblock %}</div>

  <div class="content">{% block content %}{% endblock %}</div>

  {% load static %}
  <script src="{% static 'bundle.js' %}"></script>
</body>

...
```

Et d'intégrer la récupération du fichier `bundle.js` avec la commande `collecstatic` de Django

```python
# project/settings.py

# ...

STATICFILES_DIRS = [os.path.join('assets', 'dist'),]
```

## L'automatisation des tâches

Quand on utilise Webpack, on a tendance à automatiser les commandes de lancement en passant par les scripts npm. Modifions notre fichier`package.json` :

```json
// package.json

{
  "name": "setupwebpack",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "dev": "webpack --mode=development",
    "build": "webpack --mode=production"
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

Ainsi quand on voudra lancer les commandes Webpack, il nous suffira d'écrire :

- `npm run dev` pour une génération en mode développement.
- `npm run build` pour une génération en mode production.

> Astuce : la commande `npm run dev` va générer du code pour le développement, qui ne sera pas minifié. Aussi, vous pourrez visionner vos modules JS séparemment depuis le navigateur (onglet "source" dans l'outil de développement de Chrome) avec l'apparition d'un dossier "webpack", ce qui reste très pratique pour débugguer :
> <a href="{static}../extra/images/django_webpack/webpack_debug.png" target="_blank"> <img src="{static}../extra/images/django_webpack/webpack_debug.png" style="height: 100%; width: 100%; display: block;"></a>

Bon, vous allez me dire que taper à chaque fois `npm run dev`, pour visualiser les changements apportés, c'est lourd... Et pour ça, j'ai aussi une solution, la commande `watch` de Webpack :

```json
// package.json

{
  // ...
  "scripts": {
    "dev": "webpack --mode=development",
    "build": "webpack --mode=production",
    "watch": "webpack --watch --mode=development"
  }
  // ...
}
```

En tapant `npm run watch`, Webpack sera constament en alerte sur les changements apportés au fichier statiques utilisés, et recompilera automatiquement à chaque fois qu'un nouveau changement sera enregistré.

Faisons un rapide test en lancant `npm run watch` :

```javascript
// assets/dev/index.js

let test = "Un rapide test.";
```

On voit dans le shell que Webpack compile automatiquement lors de la sauvegarde :

```bash
Hash: 56c73a6c491e47da8193
Version: webpack 4.29.6
Time: 17ms
Built at: 2019-04-01 10:24:26
    Asset      Size  Chunks             Chunk Names
bundle.js  3.85 KiB    main  [emitted]  main
Entrypoint main = bundle.js
[./assets/dev/index.js] 37 bytes {main} [built]
```

## Transpiler le SCSS en CSS

Nous allons maintenant utiliser une fonctionnalité indispensable de Webpack : sa faculté à transpiler les langages lors de son éxecution. Pour compiler le SCSS en CSS, nous allons faire appel à plusieurs [loaders](https://webpack.js.org/concepts/loaders/) pour Webpack :

1. [sass-loader](https://github.com/webpack-contrib/sass-loader) pour la conversion du SCSS en CSS
1. [css-loader](https://github.com/webpack-contrib/css-loader) pour gérer l'importation des fichiers CSS depuis Javascript
1. [mini-css-extract-plugin](https://github.com/webpack-contrib/mini-css-extract-plugin) pour recréer les fichiers CSS.

Installons les dès maintenant :

```bash
npm i -D sass-loader node-sass css-loader mini-css-extract-plugin
# 'i' pour install, '-D' pour '--save-dev'. On peut installer plusieurs modules en une commande.
```

Maintenant modifions notre fichier `webpack.config.js` :

```javascript
// webpack.config.js

const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: path.resolve(__dirname, "assets/dev/index.js"),
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "assets/dist")
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css',
            chunkFilename: '[id].css',
        })
    ],
    module: {
    module: {
        rules: [{
            test: /\.scss$/,
            use: [
                MiniCssExtractPlugin.loader, // 3. Recrée les fichiers css à partir de leurs équivalents en Javascript.
                "css-loader", // 2. Converti les fichiers CSS en équivalents Javascript
                "sass-loader" // 1. Transpile le SCSS en CSS
            ],
            exclude: /node_modules/
        }]
    }
};
```

On observe plusieurs ajouts :

1. On importe le module `mini-css-extract-plugin`
1. On ajoute un tableau `plugins` dans notre objet principal, qui contient la configuration (très basique) de notre plugin `mini-css-extract-plugin`
1. On ajoute un objet `module` dans notre objet principal, qui s'occupe des transformations des codes sources lors d'une importation depuis notre fichier `index.js`.

Dans notre objet `module`, on spécifie un tableau `rules` qui va contenir des "règles" pour appliquer nos loaders. Chaque règle est définie dans un nouvel objet (nous avons donc créé un objet spécifique pour les règles de nos fichier .scss), et possède trois variables :

- `test` qui est une chaîne de type [Regex](https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Expressions_r%C3%A9guli%C3%A8res) qui va définir quels sont les fichiers pris en compte par cette règle
- `use` qui est un tableau qui définit les loaders à utiliser (Ils se résolvent du dernier au premier dans le tableau)
- `exclude`, qui est aussi une chaîne Regex, qui définit les fichiers/dossiers à ne pas tester (`node_modules` dans notre exemple).

Vous connaissez maintenant la structure classique d'un fichier `webpack.config.js`. A chaque fois que nous voudrons prendre en charge un nouveau type de fichier, nous ajouterons une nouvelle règle, et de nouveaux loaders. Le tableau `plugins` permet de configurer nos loaders, ou d'ajouter un nouveau comportement à Webpack via d'autres types de plugins.  
Les possibités sont immenses, mais la base restera toujours la même. ;)

C'est maintenant l'heure de tester notre configuration :

```bash
# Dans votre Shell :
touch assets/dev/main.scss
```

```scss
// assets/dev/main.scss

$banner: rgb(77, 162, 201);
$gray: rgb(75, 75, 75);
$green: rgb(52, 255, 154);

$content_padding: 5% 20% 0% 20%;

// Minimal reset style :
* {
  padding: 0;
  margin: 0;
}

// Some tests :
.banner {
  background-color: $banner;
  padding: 3%;
}

h1 {
  color: $gray;
  text-align: center;

  &:hover {
    color: $green;
    cursor: pointer;
  }
}

.content {
  font-size: 1.2em;
  padding: $content_padding;
  text-align: justify;
}
```

```javascript
// assets/dev/index.js

import "./main.scss";
```

```html
<!-- apps/home/templates/base.html -->

<!DOCTYPE html>

<html lang="fr">
  {% load static %}

  <head>
    <meta charset="utf-8" />
    <title>SetupWebpack | {{ title }}</title>

    <link rel="stylesheet" type="text/css" href="{% static 'main.css' %}" />
  </head>

  <body>
    <div class="banner">{% block banner %}{% endblock %}</div>

    <div class="content">{% block content %}{% endblock %}</div>

    <script src="{% static 'bundle.js' %}"></script>
  </body>
</html>
```

Si vous avez laissé la commande `npm run watch` en éxecution depuis tout à l'heure, alors les changements sont déjà sauvegardés. Sinon, c'est l'heure de la relancer. Si tout se passe bien, vous pouvez déjà constaté l'équivalent `.css` de notre fichier `main.scss` dans le répertoire `assets/dist` !  
Executez enfin `poetry run python manage.py runserver` pour visionner le port [http://127.0.0.1:8000/](http://127.0.0.1:8000/) :  
<a href="{static}../extra/images/django_webpack/avec_css.png" target="_blank">
<img src="{static}../extra/images/django_webpack/avec_css.png" style="height: 100%; width: 100%; display: block;"></a>

Tout fonctionne bien. :)

## Transpiler le Typescript en Javascript

La gestion du SCSS étant bien implémentée, nous allons maintenant passer au Typescript !  
Nous aurons besoin du module `typescript`, du loader [ts-loader](https://github.com/TypeStrong/ts-loader) et du linter `tslint` :

```bash
npm i -D typescript ts-loader tslint
tsc --init  # Génère le fichier de configuration de Typescript.
```

Spécifiez `"module": "es6"` dans le fichier `tsconfig.json`.

On passe maintenant une nouvelle règle à notre fichier `webpack.config.js` :

```javascript

        ...

        entry: path.resolve(__dirname, "assets/dev/index.ts"),

        ...

        rules: [{
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "sass-loader"
                ]
            },
            {
                test: /\.ts$/,
                use: 'ts-loader',
                exclude: /node_modules/
            }
        ],
        resolve: {
            extensions: ['.ts', '.js']
        }

        ...

```

Nous modifions aussi l'extension de notre fichier d'entrée en `index.ts`, qui est l'extension de Typescript, et nous ajoutons un nouvel objet `resolve`, qui va s'occuper de résoudre les extensions avant l'import (ce qui évite des bugs d'importation avec Typescript).

Assurez-vous de bien renommer `index.js` en `index.ts`. Ajoutons ensuite une fonction en typescript. Cette fonction sera propre à l'application `home`, nous l'ajouterons donc dans le dossier `assets` de cette application.

```bash
mkdir apps/home/assets
mkdir apps/home/assets/ts
mkdir apps/home/assets/scss
touch apps/home/assets/ts/main.ts
touch apps/home/assets/ts/_main.scss
```

```javascript
// apps/home/assets/ts/main.ts

export function homeSetup(): void {
  const content: Element | null = document
    .getElementsByClassName("content")
    .item(0);

  if (content) {
    content.addEventListener("click", () => flashyContent(content));
  }
}

function flashyContent(content: Element): void {
  const className: string = "flashy";

  if (!content.classList.contains(className)) {
    content.classList.add(className);
  } else {
    content.classList.remove(className);
  }
}
```

```javascript
// assets/dev/index.ts

import "./main.scss";

import { homeSetup } from "../../apps/home/assets/ts/main";

// Notez l'appel des différents modules en fonction de l'adresse de la page.
// Ce n'est pas une convention, mais plutot une astuce personnelle.
document.addEventListener(
  "DOMContentLoaded",
  () => {
    // Main function.
    const page = window.location.pathname;

    switch (page) {
      case "/": {
        homeSetup();
        break;
      }
    }
  },
  false
);
```

```scss
// assets/dev/main.scss

@import '../../apps/home/assets/scss/main';

...
```

```scss
// apps/home/assets/scss/_main.scss

$flashy_font: rgb(255, 0, 234);
$flashy_background: rgb(60, 255, 0);

.content {
  cursor: pointer;
}

.flashy {
  color: $flashy_font;
  background-color: $flashy_background;
}
```

Notre fonction indispensable est prête à être testée. Lancez `npm run watch` ainsi que votre serveur Django pour juger du (magnifique) résultat :
<a href="{static}../extra/images/django_webpack/avec_typescript.png" target="_blank">
<img src="{static}../extra/images/django_webpack/avec_typescript.png" style="height: 100%; width: 100%; display: block;"></a>

Quand nous cliquons sur le texte, nous avons bien ce changement de classe introduit par notre code Typescript. :)

## Ajoutons la bibliothèque Chart.js

Webpack possède un bel avantage, c'est qu'il incorpore les bibliothèques importées dans le fichier final. Du coup, tout est centralisé et condensé.

Pour commencer, installons la bibliothèque [chart.js](https://www.chartjs.org/docs/latest/) :

```bash
npm i -D chart.js
```

Et ajoutons ce petit joujou à notre projet (on va enfin avoir quelque chose de vraiment joli !) :

```javascript
// apps/home/assets/ts/main.ts

import Chart from "chart.js";

export function homeSetup(): void {
  ...

  initGraph();
}

...

function initGraph() {
  const ctx = document.getElementById("myChart");

  if (!ctx) {
    return;
  }

  const data = {
    datasets: [
      {
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
          "rgb(255, 206, 86)",
        ],
        borderColor: ["rgb(255, 255, 255)"],
        data: [10, 20, 30],
      },
    ],
    labels: ["Rouge", "Bleu", "Jaune"],
  };

  const graph = new Chart(ctx, {
    data,
    type: "polarArea",
  });
}
```

```html
<!-- apps/home/templates/home.html -->

{% extends "base.html" %} {% block banner %}

<h1>Hello Webpack !</h1>

{% endblock %} {% block content %} {% lorem 5 %}

<canvas id="myChart" width="400" height="400"></canvas>

{% endblock %}
```

Et voila le travail ! Lorsque Webpack génère le fichier de sortie, on peut voir que la bibliothèque chart.js a bien été incorporée :
<a href="{static}../extra/images/django_webpack/lib_code.png" target="_blank">
<img src="{static}../extra/images/django_webpack/lib_code.png" style="height: 100%; width: 100%; display: block;"></a>

Je passe les centaines de lignes restantes. :D  
Quand à notre site, un beau graph est maintenant visible :
<a href="{static}../extra/images/django_webpack/avec_chartjs.png" target="_blank">
<img src="{static}../extra/images/django_webpack/avec_chartjs.png" style="height: 100%; width: 100%; display: block;"></a>

Nous arrivons à la fin de ce tuto ! J'espère qu'il vous aura été utile, et si vous avez une question ou un problème, n'hésitez pas à me contacter sur le Discord ! Pareil, si vous voyez une coquille ou une erreur, on n'est jamais à l'abri d'un oubli. :)

A bientôt sur le site !
