import requests
import pytz
import os
from datetime import datetime, timedelta, timezone

def get_calendly_availability(api_token, start_date, end_date):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Get user URI
    user_response = requests.get("https://api.calendly.com/users/me", headers=headers)
    user_uri = user_response.json()["resource"]["uri"]

    # Get event types
    event_types_response = requests.get(f"https://api.calendly.com/event_types?user={user_uri}", headers=headers)
    event_types = event_types_response.json()["collection"]

    combined_availability = []

    for event_type in event_types:
        event_type_uri = event_type["uri"]

        start_time = start_date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = end_date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") 

        params = {
            "event_type": event_type_uri,
            "start_time": start_time,
            "end_time": end_time,
            "timezone": "America/New_York"
        }
        
        availability_response = requests.get("https://api.calendly.com/event_type_available_times", headers=headers, params=params)
        availability = availability_response.json()["collection"]
        
        combined_availability.extend(availability)

    return combined_availability

def convert_basic_date_to_datetime(date):
    # example: start_date = datetime.strptime(start_date_simple, "%m-%d-%Y").replace(tzinfo=pytz.timezone('America/New_York'))
    return datetime.strptime(date, "%m-%d-%Y").replace(tzinfo=pytz.timezone('America/New_York'))

def availability_to_list_of_strings(availability, timezone, duration=30):
    availability_strings = []
    for slot in availability:
        if f'{duration}min' in slot['scheduling_url']:
            slot['end_time'] = datetime.strptime(slot['start_time'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(minutes=duration)
            # convert the times from UTC to the specified timezone
            utc_start_time = datetime.strptime(slot['start_time'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
            local_start_time = utc_start_time.astimezone(pytz.timezone(timezone))
            utc_end_time = slot['end_time'].replace(tzinfo=pytz.utc)
            local_end_time = utc_end_time.astimezone(pytz.timezone(timezone))
            availability_strings.append(f"Available: {local_start_time} - {local_end_time}")
    return availability_strings

# Usage
# api_token = os.getenv("CALENDLY_API_TOKEN")

# # Define your start and end dates in EST
# eastern = pytz.timezone('America/New_York')

# # define start and end dates
# ## make the start date the closest monday starting at 12 AM
# ### implement logic to find the closest monday
# # today = datetime.now().date()
# # days_ahead = (0 - today.weekday()) % 7  # Calculate the number of days until Monday. today.weekday() basically returns 0 for Monday, 1 for Tuesday, etc.
# # closest_monday = today + timedelta(days=days_ahead)
# # ## get the current time
# # current_time = datetime.now().time()
# # current_day_time = datetime.combine(today, current_time)
# # ## set the start date
# # start_date = datetime.combine(closest_monday, datetime.min.time())
# # ## take the current time is greater than the closest monday time
# # if current_day_time > start_date:
# #     start_date = current_day_time + timedelta(hours=1)

# # # check if the current day is less than the start date
# # today_less_than_start_date = today < start_date.date()

# # # if today is less than the start date, set the start date to the current day

# # define the start date to be the current day + 1 hour
# start_date = datetime.now().replace(tzinfo=pytz.timezone('America/New_York')) + timedelta(hours=1)

# ############################################
# ############################################
# #### OR ####################################
# ############################################
# ############################################

# # define the start date to be a specific date
# # start_date_simple = "09-28-2024"
# # start_date = datetime.strptime(start_date_simple, "%m-%d-%Y").replace(tzinfo=pytz.timezone('America/New_York'))    

# ## set the end date to 7 days from the start date
# end_date = start_date + timedelta(days=7)

# availability = get_calendly_availability(api_token, start_date, end_date)

# for slot in availability:
#     if '30min' in slot['scheduling_url']:
#         duration = 30
#         slot['end_time'] = datetime.strptime(slot['start_time'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(minutes=duration)
#         # convert the times from UTC to Eastern Time
#         utc_start_time = datetime.strptime(slot['start_time'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
#         local_start_time = utc_start_time.astimezone(pytz.timezone('America/New_York'))
#         utc_end_time = slot['end_time'].replace(tzinfo=pytz.utc)
#         local_end_time = utc_end_time.astimezone(pytz.timezone('America/New_York'))
#         print(f"Available: {local_start_time} - {local_end_time}")