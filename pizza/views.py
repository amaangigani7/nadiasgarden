from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza

# Create your views here.

def home(request):
    return render(request, 'pizza/home.html')

def order(request):
    multiple_form = MultiplePizzaForm()
    if request.method=='POST':
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = "thanks for ordering. Your %s %s and %s pizza is on it's way" %(filled_form.cleaned_data['size'],
            filled_form.cleaned_data['topping1'],
            filled_form.cleaned_data['topping2'])
            filed_form = PizzaForm()
        else:
            note = 'Pizza order has failed, try again!'
            created_pizza_pk = None
        return render(request, 'pizza/order.html', {'created_pizza_pk': created_pizza_pk, 'pizzaform': filled_form, 'note': note, 'multiple_form': multiple_form,})
    else:
        pass
    form = PizzaForm()
    return render(request, 'pizza/order.html', {'pizzaform': form, 'multiple_form': multiple_form})


def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = 'Pizzas have been ordered!'
        else:
            note = 'Pizzas were not ordered, try again.'
        return render(request, 'pizza/pizzas.html', {'note': note, 'formset': formset,})
    else:
        return render(request, 'pizza/pizzas.html', {'formset': formset})

def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = 'order has been updated'
            return render(request, 'pizza/edit_order.html', {'pizzaform': form, 'pizza':pizza, 'note': note})
    return render(request, 'pizza/edit_order.html', {'pizzaform': form, 'pizza':pizza})
