# Configure applications to emit events

Jupyter applications can be configured to emit events by registering
logging `Handler`s with an Application's `EventLogger` object.

This is usually done using a Jupyter configuration file, e.g. `jupyter_config.py`:

```python
from logging import FileHandler

# Log events to a local file on disk.
handler = FileHandler("events.txt")

# Explicitly list the types of events
# to record and what properties or what categories
# of data to begin collecting.
c.EventLogger.handlers = [handler]
```
