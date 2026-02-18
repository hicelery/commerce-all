from django.contrib import messages
from django.shortcuts import render
from .models import AboutPage, Contact
from django.views import generic
from requests import post
from .forms import ContactForm, OrderForm

# Create your views here.


def about_detail(request):
    """Display the first About Page.

    **Context**

    ``aboutpage``
        An instance of :model:`about.AboutPage`.

    **Template:**
    :template:`about/about.html`
    """

    about = AboutPage.objects.first()

    # Post request for contact forms
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Contact request submitted successfully'
            )
    contact_form = ContactForm()
    context = {"about": about,
               "contact_form": contact_form}
    return render(
        request,
        "about/about.html",
        context,
    )


def Ordercontact(request):
    """Handle order contact form submissions.

    **Context**

    ``order_form``
        An instance of :model:`about.OrderForm`.

    **Template:**
    :template:`about/contact.html`
    """

    if request.method == "POST":
        order_form = OrderForm(data=request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Order query submitted successfully'
            )
    else:
        order_form = OrderForm()

    context = {"order_form": order_form}
    return render(request, "about/contact.html", context)
