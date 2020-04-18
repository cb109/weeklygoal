from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from weeklygoal.apps.activities.models import Activity, Event


def get_localized_days():
    """Must be called inside a view so LocaleMiddleware can translate it."""
    return [
        _("Monday"),
        _("Tuesday"),
        _("Wednesday"),
        _("Thursday"),
        _("Friday"),
        _("Saturday"),
        _("Sunday"),
    ]


def redirect_to_app(request, exception):
    return redirect(reverse("app"))


def format_date(date):
    return date.strftime(settings.DATE_FORMAT)


def string_to_date(date_str):
    return datetime.strptime(date_str, settings.DATE_FORMAT)


@login_required
@require_http_methods(("GET",))
def app(request):
    """Render the current week as a table of day * activity.

    GET Args:
        day (str): Optional reference date formatted as 'DD.MM.YYYY'.
            If not specified, today's date is used. If specified, the
            current week is based on that day (Mo - Fr).

    Returns:
        html, including a Vue app

    """
    # Handle optional reference date
    today = datetime.now().date()
    reference_date = request.GET.get("day")
    if reference_date is not None:
        try:
            today = string_to_date(reference_date)
        except ValueError as err:
            pass

    # Serialize available Activities
    activities = Activity.objects.all()
    serialized_activities = [
        {
            "id": activity.id,
            "name": activity.name,
            "image_url": activity.image.url if activity.image else "",
        }
        for activity in activities
    ]

    # Serialize current week dates
    localized_days = get_localized_days()
    today_index = today.weekday()
    offset_to_monday = today_index
    monday = today - timedelta(days=offset_to_monday)
    current_week_dates = [monday + timedelta(days=offset) for offset in range(7)]
    current_week = [
        {"date": format_date(date), "day": localized_days[i],}
        for i, date in enumerate(current_week_dates)
    ]

    # Serialize Events for current week
    current_week_events = Event.objects.filter(
        created_at__date__in=current_week_dates
    ).order_by("-created_at")
    serialized_events = [
        {
            "id": event.id,
            "date": format_date(event.created_at),
            "activity": event.activity_id,
        }
        for event in current_week_events
    ]

    context = {
        "activities": serialized_activities,
        "current_week_events": serialized_events,
        "current_week": current_week,
        "today": format_date(today),
    }
    return render(request, "app.html", context,)
