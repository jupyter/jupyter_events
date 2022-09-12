# Changelog

All notable changes to this project will be documented in this file.

<!-- <START NEW CHANGELOG ENTRY> -->

## 0.5.0

([Full Changelog](https://github.com/jupyter/jupyter_events/compare/v0.4.0...af1db6f5b9052e54d5a65797b67bff17b80e7eec))

### Enhancements made

- Add pytest plugin for testing events in other libraries [#23](https://github.com/jupyter/jupyter_events/pull/23) ([@Zsailer](https://github.com/Zsailer))
- improve error messages for absent/invalid schema path [#22](https://github.com/jupyter/jupyter_events/pull/22) ([@dlqqq](https://github.com/dlqqq))

### Bugs fixed

- specify utf-8 encoding for loading/dumping yaml [#29](https://github.com/jupyter/jupyter_events/pull/29) ([@bollwyvl](https://github.com/bollwyvl))
- use safe loaders and dumpers in yaml lib [#28](https://github.com/jupyter/jupyter_events/pull/28) ([@dlqqq](https://github.com/dlqqq))

### Maintenance and upkeep improvements

- add jsonschema[format-nongpl], core event schema [#31](https://github.com/jupyter/jupyter_events/pull/31) ([@bollwyvl](https://github.com/bollwyvl))
- Add CLI tests, return codes, version [#30](https://github.com/jupyter/jupyter_events/pull/30) ([@bollwyvl](https://github.com/bollwyvl))
- Set version floor on jsonchema [#25](https://github.com/jupyter/jupyter_events/pull/25) ([@kevin-bates](https://github.com/kevin-bates))
- Testing that the `.emit` call is a no-op when no listeners are registered. [#24](https://github.com/jupyter/jupyter_events/pull/24) ([@Zsailer](https://github.com/Zsailer))

### Documentation improvements

- docs: wrap shell command in quotes [#21](https://github.com/jupyter/jupyter_events/pull/21) ([@dlqqq](https://github.com/dlqqq))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_events/graphs/contributors?from=2022-08-29&to=2022-09-12&type=c))

[@bollwyvl](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Abollwyvl+updated%3A2022-08-29..2022-09-12&type=Issues) | [@dlqqq](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Adlqqq+updated%3A2022-08-29..2022-09-12&type=Issues) | [@kevin-bates](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Akevin-bates+updated%3A2022-08-29..2022-09-12&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3AZsailer+updated%3A2022-08-29..2022-09-12&type=Issues)

<!-- <END NEW CHANGELOG ENTRY> -->

## 0.4.0

([Full Changelog](https://github.com/jupyter/jupyter_events/compare/v0.3.0...6d22b7dd73b1a04baf26a68539743d8a66599469))

### Enhancements made

- Add method to remove listener [#18](https://github.com/jupyter/jupyter_events/pull/18) ([@Zsailer](https://github.com/Zsailer))
- Add a simple CLI tool for validating event schemas [#9](https://github.com/jupyter/jupyter_events/pull/9) ([@Zsailer](https://github.com/Zsailer))

### Bugs fixed

- Fix minor bugs in Listeners API [#19](https://github.com/jupyter/jupyter_events/pull/19) ([@Zsailer](https://github.com/Zsailer))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_events/graphs/contributors?from=2022-08-24&to=2022-08-29&type=c))

[@Zsailer](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3AZsailer+updated%3A2022-08-24..2022-08-29&type=Issues)

## 0.3.0

([Full Changelog](https://github.com/jupyter/jupyter_events/compare/v0.2.0...94646036f0ab4b3397e261422fd3041c0d7501e9))

### Enhancements made

- Remove (duplicate) version argument from API [#16](https://github.com/jupyter/jupyter_events/pull/16) ([@Zsailer](https://github.com/Zsailer))
- Add a "modifiers" hook to allow extension authors to mutate/redact event data [#12](https://github.com/jupyter/jupyter_events/pull/12) ([@Zsailer](https://github.com/Zsailer))
- Add Listeners API [#10](https://github.com/jupyter/jupyter_events/pull/10) ([@Zsailer](https://github.com/Zsailer))

### Bugs fixed

- Reading strings as file path is unsafe [#15](https://github.com/jupyter/jupyter_events/pull/15) ([@Zsailer](https://github.com/Zsailer))

### Maintenance and upkeep improvements

- Fix check_release build [#14](https://github.com/jupyter/jupyter_events/pull/14) ([@blink1073](https://github.com/blink1073))

### Documentation improvements

- Add JupyterLite example to the documentation [#6](https://github.com/jupyter/jupyter_events/pull/6) ([@Zsailer](https://github.com/Zsailer))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_events/graphs/contributors?from=2022-08-11&to=2022-08-24&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Ablink1073+updated%3A2022-08-11..2022-08-24&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3AZsailer+updated%3A2022-08-11..2022-08-24&type=Issues)

## 0.2.0

([Full Changelog](https://github.com/jupyter/jupyter_events/compare/v0.1.0...88acd8ec613fe7d2aa6fcaf07158275989dc5dfd))

### Enhancements made

- Add new EventSchema and SchemaRegistry API [#4](https://github.com/jupyter/jupyter_events/pull/4) ([@Zsailer](https://github.com/Zsailer))
- Add redactionPolicies field to Jupyter Event schemas [#2](https://github.com/jupyter/jupyter_events/pull/2) ([@Zsailer](https://github.com/Zsailer))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_events/graphs/contributors?from=2022-05-31&to=2022-08-11&type=c))

[@kevin-bates](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Akevin-bates+updated%3A2022-05-31..2022-08-11&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3AZsailer+updated%3A2022-05-31..2022-08-11&type=Issues)

## 0.1.0
