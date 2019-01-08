# PythonClassmates: Opinions d'étudiants en programmation python

Ce blog propose d'offrir une plateforme de publication collaborative maintenue par les étudiants et mentors du *discord* des étudiants ***DA Python*** et ***Data Scientists*** d'*Openclassrooms*. L'objectif de ce dernier est de fournir des news, des didacticiels, des critiques de livres, des astuces en relation avec le langage de programmation python.

## Contribuer

Pour contribuer à ce blog, il n'y a besoin d'aucun outils particuler. Il suffit de rédiger un article en commençant par créer un fichier .rst ou .md dans content/articles. 

Pour un article au format ReStructuredText, l'en-tête du fichier .rst doit suivre le format suivant:
```
Le titre de mon article
#######################

:date: 2018-07-14 14:00
:modified: 2019-01-08 08:00
:category: Articles
:tags: tag1, tag2
:lug: le-titre-de-mon-article-sous-forme-de-slug
:author: Jean Dupont
:summary: Version courte de l'article
```

Pour un article au format Markdown, l'en-tête du fichier .md doit suivre le format suivant:
```
Title: Le titre de mon article
Date: 2018-07-14 14:00
Modified: 2019-01-08 08:00
Category: Articles
Tags: tag1, tag2
Slug: le-titre-de-mon-article-sous-forme-de-slug
Author: Jean Dupont
```

## Outils pour visualiser son article

Pour pouvoir visualiser son article, les dépendances à installer sont:

- Python 3.6+
- `$ pip3 install pipenv` ou `$ pip install pipenv` (sous windows)
- `$ pipenv install`

Pour générer le html statique à partir de l'article en ReStructuredText ou en Markdown:

- `$ pipenv run invoke build`

Pour visualiser son article sur [http://localhost:8000](http://localhost:8000):

- `$ pipenv run invoke runserver` (Vous pouvez arrêter le server en appuyant sur CTRL+C ou Cmd+C selon l'OS)
