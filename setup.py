__author__ = 'Sahat'

from setuptools import setup, find_packages

setup(
    name='Papertalk',
    version="0.0.1",
    author='Papertalk',
    author_email='krmckelv@gmail.com',
    description='Discuss articles online',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'beautifulsoup', 'Flask-PyMongo', 'werkzeug'],
    entry_points={
      'console_scripts': [
          'papertalk = papertalk.server:main',
      ]
    },
)

