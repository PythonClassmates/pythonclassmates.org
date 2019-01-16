Title: Installer Pelican
Date: 2019-01-09 15:29
Category: tuto
Lang: fr
Slug: installer-pelican
Tags: web, python, pelican
Summary: Installation rapide de _Pelican_
Author: Freezed

# Démarrage rapide

_C'est une traduction basique du [démarrage rapide](https://docs.getpelican.com/en/4.0.1/quickstart.html) officiel_

---

## Créez le répertoire

```python
mkdir -p ~/projects/yoursite
cd ~/projects/yoursite
```

## Créez un environnement virtuel

```python
virtualenv .venv -p /usr/bin/python3.6
source .venv/bin/activate
```

## Installez _Pelican_ et markdown (si besoin, optionnel)

```python
pip install pelican markdown
```

## Créez le squelette de l'arborescence

```python
pelican-quickstart
```

Pour les questions avec une réponse entre crochet, appuyez sur `Entrée` pour acceptez cette valeur. Quand il vous sera demandé le préfixe de votre URL, entrez votre nom de domaine comme indiqué (`http://example.com`).

## Créez un article

Vous ne pourrez lancer _Pelican_ tant qu'il n'y a pas d'article. Utilisez votre éditeur préféré pour créez votre premier article avec le contenu suivant :

```python
Title: My First Review
Date: 2010-12-03 10:20
Category: Review

Following is a review of my favorite mechanical keyboard.
```

Considerant que cet article est au format Markdown, enregistrez le en tant que `~/projects/yoursite/content/keyboard-review.md.`

## Générez le site

Toujours depuis le répertoire, lancez la commande _Pelican_ pour générez votre site

```python
pelican content
```
Votre site à été généré dans le répertoire `output`. Peut-être aurez vous un message d'alerte relatif aux _flux_, c'est normal en développement et vous pouvez l'ignorer

# Prévisualisation du site

Ouvrez une session de terminal depuis le répertoire d'installation  et lancez la commande suivante :
```python
pelican --listen
```

Rendez vous à l'adresse [http://localhost:8000/](http://localhost:8000/) à l'aide de votre navigateur, c'est parfait !
