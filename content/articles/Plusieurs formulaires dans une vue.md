Title: Afficher plusieurs formulaires de manière indépendantes dans le même gabarit
Date: 2019-01-18 10:11
Modified: 2019-01-17 08:00
Category: Articles
Tags: Django, CBV
Slug: 
Author: Aurélia Gourbère



# Afficher plusieurs formulaires de manière indépendantes dans le même gabarit

## Problématique 

Je souhaitais avoir une vue  : update profil qui me permettrait de mettre à jour les différents aspects du profil utilisateur de manière indépendante. Au niveau de l'affichage , je souhaitais que tous ces formulaires (qui me serviraient à changer, créer et supprimer) soient sur le même gabarit comme une sorte de tableau de bord ...

## Raison
 
* Pour pouvoir changer et enregistrer qu'une partie du profil de manière indépendante.
* Pour faciliter les tests par la suite.
* Pour améliorer l'expérience utilisateur.

## Source

Je me suis énormément inspirée de cette [page](https://krzysztofzuraw.com/blog/2016/two-forms-one-view-django.html) Merci à son auteur!

## Méthode

J'ai utilisé les Vues fondées sur les classes de Django et plus spécialement [les Vues génériques d’édition](https://docs.djangoproject.com/fr/2.1/ref/class-based-views/generic-editing/). Ici j'ai choisi Formview mais on aurait très bien bu le faire avec UpdateView.

Une vue principale me permet de faire un GET des différents formulaires, puis une autre vue me sert à faire le POST . Dans cette deuxième vue je redirige en cas de succès du POST vers le même template que la vue principale , ce qui a pour effet d'afficher les informations qui viennent d'être saisie par l'utilisateur et de lui permettre à nouveau d'ouvrir le formulaire. La validation des différents formulaires se fait de manière indépendante et redirige toujours sur la page de mise à jour du profil.

views.py

```
class UpdateProfilView(TemplateView):

    template_name = 'musicians/update_profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        avatar_form = AvatarForm(self.request.GET or None,
                                 instance=request.user.userprofile)
        profile_form = ProfileForm(self.request.GET or None,
                                   instance=request.user.userprofile)
                
        context = self.get_context_data(**kwargs)
        context['avatar_form'] = avatar_form
        context['profile_form'] = profile_form
        return self.render_to_response(context)
        
```        

Puis viennent les vues qui me servent à faire le POST des formulaires.

views.py

```
class UpdateAvatarView(FormView, SuccessMessageMixin):

    form_class = AvatarForm
    template_name = 'musicians/update_profile.html'

    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        avatar_form = self.form_class(request.POST,
                                      request.FILES ,
                                      instance=request.user.userprofile)
        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(self.request, (" Votre image a été  mise à jour!"))
            return redirect('musicians:update_profile') #, self.get_context_data(success=True))

        else:
            avatar_form = self.form_class(instance=request.user.userprofile)

            return self.render_to_response(
               self.get_context_data(avatar_form =avatar_form))


class UpdateDataView(FormView, SuccessMessageMixin):

    form_class = ProfileForm
    template_name = 'musicians/update_profile.html'

    @method_decorator(login_required)
    @transaction.atomic
    def post(self , request , *args , **kwargs):
        profile_form = self.form_class(request.POST,
                                       instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            print(request.POST.get("county_name"))
            messages.success(self.request , (" Vos données ont été mises à jour!"))
            return redirect('musicians:update_profile')

        else:
            profile_form = self.form_class(instance=request.user.userprofile)

            return render(
                self.get_context_data(profile_form=profile_form))
         
```                


Ces deux vues font appel aux formulaires suivants:

forms.py

```
class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'birth_year', 'gender']


class AvatarForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']  
```        

Ils sont basés sur le même modèle: Userprofile mais ne donnent accès qu'à une partie des champs du modèle.

models.py

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
    username = models.CharField("Nom", max_length=60, blank=True)
    bio = models.TextField("Courte description", max_length=500, blank=True)
    code = models.CharField("code postal", max_length=5, blank=True)
    county_name = models.CharField("Nom du département", max_length=60, blank=True)
    town = models.CharField("Ville", max_length=60, blank=True)
    birth_year = YearField("Année de naissance", null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='user_avatar/')
    gender = models.CharField('Genre' , max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Au niveau des urls : 

urls.py

```
from . import views
from django.urls import path

app_name = 'musicians'

urlpatterns = [

    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.UpdateProfilView.as_view(), name='update_profile'),
    path('update_avatar/submit', views.UpdateAvatarView.as_view(), name='update_avatar'),
    path('update_data/submit', views.UpdateDataView.as_view(), name='update_data'),
]
```    

Dans le gabarit : update_profile.html commun aux différentes vues, les formulaires sont appelés de manière indépendantes:

update_profil.html

```
<div class="row valign-wrapper">
   
   
   <!--avatar form-->
   <div class="col s5">
      <form action='{% url "musicians:update_avatar" %}' method="post" enctype="multipart/form-data" >
         {% csrf_token %}
         {% if user.userprofile.avatar %}
         <img alt="Avatar" class="circle responsive-img" src="{{ user.userprofile.avatar.url }}"/>
         {% else %}
         <img alt="Avatar" class="circle responsive-img" src="{% static 'core/img/0.jpg' %}" />
         {% endif %}
         {{ avatar_form.as_p }}
         <button class="btn-floating btn-large waves-effect waves-light " type="submit" >
         <i class="material-icons">check</i></button>
      </form>
   </div>
   
   
   <!--profile form-->
   <div class="col s7">
      <form action='{% url "musicians:update_data" %}' method="post"  >
         {% csrf_token %}
         {{ profile_form.as_p }}
         <button class="btn-floating btn-large waves-effect waves-light " type="submit" >
         <i class="material-icons">check</i></button>
      </form>
   </div>
</div>
```  

## Conclusion

Grâce à cette méthode le code est lisible et les tests sont simplifiés. On peut faire de simple petits formulaires portant sur une partie spécifique du profil. De plus l'utilisateur peut à sa guise mettre à jour les différentes parties de son profil et on peut même imaginer par ce biais l'informer du taux de remplissage de son profil.