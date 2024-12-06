# winzy-txt2img-val-town

[![PyPI](https://img.shields.io/pypi/v/winzy-txt2img-val-town.svg)](https://pypi.org/project/winzy-txt2img-val-town/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-txt2img-val-town?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-txt2img-val-town/releases)
[![Tests](https://github.com/sukhbinder/winzy-txt2img-val-town/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-txt2img-val-town/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-txt2img-val-town/blob/main/LICENSE)

Text to Image Gen Using Val Town's imggenurl 

## Installation

First configure your Winzy project [to use Winzy](https://github.com/sukhbinder/winzy).

Then install this plugin in the same environment as your Winzy application.
```bash
pip install winzy-txt2img-val-town
```
## Usage

Using as this 

```bash
winzy t2i a beautiful indian girl fair complepion looking at the camera smiling high definition realistic , stunning -s -hd
```

produces this

![a beautiful girl](image_0a6fa09d.png)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-txt2img-val-town
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
