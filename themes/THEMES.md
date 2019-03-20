# Thèmes

Bienvenue dans la section des thèmes personnels. Ce guide a pour but de vous renseigner sur la méthode adoptée pour construire vos thèmes.

## I - Construire un thème Pelican

La documentation officielle est disponible [ici](http://docs.getpelican.com/en/3.6.3/themes.html).  
  
Nous reprenons la structure des thèmes visible dans la documentation. Nous vous conseillons d'importer les pages html du dossier [Simple theme](https://github.com/getpelican/pelican/tree/master/pelican/themes/simple/templates) pour avoir une base sur quoi travailler (Ce sont les pages du thème Pelican par défaut).

Si vous souaitez créer votre thème, créez un nouveau dossier dans le dossier `themes` avec la structure suivante :

```text
- static
    - css
    - scss
- fonts
- templates
- images
```

## II - L'usage du SCSS

Nous avons fait le choix d'utiliser SCSS pour produire nos styles. SCSS est une surcouche au langage CSS, dont la documentation est disponible [ici](https://sass-lang.com/guide).
  
>Note : nous utilisons la variante *SCSS* et non *SASS*. SCSS a l'avantage de reprendre la syntaxe de CSS, ce qui rend l'apprentissage plus facile.

Pour ce qui est du *Style Guide*, je recommande [cet article](https://sass-guidelin.es/fr/). Pour résumer, je recommande surtout de suivre [la règle des imbrications de sélecteur](https://sass-guidelin.es/fr/#imbrication-des-slecteurs). Le reste n'est pas indispensable.  
  
### Transformer son SCSS en CSS

Il vous faudra télécharger un programme parmis ceux donnés [dans la documentation officielle](https://sass-lang.com/install).  
Ensuite, ouvrez le fichier `tasks.py` de ce projet. En tête de ce fichier se trouve un dictionnaire `CONFIG` qui sert de configuration.  
Vous pouvez ajouter votre thème dans la partie `theme list`. Suivez l'exemple en commentaire.  
`CONFIG['theme:active']` permet de selectionner son thème. Modifiez sa valeur pour cibler le chemin du thème voulu.  
  
Une fois votre thème crée et/ou sélectionné, il vous suffira de lancer la commande `invoke scss` à la racine du projet pour générer vos fichiers scss en css.  

>Note : la commande `invoke upstyle` permet de convertir les fichiers scss, build le site et lancer le serveur en une seule commande.