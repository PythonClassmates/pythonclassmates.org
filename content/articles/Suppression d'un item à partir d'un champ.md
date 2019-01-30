Title: Supprimer un item à partir d'un formulaire de sélection.
Date: 2019-01-18 10:18
Modified: 2019-01-17 08:00
Category: Articles
Tags: Django, Forms, CBV
Slug:
Author: Aurélia Gourbère


# Permettre à l'utilisateur de supprimer un de ses items à partir d'un formulaire de sélection. 

## Contexte  

Dans ce projet , le musicien peut jouer de plusieurs instruments. Dans le cas où il veuille en supprimer un: il a accès à un formulaire où il peut sélectionner un instrument parmi les siens.

## Contraintes

Dans ce cas précis nous ne pouvions pas utiliser de DeleteView car le choix porte sur un queryset contenant plusieurs items. 

## Solution

Créer une vue générique Formview qui renvoi un formulaire pré rempli avec un queryset comportant tous les instruments du musiciens.

De la même manière que le document précédant ce formulaire est présent dans une vue qui fera le GET et dans une autre chargée du POST car nous affichons plusieurs formulaires sur le même gabarit. [cf ce document](https://github.com/horlas/How_to/blob/master/Plusieurs%20formulaires%20dans%20une%20vue.md) .

Lors du post du formulaire, nous supprimons l'instrument sélectionné transmis par l'utilisateur.

models.py

```
class Instrument(models.Model):
    ''' Musicians Instruments'''
    instrument = models.CharField('instrument', max_length=80, choices=INSTRUMENT_CHOICE, 											blank=False)
    level = models.CharField('niveau de maitrise', max_length=80, choices=LEVEL_CHOICE, 										blank=False)
    musician = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.instrument
``` 

forms.py

```
class InstruDeleteForm(Form):

    # here we use a dummy `queryset`, because ModelChoiceField
    # requires some queryset
    instrument = ModelChoiceField(queryset=Instrument.objects.none(), empty_label=None)

    def __init__(self, user, *args, **kwargs):
        super(InstruDeleteForm, self).__init__(*args, **kwargs)
        self.fields['instrument'].queryset = Instrument.objects.filter(musician=user)
```

Ici nous passons au constructeur du formulaire ```user```, ce qui nous permettra par la suite de "peupler" le formulaire avec les données de l'utilisateur connecté (request.user)


Vue en charge du GET

views.py

```
class UpdateProfilView(TemplateView):

    template_name = 'musicians/update_profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        del_instru_form = InstruDeleteForm(request.user)
        context = self.get_context_data(**kwargs)
        context['del_instru_form'] = del_instru_form
        return self.render_to_response(context)

```
Comme on peut le voir ici request.user est passé en argument du formulaire InstruDeleteForm.

Vue en charge du POST

```
class InstruDeleteView(FormView, SuccessMessageMixin):
    '''View to delete instrument based on a Formwview because with deleteview
    we can not have the select option. So we use a custom form
    witch display a queryset : request. user instrument'''

    template_name = 'musicians/update_profile.html'
    success_url = reverse_lazy('musicians:update_profile')
    success_message = "Votre Instrument a été supprimé ! "

    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        del_instru_form = InstruDeleteForm(request.user, request.POST)
        # get instrument id user wants to delete
        delete_id = request.POST['instrument']
        if del_instru_form.is_valid():
            delete_instrument = Instrument.objects.get(id=delete_id)
            delete_instrument.delete()
            return redirect(self.success_url)
```            
            
Ici on récupère la valeur du choix de l'utilisateur par ```delete_id = request.POST['instrument']``` , ce qui nous permet de supprimer l'entrée directement dans la base.

urls.py

```
app_name = 'musicians'

urlpatterns = [

    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.UpdateProfilView.as_view(), name='update_profile'),
	...		
    path('add_instru/submit', views.InstruCreateView.as_view(), name='add_instru'),
    path('delete_instru/submit', views.InstruDeleteView.as_view(), name='del_instru'),


]
```

update_profile.html

```
 <form action='{% url "musicians:del_instru" %}' method="post">
      {% csrf_token %}
      <div class="row valign-wrapper">
         <div class="col s6">
            {{ del_instru_form.as_p }}
         </div>
         <div class="col s6 center-align ">
            <button  class="btn-floating btn-small waves-effect waves-light">
            <i class="material-icons">delete</i>  </button>
         </div>
      </div>
   </form>
```   
