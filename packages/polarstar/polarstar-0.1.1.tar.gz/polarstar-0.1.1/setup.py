# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['polarstar']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['PolarStar = polarstar.__main__:main']}

setup_kwargs = {
    'name': 'polarstar',
    'version': '0.1.1',
    'description': 'Polar Star',
    'long_description': "# Polar Star\n\n[![PyPI](https://img.shields.io/pypi/v/PolarStar.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/PolarStar.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/PolarStar)][python version]\n[![License](https://img.shields.io/pypi/l/PolarStar)][license]\n\n[![Documentation Status](https://readthedocs.org/projects/polarstar/badge/?version=latest)](https://polarstar.readthedocs.io/en/latest/?badge=latest)\n[![Tests](https://github.com/juliogallinaro/PolarStar/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/juliogallinaro/PolarStar/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/PolarStar/\n[status]: https://pypi.org/project/PolarStar/\n[python version]: https://pypi.org/project/PolarStar\n[read the docs]: https://PolarStar.readthedocs.io/\n[tests]: https://github.com/juliogallinaro/PolarStar/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/juliogallinaro/PolarStar\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Polar Star_ via [pip] from [PyPI]:\n\n```console\n$ pip install PolarStar\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [GPL 3.0 license][license],\n_Polar Star_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/juliogallinaro/PolarStar/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/juliogallinaro/PolarStar/blob/main/LICENSE\n[contributor guide]: https://github.com/juliogallinaro/PolarStar/blob/main/CONTRIBUTING.md\n[command-line reference]: https://PolarStar.readthedocs.io/en/latest/usage.html\n",
    'author': 'Júlio Gallinaro Maranho and Patrícia Aparecida da Ana',
    'author_email': 'juliogallinaro@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/juliogallinaro/PolarStar',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
