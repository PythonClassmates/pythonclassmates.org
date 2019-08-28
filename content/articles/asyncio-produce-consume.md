Title: Producers / consumers avec asyncio
Date: 2019-08-28 15:30
Category: Articles
Tags: asyncio
Slug: asyncio-produce-consume
Author: Vianney


# Coroutines concurrentes

Quand on cherche à exécuter plusieurs coroutines en concurrence en Python
on pense tout de suite à `gather()` ou `as_completed()`.
C’est adapté quand on a un ensemble limité de coroutines à dérouler.
Par exemple :

```python
import asyncio
import random
 
async def cor():
    seconds = random.randint(0, 5)
    print(f'waiting {seconds}s...')
    await asyncio.sleep(seconds)
    print(f'waiting {seconds}s, done')
 
async def main():
    coroutines = (cor() for _ in range(10))
    await asyncio.gather(*coroutines)
 
asyncio.run(main())
```

# Pas plus de trois à la fois

Dans l’exemple précédent, on a instancié 10 coroutines, c’est raisonnable.
Si on n’en veut pas plus de 3 qui s’exécutent en concurrence,
on peut améliorer un peu le code des coroutines en les bordant
par un sémaphore commun :

```python
import asyncio
import random
 
async def cor(semaphore):
    async with semaphore:
        seconds = random.randint(0, 5)
        print(f'waiting {seconds}s...')
        await asyncio.sleep(seconds)
        print(f'waiting {seconds}s, done')
 
async def main():
    semaphore = asyncio.Semaphore(3)
    coroutines = (cor(semaphore) for _ in range(10))
    await asyncio.gather(*coroutines)
 
asyncio.run(main())
```

C’est élégant et ça peut être très pratique.
Par exemple si nos coroutines balancent des requêtes à un serveur,
on le fait poliment : pas plus de 3 à la fois.
Ça peut éviter de se faire jeter pour DoS.

# Produire et consommer

Maintenant, comment faire si nous avons un nombre très grand, voire infini,
de coroutines ?
Le `gather()` ou le `as_completed()` n’est plus adapté, puisqu’on ne veut pas instancier
ce très grand nombre de coroutines.
Il y a plusieurs façons de résoudre ce problème.
Voyons voir comment on peut s’en tirer avec une __queue__.

Une queue asyncio a les propriétés suivantes :

* on peut lui donner une taille maximale à l’instanciation. Sinon, elle a une taille infinie.
* on y ajoute un élément avec la coroutine `put(_item_)`. C’est une coroutine car elle bloque tant qu’il n’y a pas de place de libre dans la queue. S’il y a de la place, elle ajoute l’élément et rend directement la main, en synchrone, à l’appelant.
* on y récupère un élément avec la coroutine `get()`. C’est une coroutine car elle bloque tant que la queue reste vide. Le fait de récupérer un élément ne libère pas de place dans la queue. Il faut le faire de manière explicite en appelant la méthode `task_done()`.
* on peut attendre que la queue soit vide avec la coroutine `join()` : cela peut être très utile en fin de traitement (nous y reviendrons plus tard).

On crée donc une coroutine qui va alimenter la queue (le __producer__), et 3 autres qui vont la consommer (les __consumers__). Les consumers vont boucler indéfiniment. Par exemple :

```python
import asyncio
import random
 
async def producer(queue):
    for _ in range(10):
        seconds = random.randint(0, 5)
        await queue.put(seconds)
 
 
async def consumer(queue):
    while True:
        try:
            seconds = await queue.get()
            print(f'waiting {seconds}s...')
            await asyncio.sleep(seconds)
            print(f'waiting {seconds}s, done')
        finally:
            queue.task_done()
 
 
async def main():
    queue = asyncio.Queue(3)
    producer_ = producer(queue)
    consumers = (consumer(queue) for _ in range(3))
    await asyncio.gather(producer_, *consumers)
 
 
asyncio.run(main())
```

