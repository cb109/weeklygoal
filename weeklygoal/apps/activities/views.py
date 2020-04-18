from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods


def redirect_to_app(request, exception):
    return redirect(reverse("app"))


@login_required
@require_http_methods(("GET",))
def app(request):
    days = [
        _("Monday"),
        _("Tuesday"),
        _("Wednesday"),
        _("Thursday"),
        _("Friday"),
        _("Saturday"),
        _("Sunday"),
    ]
    return render(request, "app.html", {"days": days})
