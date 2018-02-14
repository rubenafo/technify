from setuptools import setup, find_packages

setup(
  name = 'technify',
  packages = find_packages(),
  version = '0.6.5',
  description = 'A framework to run technical analysis. Powered by pandas and ta-lib.',
  author = 'Ruben Afonso',
  author_email = 'rbfrancos@gmail.com',
  url = 'https://github.com/rubenafo/technify', 
  download_url = 'https://github.com/rubenafo/technify/archive/0.6.5.zip',
  keywords = ['technical-analysis', 'pandas', 'finance','stock'],
  classifiers = [],
  install_requires = ["yfm", "quandl","ta-lib"]
)

