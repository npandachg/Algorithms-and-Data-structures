try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Basic Algorithms and Data Structures',
    'author': 'Nishant Panda',
    'url': 'https://github.com/npandachg/Algorithms-and-Data-structures.git',
    'author_email': 'nishant.panda@gmail.com',
    'version': '0.1',
    'packages': ['AlgoDS'],
    'name': 'AlgoDS'
}

setup(**config)
