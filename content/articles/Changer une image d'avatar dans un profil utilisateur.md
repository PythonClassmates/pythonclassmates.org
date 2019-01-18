Title: Changer une image d'avatar dans un profil utilisateur
Date: 2019-01-18 09:50
Modified: 2019-01-08 08:00
Category: Articles
Tags: Django, Pillow
Slug: Changer-une-image-avatar-dans-un-profil
Author: Aurélia Gourbère


# Changer une image d'avatar dans un profil utilisateur

## Contraintes de la fonctionnailité:

* Pouvoir charger une image d'avatar (upload).
* Pouvoir mettre à jour l'avatar (update).
* Redimensionner l'image chargée
* Renommer l'image chargée (date_user_id.jpg)
* Pouvoir envoyer du png comme du jpeg et sortir du jpeg.
* Nettoyer le répertoire de stockage de manière à ce que seule l'image de l'avatar courant soit en stock.

## Librairies utilisées

```django-model-utils``` Fieldtracker [ Doc](https://django-model-utils.readthedocs.io/en/latest/utilities.html)

```Pillow ``` [Doc](https://pillow.readthedocs.io/en/stable/)

## Surcharge de la méthode save() du Model Userprofile


``` models.py ``` 

Dépendances et bibliothèques

```
from model_utils import FieldTracker
from PIL import Image
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os
from django.conf import settings

```
Model Userprofile

```
class UserProfile(models.Model):
    '''
    Custom User Profile
    '''

    GENDER_CHOICES = (
        ('H', 'Homme'),
        ('F', 'Femme'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=60, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    dept = models.CharField(max_length=5, blank=True)
    town = models.CharField(max_length=60, blank=True)
    birth_year = YearField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='user_avatar/')
    gender = models.CharField('gender' , max_length=1 , choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Here we instantiate a Fieltracker to track any fields specially avatar field
    tracker = FieldTracker()
    
```    
```
    def save(self, *args, **kwargs):
        super().save()

        # we get here the self avatar condition
        # in case of there is no self.avatar as example
        # after a clear action.
        if self.avatar and self.tracker.has_changed('avatar'):

            # keep the upload image path in order to delete it after
            upload_image = self.avatar.path

            # rename avatar image
            avatar_name = '{}-{}.jpg'.format(date.today(), self.user.id)

            img = Image.open(upload_image)

            # convert all picture to jpg
            img = img.convert('RGB')

            # resize picture
            img = img.resize((140, 140), Image.ANTIALIAS)

            # make readable picture
            output = BytesIO()
            img.save(output, format='JPEG', quality=100)
            output.seek(0)
            self.avatar = InMemoryUploadedFile(output,
                                              'ImageField',
                                              avatar_name,
                                              'image/jpeg',
                                              sys.getsizeof(output),
                                              None)

            super(UserProfile, self).save()

			# delete the upload of avatar before resize it
            os.remove(upload_image)

            # delete old image file
            if self.tracker.previous('avatar'):
                old_avatar = '{}{}'.format(settings.MEDIA_ROOT, self.tracker.previous('avatar'))
                os.remove(old_avatar)

        # delete old image file even in case of "clear" image action
        if not self.avatar and self.tracker.has_changed('avatar'):
            old_avatar = '{}{}'.format(settings.MEDIA_ROOT , self.tracker.previous('avatar'))
            os.remove(old_avatar)
            
```            

views.py

```
@login_required
@transaction.atomic
def update_profile(request):

    if request.method == 'POST':

        profile_form = ProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request , _('Your profile was successfully updated!'))
            return redirect('musicians:profile')
        else:
            messages.error(request , _('Please correct the error below.'))
    #
    else:
        profile_form = ProfileForm(instance=request.user.userprofile)

    return render(request , 'musicians/update_profile.html', {

        'profile_form': profile_form
    })
```
    
Template : l'aspect frontend n'est absolument pas mis en valeur, mais le code fonctionne.

``` update_profile.html ```

```
{% extends 'core/base.html' %}
{% load static %}
{% block content %}

<div class="container">
    <div class="row">
        <div class="col s12  ">

<form method="post" enctype="multipart/form-data">
  {% csrf_token %}
  {{ profile_form.as_p }}
  <input type="submit" value="Save">

</form>

 </div>
 </div>
</div>


{% endblock %}
```

``` profile.html ```

```
{% extends 'core/base.html' %}
{% load static %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col s12  ">

<h2>Profil de {{user.userprofile.username}}</h2>
<h2>email :{{user.email}}</h2>
<h4>Bio : {{user.userprofile.bio}}</h4>
 {% if user.userprofile.avatar %}
  <img src="{{ user.userprofile.avatar.url }}" />
 {% else %}
     <img src="{% static 'core/img/0.jpg' %}" />
 {% endif %}


<a href="{% url 'musicians:update_profile' %}" class="waves-effect waves-light btn">button</a>
</div>
        </div>
</div>

{% endblock %}

```
  