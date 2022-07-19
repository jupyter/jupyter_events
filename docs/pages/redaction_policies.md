# Redacting Sensitive Data

Jupyter Events might possible include sensitive data, specifically personally identifiable information (PII). To reduce
the risk of capturing unwanted PII, Jupyter Events requires _every_ registered event to explicitly list its
`redactionPolicies`. Data labeled with a redacted policed will be removed from an event by Jupyter Events **before** before being emitted. Schemas that list properties without an explicit `redactionPolicies` list will fail validation.
