# bookit [![](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www,python.org/downloads/)

Build Tool:
- Poetry: https://python-poetry.org/docs/
`curl -sSL https://install.python-poetry.org | python3 -`
Verify poetry installation with:
`$ poetry --version`


## Contributing

### Local Environment Setup
- pyenv via homebrew
- Python 3.11 via pyenv
- Poetry via poetry installer
    - add to path

### Adding Dependencies
For runtime dependencies that should be included in the distribution package:
`$ poetry add <library>`

For development dependencies (`pytest`, `mock`, etc.) that should be excluded from the distribution package:
`$ poetry add --dev <library>`

### Running Tests Locally
`$ poetry run pytest`


### Running the Bot
From `bookit/bookit` directory:
`$ poetry run python resy_booking_bot.py`


### Workflow & Architecture
User steps:
- User defines desired reservation details in `resy.ini`

Bot steps:
- Start at time defined in `resy.ini`
- Find all available reservation slots 
- Filter on user-defined criteria (table type, time)
