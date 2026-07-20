# Eve Dates

eve_dates provides functions for determining the next and previous downtime, relative to a given whenever.Instant. The previous downtime from now can be used to determine the latest possible valid compatibility date used by the EVE ESI. Note that this is just the latest valid date, it does not determine whether there is actually a schema version for that date. Using a compatibility date in the future with the EVE ESI will result in a error.

## Usage

```python
from pfmsoft.eve_snippets.eve_dates import previous_downtime
from whenever import Instant

now = Instant()
most_recent_downtime = previous_downtime(now)
most_recent_compatibility_date = most_recent_downtime.format("YYYY-MM-DD")
```