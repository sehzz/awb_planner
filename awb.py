from icalendar import Calendar
import json

ics_file_path = "awb-abfuhrtermine.ics"

with open(ics_file_path, "r", encoding="utf-8") as file:
    cal = Calendar.from_ical(file.read())

events = []

for event in cal.walk("vevent"):
    start_date = event.get("DTSTART").dt
    event_data = {
        "summary": str(event.get("SUMMARY")),
        "start": start_date.strftime("%Y-%m-%d")
    }
    events.append(event_data)

events_sorted = sorted(events, key=lambda x: x["start"])

json_data = json.dumps(events_sorted, indent=4, ensure_ascii=False)

file_name = "events.json"
with open(file_name, "w", encoding="utf-8") as json_file:
    json_file.write(json_data)

