.. _adding-events:

Adding the Event System to an application
=========================================

Jupyter Events enables you to log events from your running application.
(It's designed to work best with traitlet's `Application` object
for simple configuration.) To use the system, begin by creating an
instance of ``EventLogger``:

.. code-block:: python


    from jupyter_events import EventLogger

    class MyApplication:

        def __init__(self):
            ...
            # The arguments
            self.eventlogger = EventLogger(
                ...
                # Either pass the traits (see below) here,
                # or enable users of your application to configure
                # the EventLogger's traits.
            )


EventLogger has two configurable traits:

    - ``handlers``: a list of Python's logging handlers that
        handle the recording of incoming events.
    - ``allowed_schemas``: a dictionary of options for each schema
        describing what data should be collected.

Next, you'll need to register event schemas for your application.
You can register schemas using the ``register_schema_file``
(JSON or YAML format) or ``register_schema`` methods.


Once your have an instance of ``EventLogger`` and your registered
schemas, you can use the ``record_event`` method to log that event.

.. code-block:: python

    # Record an example event.
    event = {'name': 'example event'}
    self.eventlogger.record_event(
        schema_id='url.to.event.schema',
        version=1,
        event=event
    )
