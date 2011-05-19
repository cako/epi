try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'Epi',
    'author': 'Carlos Alberto da Costa Filho',
    'url': 'URL',
    'download_url': 'Download URL',
    'author_email': 'c.dacostaf@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)
