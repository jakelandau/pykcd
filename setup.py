from setuptools import setup

setup(name='pykcd',
      version = '0.2.2',
      description = 'Python interface for the XKCD API',
      url = 'http://github.com/JacobLandau/pykcd',
      author = 'Jacob Landau',
      author_email = 'Jacob@PopcornFlicks.ca',
      license = 'MIT',
      packages = ['pykcd'],
      install_requires = ['BeautifulSoup4', 'requests', 'wget'],
      zip_safe = False)