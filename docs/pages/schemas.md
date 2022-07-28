# Writing a schema for Jupyter Events

Jupyter Event Schemas must be valid [JSON schema](https://json-schema.org/) and can be written in valid
YAML or JSON. Every schema is validated against Jupyter Event's "meta"-JSON schema, [here]().

At a minimum, valid Jupyter Event schema requires have the following keys:

- `$id` : a URI to identify (and possibly locate) the schema.
- `version` : the schema version.
- `redactionPolicies`: a list of labels representing the personal data sensitivity of this event. The main logger can be configured to redact any events or event properties that might contain sensitive information. Set this value to `"unrestricted"` if emitting that this event happen does not reveal any person data.
- `properties` : attributes of the event being emitted.

  Each property should have the following attributes:

  - `title` : name of the property
  - `redactionPolicies`: a list of labels representing the personal data sensitivity of this property. This field will be redacted from the emitted event if the policy is not allowed.

- `required`: list of required properties.

Here is a minimal example of a valid JSON schema for an event.

```yaml
$id: event.jupyter.org/example-event
version: 1
title: My Event
description: |
  All events must have a name property
type: object
redactionPolicy:
  - category.jupyter.org/unrestricted
properties:
  thing:
    title: Thing
    redactionPolicy:
      - category.jupyter.org/unrestricted
    description: A random thing.
  user:
    title: User name
    redactionPolicies:
      - category.jupyter.org/user-identifier
    description: Name of user who initiated event
required:
  - thing
  - user
```

## Redaction Policies

Each property can be labelled with `redactionPolicies` field. This makes it easier to
filter properties based on a category. We recommend that schema authors use valid
URIs for these labels, e.g. something like `category.jupyter.org/unrestricted`.

Below is a list of common category labels that Jupyter Events recommends using:

- `category.jupyter.org/unrestricted`
- `category.jupyter.org/user-identifier`
- `category.jupyter.org/user-identifiable-information`
- `category.jupyter.org/action-timestamp`