Ce qui donne en sortie :

```
...
waiting 3s, done
waiting 2s...
waiting 5s, done
waiting 5s, done
waiting 2s, done
```

Notez comment les consumers libèrent la queue dans un finally. C’est plus prudent.

# C’est bien mais c’est pas top

Ok, ça a l’air de marcher, sauf que… notre script reste coincé en boucle infinie.
Les consumers attendent sans fin de nouvelles valeurs dans la queue sauf que
le producer, lui, a fini son taf sans prévenir quiconque :
on est obligé de flinguer le process à coup de [ctrl-c].

Un autre truc moyen dans ce qu’on vient de faire, c’est que si un consumer plante,
le comportement par défaut du `gather()` est de laisser les autres tâches tourner.
On se trouve ainsi dans le risque d’un producer isolé sans aucun consumer derrière.
Il attendra comme un con que la queue soit consommée.

# `as_completed` à la rescousse ?

Le `gather()` rassemblant les consumers et le producer ne semble plus adapté.
En le remplaçant par un `as_completed()`, on peut récupérer la valeur de retour de la première coroutine à s’arrêter.
Si tout se passe bien, ce devrait être le producer.
Sinon, l’erreur sera correctement propagée :

```python
import asyncio
import random
 
async def producer(queue):
    for _ in range(10):
        seconds = random.randint(0, 5)
        await queue.put(seconds)
 
 
async def consumer(queue):
    while True:
        try:
            seconds = await queue.get()
            print(f'waiting {seconds}s...')
            await asyncio.sleep(seconds)
            print(f'waiting {seconds}s, done')
        finally:
            queue.task_done()
 
 
async def main():
    queue = asyncio.Queue(3)
    producer_ = producer(queue)
    consumers = (consumer(queue) for _ in range(3))
    for completed in asyncio.as_completed([producer_, *consumers]):
        await completed
        break
 
asyncio.run(main())
```

Notre expérience fonctionne en cas d’erreur 
(essayez en levant une erreur dans le consumer par exemple) :
le programme s’arrête brutalement, l’erreur est propagée.
Mais si tout se passe bien, les consumers resteront dans leur boucle infinie :
il nous faut un mécanisme d’arrêt des consumers.

De plus, le break juste après la fin du producer n’est pas très intelligent :
on arrête le traitement alors qu’il se peut qu’il reste des éléments non traités
dans la queue.
Nous devrions attendre que la queue soit vide avant de tout arrêter.

# Et finalement…

```python
import asyncio
import random
 
async def producer(queue):
    for _ in range(10):
        seconds = random.randint(0, 5)
        await queue.put(seconds)
 
 
async def consumer(queue):
    while True:
        try:
            seconds = await queue.get()
            print(f'waiting {seconds}s...')
            await asyncio.sleep(seconds)
            print(f'waiting {seconds}s, done')
        except asyncio.CancelledError:
            print("consumer STOP")
            return
        else:
            queue.task_done()
 
 
async def main():
    queue = asyncio.Queue(3)
    producer_ = producer(queue)
    consumers = [asyncio.create_task(consumer(queue)) for _ in range(3)]
    for completed in asyncio.as_completed([producer_, *consumers]):
        await completed
        break
 
    await queue.join()
    for c in consumers:
        c.cancel()
 
asyncio.run(main())
```

Vous aurez noté quelques changements :

* Les consumers ont maintenant une porte de sortie : en cas d’annulation, ils prennent fin.  Cela se fait en traitant spécialement l’erreur `CancelledError`.
* Nous attendons que la queue soit vide en attendant la coroutine `join`.
* Nous avons préféré créer des objets `Task` pour les consumers. En effet une `Task` est annulable, au contraire d’une coroutine. Le script se termine ainsi proprement.

> **Note :** les exemples de cet articles sont en python 3.7.
> En python 3.6 il faudra faire quelques ajustements.

> **Note 2 :** il n’y a pas de blague salace dans cet article.
