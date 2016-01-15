from setuptools import setup

setup(name='pykcd',
    version = '1.0.1',
    description = 'Python interface/wrapper for the XKCD API',
    url = 'https://github.com/JacobLandau/pykcd',
    author = 'Jacob Landau',
    author_email = 'Jacob@PopcornFlicks.ca',
    license = 'MIT',
    packages = ['pykcd'],
    install_requires = ['BeautifulSoup4', 'requests', 'wget', 'lxml'],
    zip_safe = False)
