Title: GHI - GitHub Issues
Date: 2018.11.29 21:21
Category: Articles
Slug: ghi-git-hub-issues
Author: Freezed


`ghi` : _GitHub Issues on the command line. Use your `$EDITOR`, not your browser._

CLI vs GUI, pour moi le choix est souvent vite fait. Du coup ça fait quelques temps que je gère dès que possible mes` issues `github en CLI à l'aide de [ghi](https://github.com/stephencelis/ghi), un client dédié aux `issues` GitHub éccrit en Ruby.

La vrai feature qui me manque est l'affectation d'un `project`, dommage… Mais sinon on fait des trucs directement en console qui font _vraiment_ gagner du temps :

Liste les `issues` & `pulls` open :

```shell
~/git/pythonclassmates.org $ ghi list
# PythonClassmates/pythonclassmates.org open issues
  19: License proposal ↑
  18: License proposal ↑
  16: Travis CI rollback has not been runned
  15: Installation HowTo
  14: About page is missing
  13: Error 404 on category/tutoriels.html
  12: Error 404 on category/news.html
```
Seulement les` issues `:

```shell
~/git/pythonclassmates.org $ ghi list --no-pulls
# PythonClassmates/pythonclassmates.org open issues
  16: Travis CI rollback has not been runned
  15: Installation HowTo
  14: About page is missing
  13: Error 404 on category/tutoriels.html
  12: Error 404 on category/news.html
```

Affiche l'`issue 14`
```shell
~/git/pythonclassmates.org $ ghi 14
#14: About page is missing
@freezed opened this issue 23 hours ago.   open

    With links to :
    - [ ] pelican
    - [ ] template
    - [ ] github

```

`--web` ouvre la page dans votre navigateur : `ghi list --web`, `ghi 14 --web`, etc.

Bien sûr `ghi edit …` permet d'en éditer une (!)

Et `ghi open …` d'en créer. Tellement pratique quand on code et que l'on tombe sur un bug, une idée, ou autre… Fini le _«Je noterai ça tout à l'heure»_ qu'on aura oublié dans 5 minutes. Là en 15s c'est plié. Et avec l'habitude on y met presque tout :

```shell
ghi open --claim --label bug --label test --message "Test de la class Adallas à améliorer

Et là avec le double quote on laisse une ligne et on peut ajouter tous les
commentaires utiles.

Bon si comme moi vous êtes des maniaque le l'historique de votre shell, arretez
vous après `--message` et vous pourrez éditer votre issue dans votre éditeur,
par ce que là votre historique va dérouiller…

Les check-box du GHFMD sont aussi possible :
- [ ] foo
- [ ] bar
- [ ] foobar

Et quand on a fini de raconter sa vie on ferme la double quote. Hoplà!"
```
Aller pour finir un petit one-liner en shell pour créer les` issues `à partir d'un fichier texte (`issues.txt`) que l'on aura rempli avec un titre d'issue par ligne. Idéal en début de projet quand on à toute la roadmap à renseigner…

```shell
$ cat issues.txt
test issue #11
test issue #22
Foobar
```
puis

```shell
$ IFS='';while read issue; do ghi open --claim --label test --message "${issue}";done < issues.txt
#32: test issue #11
@freezed opened this issue 0 seconds ago.   open
@freezed is assigned.  test

Opened on freezed/python.
#33: test issue #22
@freezed opened this issue 0 seconds ago.   open
@freezed is assigned.  test

Opened on freezed/python.
#34: Foobar
@freezed opened this issue 0 seconds ago.   open
@freezed is assigned.  test
```

Bon code!
