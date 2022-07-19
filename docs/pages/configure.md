.. \_using-events:

# Using Jupyter Events in Jupyter applications

Most people will use `jupyter_events` to log events data from Jupyter
applications, (e.g. JupyterLab, Jupyter Server, JupyterHub, etc).

In this case, you'll be able to record events provided by schemas within
those applications. To start, you'll need to configure each
application's `EventLogger` object.

This usually means two things:

1. Define a set of `logging` handlers (from Python's standard library)
   to tell Jupyter Events where to send your event data
   (e.g. file, remote storage, etc.)
2. List redacted policies to remove sensitive data from any events.

Here is an example of a Jupyter configuration file, e.g. `jupyter_config.d`,
that demonstrates how to configure an eventlog.

```python
from logging import FileHandler

# Log events to a local file on disk.
handler = FileHandler('events.txt')

# Explicitly list the types of events
# to record and what properties or what categories
# of data to begin collecting.
c.EventLogger.handlers = [handler]
c.EventLogger.redacted_policies = ["user-identifiable-information", "user-identifier"]
```
