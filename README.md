# PythonClassmates: Opinions d'étudiants en programmation python

Ce blog propose d'offrir une plateforme de publication collaborative maintenue par les étudiants et mentors du *discord* des étudiants **Python** d'*Openclassrooms*. L'objectif de ce dernier est de fournir des news, des didacticiels, des critiques de livres, des astuces en relation avec le langage de programmation python.

## Contribuer un nouvel article

Pour contribuer à ce blog, il n'y a besoin d'aucun outils particuler. Il faut juste posséder un compte guthub et commencer par faire un fork de ce dépôt. Ensuite, il fsut créer un fichier .rst ou .md dans content/articles pour accueillir votre nouvel article avec les en-têtes décrites ci-dessous. N'hésitez pas à consulter les autres articles en exemple. Vous pouvez ajouter votre nouvel article directement depuis github, ou consolter la section suivante pour apprendre à travailler en local sur son propre ordinateur.

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

Voici un article d'aide pour vous accompagner dans la [rédaction d'un article au format ReStructuredText](http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) (le format de markup officiel pour les projets python).

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

Voici un [article pour vous aider](https://guides.github.com/features/mastering-markdown/) si vous n'avez encore jamais rédigé de fichiers au format Markdown.

Une fois que votre article est terminé, vous pouvez demander sont ajout au blog collaboratif (ou sa modification si vous avez retouché article existant) en soumettant une **pull request** depuis l'interface github de votre fork du projet. Un admin s'occupera de son intégration. Voici un article pour vous aider à [créer une pull request](https://help.github.com/articles/creating-a-pull-request/).

## Rédiger un article en local



## Outils pour visualiser son article

Pour pouvoir visualiser son article, les dépendances à installer sont:

- Python 3.6+
- `$ pip3 install pipenv` ou `$ pip install pipenv` (sous windows)
- `$ pipenv install`

Pour générer le html statique à partir de l'article en ReStructuredText ou en Markdown:

- `$ pipenv run invoke build`

Pour visualiser son article sur [http://localhost:8000](http://localhost:8000):

- `$ pipenv run invoke runserver` (Vous pouvez arrêter le server en appuyant sur CTRL+C ou Cmd+C selon l'OS)
