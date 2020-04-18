from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods


def get_localized_days():
    """Must be called inside a view so LocaleMiddleware can translate it."""
    return [
        {"label": _("Monday"), "value": "Monday"},
        {"label": _("Tuesday"), "value": "Tuesday"},
        {"label": _("Wednesday"), "value": "Wednesday"},
        {"label": _("Thursday"), "value": "Thursday"},
        {"label": _("Friday"), "value": "Friday"},
        {"label": _("Saturday"), "value": "Saturday"},
        {"label": _("Sunday"), "value": "Sunday"},
    ]


def redirect_to_app(request, exception):
    return redirect(reverse("app"))


@login_required
@require_http_methods(("GET",))
def app(request):
    return render(request, "app.html", {"days": get_localized_days()})
