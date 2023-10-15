# Adding `EventLogger` to a Jupyter application

To begin using Jupyter Events in your Python application, create an instance of the `EventLogger` object in your application.

```python
from jupyter_core.application import JupyterApp
from jupyter_events import EventLogger
from jupyter_events import Event


class MyApplication(JupyterApp):
    classes = [EventLogger, ...]
    eventlogger = Instance(EventLogger)

    def initialize(self, *args, **kwargs):
        self.eventlogger = EventLogger(parent=self)
        ...
```

Register an event schema with the logger.

```python
        schema = """
        $id: http://myapplication.org/my-method
        version: 1
        title: My Method Executed
        description: My method was executed one time.
        properties:
        msg:
            title: Message
            type: string
        """

        self.eventlogger.register_event_schema(schema=schema)
```

Call `.emit(...)` within the application to emit an instance of the event.

```python
    def my_method(self):
        # Do something
        ...
        # Emit event telling listeners that this event happened.
        self.eventlogger.emit(
            schema_id="myapplication.org/my-method", data={"msg": "Hello, world!"}
        )
        # Do something else...
        ...
```

Great! Now your application is logging events from within. Deployers of your application can configure the system to listen to this event using Jupyter's configuration system. This usually means reading a `jupyter_config.py` file like this:

```python
# A Jupyter
from logging import StreamHandler

handler = StreamHandler()
c.EventLogger.handlers = [handler]
```

Now when we run our application and call the method, the event will be emitted to the console:

```
app = MyApplication.launch_instance(config_file="jupyter_config.py")
app.my_method()
```

```
{'__timestamp__': '2022-08-09T17:15:27.458048Z',
 '__schema__': 'myapplication.org/my-method',
 '__schema_version__': 1,
 '__metadata_version__': 1,
 'msg': 'Hello, world!'}
```
