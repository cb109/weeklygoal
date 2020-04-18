from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


@login_required
def app(request):
    return render(request, "app.html")


def redirect_to_app(request, exception):
    return redirect(reverse("app"))
