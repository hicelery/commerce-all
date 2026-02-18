from django.contrib import messages
from django.shortcuts import render
from .models import AboutPage, Contact
from django.views import generic
from requests import post
from .forms import ContactForm

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
