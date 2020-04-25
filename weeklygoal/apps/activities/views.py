import json
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from weeklygoal.apps.activities.models import Activity, Event, UserSettings


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


def serialize_event(event):
    return {
        "id": event.id,
        "date": format_date(event.created_at),
        "activity": event.activity_id,
    }


def get_weekstart_for_date(today):
    today_index = today.weekday()
    offset_to_monday = today_index
    monday = today - timedelta(days=offset_to_monday)
    return monday


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
    user = request.user

    # Handle optional reference date
    today = datetime.now().date()
    reference_date = request.GET.get("day")
    if reference_date is not None:
        try:
            today = string_to_date(reference_date)
        except ValueError as err:
            pass

    # Serialize available Activities
    activities = Activity.objects.filter(active=True, user=user)
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
    monday = get_weekstart_for_date(today)
    current_week_dates = [monday + timedelta(days=offset) for offset in range(7)]
    current_week = [
        {"date": format_date(date), "day": localized_days[i],}
        for i, date in enumerate(current_week_dates)
    ]

    # Serialize Events for current week
    current_week_events = Event.objects.filter(
        created_at__date__in=current_week_dates, activity__in=activities
    ).order_by("-created_at")
    serialized_events = [serialize_event(event) for event in current_week_events]

    iso_year, iso_weeknumber, iso_weekday = today.isocalendar()

    try:
        goal = user.settings.goal
        background_color = user.settings.background_color
        highlight_color = user.settings.highlight_color
    except UserSettings.DoesNotExist:
        goal = 5
        background_color = settings.COLOR_BACKGROUND_DEFAULT
        highlight_color = settings.COLOR_HIGHLIGHT_DEFAULT

    context = {
        "activities": serialized_activities,
        "actual_today": format_date(datetime.now().date()),
        "current_week_events": serialized_events,
        "current_week": current_week,
        "goal": goal,
        "iso_weeknumber": iso_weeknumber,
        "iso_year": iso_year,
        "today": format_date(today),
        "username": user.username,
        "urls": {
            "logout": reverse("logout"),
            "create_event": reverse("create_event"),
            "delete_event": reverse("delete_event", kwargs={"event_id": 0}).replace(
                "0", ""
            ),
            "change_week": reverse("change_week", kwargs={"direction": "0"}).replace(
                "0", ""
            ),
        },
        "strings": {"today": _("Today"), "week": _("Week")},
        "colors": {"background": background_color, "highlight": highlight_color},
    }
    return render(request, "app.html", context,)


@login_required
@require_http_methods(("POST",))
def create_event(request):
    data = json.loads(request.body.decode("utf-8"))

    activity_id = data["activity"]
    activity = Activity.objects.get(id=activity_id, user=request.user)
    date = string_to_date(data["date"])

    event = Event.objects.create(activity=activity, created_at=date)
    serialized_event = serialize_event(event)
    return JsonResponse(serialized_event, status=200)


@login_required
@require_http_methods(("DELETE",))
def delete_event(request, event_id):
    Event.objects.get(id=event_id, activity__user=request.user).delete()
    return HttpResponse(status=204)


@login_required
@require_http_methods(("GET",))
def change_week(request, direction):
    assert direction in ("previous", "next")

    day = string_to_date(request.GET["day"]).date()
    if direction == "previous":
        weekstart = day - timedelta(days=7)
    elif direction == "next":
        weekstart = day + timedelta(days=7)

    next_url = reverse("app") + "?day=" + format_date(weekstart)
    return JsonResponse({"next_url": next_url})
