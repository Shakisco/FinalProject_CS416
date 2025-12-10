from django.shortcuts import render, redirect
from django.conf import settings
from .models import Favorite
import requests

# Create your views here.
def view_events(request):
    classification = request.GET.get('classificationName', '').strip()
    city = request.GET.get('city', '').strip()

    events = []
    error = ""

    if classification and city:
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "classificationName": classification,
            "city": city,
            "sort": "date,asc",
            "apikey": settings.TM_API_KEY,
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            if response.ok:
                data = response.json()
                raw_events = data.get("_embedded", {}).get("events", [])

                for ev in raw_events:
                    name = ev.get("name", "Unknown event")
                    tm_id = ev.get("id", "")

                    start = ev.get("dates", {}).get("start", {})
                    date_str = start.get("localDate", "")
                    time_str = start.get("localTime", "")

                    if time_str:
                        parts = time_str.split(":")
                        if len(parts) >= 2:
                            hour = int(parts[0])
                            minute = parts[1]
                            ampm = "AM"
                            if hour >= 12:
                                ampm = "PM"
                                if hour > 12:
                                    hour -= 12
                            elif hour == 0:
                                hour = 12
                            time_str = f"{hour}:{minute} {ampm}"

                    venue_name = ""
                    street = ""
                    city_name = ""
                    state_code = ""
                    image_url = ""
                    event_url = ""

                    venues = ev.get("_embedded", {}).get("venues", [])
                    if venues:
                        v = venues[0]
                        venue_name = v.get("name", "")
                        street = v.get("address", {}).get("line1", "")
                        city_name = v.get("city", {}).get("name", "")
                        state_code = v.get("state", {}).get("stateCode", "")

                    images = ev.get("images", [])
                    if images:
                        image_url = images[0].get("url", "")

                    event_url = ev.get("url", "")

                    events.append({
                        "tm_id": tm_id,
                        "name": name,
                        "venue": venue_name,
                        "street": street,
                        "city": city_name,
                        "state": state_code,
                        "event_date": date_str,
                        "event_time": time_str,
                        "url": event_url,
                        "image": image_url,
                    })
            else:
                error = "An error occurred while contacting Ticketmaster."
        except Exception:
            error = "An error occurred while contacting Ticketmaster."

    elif request.GET:
        if not classification and not city:
            error = "Please enter a search term and a city."
        elif not classification:
            error = "Search term cannot be empty. Please enter a search term."
        elif not city:
            error = "City cannot be empty. Please enter a city."

    context = {
        "events": events,
        "classification": classification,
        "city": city,
        "error": error,
    }
    return render(request, "view_events.html", context)

def view_favorites(request):
    favorites = Favorite.objects.all()
    return render(request, "favorites.html", {"favorites": favorites})

def add_favorite(request):
    if request.method == "POST":
        tm_id = request.POST.get("tm_id", "")
        name = request.POST.get("name", "")
        venue = request.POST.get("venue", "")
        street = request.POST.get("street", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        event_date = request.POST.get("event_date", "")
        event_time = request.POST.get("event_time", "")
        url = request.POST.get("url", "")
        image = request.POST.get("image", "")

        if tm_id and Favorite.objects.filter(tm_id=tm_id).exists():
            return redirect("view_events")

        Favorite.objects.create(
            tm_id=tm_id,
            name=name,
            venue=venue,
            street=street,
            city=city,
            state=state,
            event_date=event_date,
            event_time=event_time,
            url=url,
            image=image,
        )
    return redirect("view_events")

def delete_favorite(request):
    if request.method == "POST":
        fav_id = request.POST.get("fav_id")
        if fav_id:
            Favorite.objects.filter(id=fav_id).delete()
    return redirect("view_favorites")