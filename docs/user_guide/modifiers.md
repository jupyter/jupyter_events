# Modifying events in an application using `jupyter_events`

If you're deploying a configurable application that uses Jupyter Events to emit events, you can extend the application's event logger to modify/mutate/redact incoming events before they are emitted. This is particularly useful if you need to mask, salt, or remove sensitive data from incoming event.

To modify events, define a callable (function or method) that modifies the event data dictionary. This callable **must** follow an exact signature (type annotations required):

```python
def my_modifier(schema_id: str, data: dict) -> dict:
    ...
```

The return value is the mutated event data (dict). This data will be validated and emitted _after_ it is modified, so it still must follow the event's schema.

Next, add this modifier to the event logger using the `.add_modifier` method:

```python
logger = EventLogger()
logger.add_modifier(my_modifier)
```

This method enforces the signature above and will raise a `ModifierError` if the signature does not match.
