Title: Réutiliser le composant messages d'erreurs .
Date: 2019-01-18 15:25
Modified: 2019-01-17 08:00
Category: Articles
Tags: Django, Forms, CBV
Slug: 
Author: Aurélia Gourbère


# Réutiliser un template d'affichage des messages d'erreurs de formulaire

## Contexte  

Pour éviter la redondance de l'affichage dans un gabarit des messages d'erreur d'un formulaire . Nous pouvons faire un template réutilisable.

## Template form_errors.html

Dans le cas où notre projet a plusieurs apps, nous faisons le choix de le mettre dans le répertoire core/template/form_erros.html

```
{% block content %}

          {% if form.errors %}
            {% for field in form.%}
                {% for error in field.errors %}
                    <div class="alert alert-danger">
                        <strong>{{ error|escape }}</strong>
                     </div>
                {% endfor %}
            {% endfor %}
            {% for error in form.non_field_errors %}
                <div class="alert alert-danger">
                <strong>{{ error|escape }}</strong>
                </div>
            {% endfor %}
        {% endif %}


{% endblock %}
```
 

## Réutilisation dans le reste du projet

Pour chaque formulaire du projet nous pouvons à présent appeler ce petit bout de code pour l'affichage des erreurs possibles générées par n'importe lequel de nos formulaires:

```
 <!--profile form-->
   <div class="col s7">
      <form action='{% url "musicians:update_data" %}' method="post"  >
         {% csrf_token %}

        {% include 'core/form_errors.html' with form=profil_form %}

         {{ profile_form.as_p }}
         <button class="btn-floating btn-large waves-effect waves-light " type="submit" >
         <i class="material-icons">check</i></button>

      </form>
   </div>
</div>
```

