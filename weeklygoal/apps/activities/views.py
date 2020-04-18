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


@login_required
@require_http_methods(("GET",))
def app(request):
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
    today = datetime.now().date()
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

    return render(
        request,
        "app.html",
        {
            "activities": serialized_activities,
            "current_week": current_week,
            "current_week_events": serialized_events,
        },
    )
