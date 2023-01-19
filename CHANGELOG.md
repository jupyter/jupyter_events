# Changelog

All notable changes to this project will be documented in this file.

<!-- <START NEW CHANGELOG ENTRY> -->

## 0.6.3

([Full Changelog](https://github.com/jupyter/jupyter_events/compare/v0.6.2...ac65980322317f1f30bc07150c9e14afaad03d40))

### Maintenance and upkeep improvements

- Clean up typing [#64](https://github.com/jupyter/jupyter_events/pull/64) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_events/graphs/contributors?from=2023-01-10&to=2023-01-12&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Ablink1073+updated%3A2023-01-10..2023-01-12&type=Issues)

<!-- <END NEW CHANGELOG ENTRY> -->

## 0.6.2

([Full Changelog](https://github.com/jupyter/jupyter_events/compare/v0.6.1...a00859944090df5277f263fcfe72ae48b8cc2382))

### Maintenance and upkeep improvements

- Decrease pyyaml dependency floor to increase compatibility [#63](https://github.com/jupyter/jupyter_events/pull/63) ([@kevin-bates](https://github.com/kevin-bates))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_events/graphs/contributors?from=2023-01-10&to=2023-01-10&type=c))

[@kevin-bates](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Akevin-bates+updated%3A2023-01-10..2023-01-10&type=Issues)

## 0.6.1

([Full Changelog](https://github.com/jupyter/jupyter_events/compare/v0.6.0...1aa57024d0a8c73b10d9944375f84c01ee9f5c33))

### Maintenance and upkeep improvements

- Remove artificial cap on jsonschema dependency [#61](https://github.com/jupyter/jupyter_events/pull/61) ([@kevin-bates](https://github.com/kevin-bates))
- Try dropping jsonschema dependency [#59](https://github.com/jupyter/jupyter_events/pull/59) ([@bretttully](https://github.com/bretttully))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_events/graphs/contributors?from=2023-01-09&to=2023-01-10&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Ablink1073+updated%3A2023-01-09..2023-01-10&type=Issues) | [@bretttully](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Abretttully+updated%3A2023-01-09..2023-01-10&type=Issues) | [@kevin-bates](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Akevin-bates+updated%3A2023-01-09..2023-01-10&type=Issues)

## 0.6.0

([Full Changelog](https://github.com/jupyter/jupyter_events/compare/v0.5.0...83f01b142c3190074d9e6108155514ddc6237d2c))

### Maintenance and upkeep improvements

- Add typing file [#60](https://github.com/jupyter/jupyter_events/pull/60) ([@blink1073](https://github.com/blink1073))
- More lint cleanup [#56](https://github.com/jupyter/jupyter_events/pull/56) ([@blink1073](https://github.com/blink1073))
- Add more ci checks [#53](https://github.com/jupyter/jupyter_events/pull/53) ([@blink1073](https://github.com/blink1073))
- Allow releasing from repo [#52](https://github.com/jupyter/jupyter_events/pull/52) ([@blink1073](https://github.com/blink1073))
- Adopt ruff and address lint [#51](https://github.com/jupyter/jupyter_events/pull/51) ([@blink1073](https://github.com/blink1073))
- Use base setup dependency type [#47](https://github.com/jupyter/jupyter_events/pull/47) ([@blink1073](https://github.com/blink1073))
- Clean up CI [#45](https://github.com/jupyter/jupyter_events/pull/45) ([@blink1073](https://github.com/blink1073))
- CI Cleanup [#44](https://github.com/jupyter/jupyter_events/pull/44) ([@blink1073](https://github.com/blink1073))
- Bump actions/checkout from 2 to 3 [#42](https://github.com/jupyter/jupyter_events/pull/42) ([@dependabot](https://github.com/dependabot))
- Add dependabot [#41](https://github.com/jupyter/jupyter_events/pull/41) ([@blink1073](https://github.com/blink1073))
- Maintenance cleanup [#36](https://github.com/jupyter/jupyter_events/pull/36) ([@blink1073](https://github.com/blink1073))
- Clean up CI checks [#35](https://github.com/jupyter/jupyter_events/pull/35) ([@blink1073](https://github.com/blink1073))
- Clean up pyproject and ci [#33](https://github.com/jupyter/jupyter_events/pull/33) ([@blink1073](https://github.com/blink1073))

### Documentation improvements

- Fix listener example [#34](https://github.com/jupyter/jupyter_events/pull/34) ([@dlqqq](https://github.com/dlqqq))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_events/graphs/contributors?from=2022-09-12&to=2023-01-09&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Ablink1073+updated%3A2022-09-12..2023-01-09&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Adependabot+updated%3A2022-09-12..2023-01-09&type=Issues) | [@dlqqq](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Adlqqq+updated%3A2022-09-12..2023-01-09&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Apre-commit-ci+updated%3A2022-09-12..2023-01-09&type=Issues)

## 0.5.0

([Full Changelog](https://github.com/jupyter/jupyter_events/compare/v0.4.0...af1db6f5b9052e54d5a65797b67bff17b80e7eec))

### Enhancements made

- Add pytest plugin for testing events in other libraries [#23](https://github.com/jupyter/jupyter_events/pull/23) ([@Zsailer](https://github.com/Zsailer))
- improve error messages for absent/invalid schema path [#22](https://github.com/jupyter/jupyter_events/pull/22) ([@dlqqq](https://github.com/dlqqq))

### Bugs fixed

- specify utf-8 encoding for loading/dumping yaml [#29](https://github.com/jupyter/jupyter_events/pull/29) ([@bollwyvl](https://github.com/bollwyvl))
- use safe loaders and dumpers in yaml lib [#28](https://github.com/jupyter/jupyter_events/pull/28) ([@dlqqq](https://github.com/dlqqq))

### Maintenance and upkeep improvements

- add jsonschema\[format-nongpl\], core event schema [#31](https://github.com/jupyter/jupyter_events/pull/31) ([@bollwyvl](https://github.com/bollwyvl))
- Add CLI tests, return codes, version [#30](https://github.com/jupyter/jupyter_events/pull/30) ([@bollwyvl](https://github.com/bollwyvl))
- Set version floor on jsonchema [#25](https://github.com/jupyter/jupyter_events/pull/25) ([@kevin-bates](https://github.com/kevin-bates))
- Testing that the `.emit` call is a no-op when no listeners are registered. [#24](https://github.com/jupyter/jupyter_events/pull/24) ([@Zsailer](https://github.com/Zsailer))

### Documentation improvements

- docs: wrap shell command in quotes [#21](https://github.com/jupyter/jupyter_events/pull/21) ([@dlqqq](https://github.com/dlqqq))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter_events/graphs/contributors?from=2022-08-29&to=2022-09-12&type=c))

[@bollwyvl](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Abollwyvl+updated%3A2022-08-29..2022-09-12&type=Issues) | [@dlqqq](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Adlqqq+updated%3A2022-08-29..2022-09-12&type=Issues) | [@kevin-bates](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3Akevin-bates+updated%3A2022-08-29..2022-09-12&type=Issues) | [@Zsailer](https://github.com/search?q=repo%3Ajupyter%2Fjupyter_events+involves%3AZsailer+updated%3A2022-08-29..2022-09-12&type=Issues)

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
