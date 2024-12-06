# calendly-fetcher
A code base using the Calendly API that fetches your calendar data and converts it into readable text format.

# Usage

Use PyPI to install the package:

```bash
pip install calendly-fetcher
```

Set the `CALENDLY_API_KEY` environment variable to your Calendly API key. You can get it from [here](https://calendly.com/integrations).

```bash
export CALENDLY_API_KEY="your-api-key"
```

Check that your API key is set correctly (you should see your API key printed):

```bash
echo $CALENDLY_API_KEY
```

Then, you can use the package in Python as follows:

```python
import os
from calendly_fetcher.calendly_fetcher import get_calendly_availability

# Set the API key (you can get it from https://calendly.com/integrations)
api_key = os.environ.get("CALENDLY_API_KEY")
```

# Example

```python
import os
import pytz
from datetime import datetime, timedelta
from calendly_fetcher.calendly_fetcher import get_calendly_availability, convert_basic_date_to_datetime

# Set the API key (you can get it from https://calendly.com/integrations)
api_key = os.environ.get("CALENDLY_API_KEY")

# set start and end dates
start_date = "09-01-2021"
end_date = "09-30-2021"

# convert the dates to datetime objects
start_date = convert_basic_date_to_datetime(start_date)
end_date = convert_basic_date_to_datetime(end_date)

# set your timezone
my_timezone = "America/New_York"

# get availability
availability = get_calendly_availability(api_key, start_date, end_date)

# print availability
for slot in availability:
    if '30min' in slot['scheduling_url']:
        duration = 30
        slot['end_time'] = datetime.strptime(slot['start_time'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(minutes=duration)
        # convert the times from UTC to Eastern Time
        utc_start_time = datetime.strptime(slot['start_time'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
        local_start_time = utc_start_time.astimezone(pytz.timezone(my_timezone))
        utc_end_time = slot['end_time'].replace(tzinfo=pytz.utc)
        local_end_time = utc_end_time.astimezone(pytz.timezone(my_timezone))
        print(f"Available: {local_start_time} - {local_end_time}")
```