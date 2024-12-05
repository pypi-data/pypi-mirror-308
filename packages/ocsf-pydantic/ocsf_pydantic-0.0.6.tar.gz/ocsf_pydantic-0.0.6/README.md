# Project Name

OCSF-Pydantic

## Description

[Pydantic](https://docs.pydantic.dev/latest/) validated models for [OCSF schema](https://schema.ocsf.io) events & objects

## Installation

`pip install ocsf-pydantic`


## Usage

all event & object models are available via `ocsf`

```
from ocsf.events.application.api import Api

apievent: dict = ... # an OCSF normalized dict
APIActivity(**apievent)

```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
