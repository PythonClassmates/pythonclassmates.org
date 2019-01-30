# PythonClassmates

### Opinions d'étudiants en programmation python

---

Ce blog propose d'offrir une plateforme de publication collaborative maintenue par les étudiants et mentors du *discord* des étudiants **Python** d'*Openclassrooms*. L'objectif de ce dernier est de fournir des news, des didacticiels, des critiques de livres, des astuces en relation avec le langage de programmation python.

## Contribuer via l'interface _Github_

1. [Connectez-vous](https://github.com/login) à votre _Github_
2. Faites un fork du dépôt
3. Créez votre nouvel article (ou modifiez un existant) au format `rst` ou `md` dans `content/articles/`, l'en-têtes doit respecter le modèle correspondant au format choisi. (N'hésitez pas à consulter les autres articles en exemple) :

_Pour un article au format _ReStructuredText_, l'en-tête du fichier `.rst` doit suivre le format suivant :_

```restructuredtext
Le titre de mon article
#######################

:date: 2018-07-14 14:00
:modified: 2019-01-08 08:00
:category: Articles
:tags: tag1, tag2
:slug: le-titre-de-mon-article-sous-forme-de-slug
:author: Jean Dupont
:summary: Version courte de l'article

Voici un article d'aide pour vous accompagner dans la [rédaction d'un article au format ReStructuredText](http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) (le format de markup officiel pour les projets python).
```
_Pour un article au format _Markdown_, l'en-tête du fichier `.md` doit suivre le format suivant :_

```markdown
Title: Le titre de mon article
Date: 2018-07-14 14:00
Modified: 2019-01-08 08:00
Tags: tag1, tag2
Slug: le-titre-de-mon-article-sous-forme-de-slug
Author: Jean Dupont
Summary: Version courte de l'article

Voici un [article pour vous aider](https://guides.github.com/features/mastering-markdown/) si vous n'avez encore jamais rédigé de fichiers au format _Markdown_.
```

Une fois votre article terminé, demandez d'ajouter cette modification en soumettant une **pull request** (PR) depuis l'interface _Github_ (dans votre fork). Cette _PR_ sera traitée par un mainteneur du projet. Voici un article pour vous aider : [créer une pull request](https://help.github.com/articles/creating-a-pull-request/).

### Contribuer depuis votre ordinateur

1. Installez `git`
    * Pour _Mac OS_ et _Linux_, vous avez peut-être une version déjà installée, essayez  la commande `$ git --version` dans un terminal pour vous en assurer
    * Pour _Windows_, installez [Git For Windows](https://gitforwindows.org/) et [suivre ce cours](https://openclassrooms.com/fr/courses/2342361-gerez-votre-code-avec-git-et-github) si vous avez besoin de découvrir l'outil

2. Clonez votre _fork_ du projet avec de la commande `git clone <adresse-de-votre-fork>.git`
3. Ajoutez/modifiez un article comme indiqué ci dessus.
4. Poussez la modification sur github avec la commande `git push origin master`
5. Retournez sur la page d'accueil de votre _fork_ sur _Github_ un message vous invitera à créer une _PR_

## Outils pour visualiser son article

Pour pouvoir visualiser son article lors du développement local, les dépendances à installer sont:

- Python 3.6+
- `$ pip3 install pipenv` ou `$ pip install pipenv` (sous windows)
- `$ pipenv install`

Pour générer le html statique à partir de l'article en _ReStructuredText_ ou en _Markdown_:

- `$ pipenv run invoke build`

Pour visualiser son article sur [http://localhost:8000](http://localhost:8000):

- `$ pipenv run invoke runserver` (Vous pouvez arrêter le server en appuyant sur CTRL+C ou Cmd+C selon l'OS)
