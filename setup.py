from setuptools import setup, find_packages

setup(
  name = 'technify',
  packages = find_packages(),
  version = '0.8.0',
  description = 'A framework to run technical analysis. Powered by pandas and ta-lib.',
  author = 'Ruben Afonso',
  author_email = 'rbfrancos@gmail.com',
  url = 'https://github.com/rubenafo/technify', 
  download_url = 'https://github.com/rubenafo/technify/archive/0.8.0.zip',
  keywords = ['technical-analysis', 'pandas', 'finance','stock', 'ta-lib'],
  classifiers = [],
  install_requires = ["quandl","ta-lib"]
)

