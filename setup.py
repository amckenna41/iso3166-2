###############################################################################
#####   Setup.py - installs all the required packages and dependancies    #####
###############################################################################

import pathlib
from setuptools import setup, find_packages
import sys

#software metadata
__name__ = 'iso3166-2'
__version__ = "1.0.2"
__description__ = "A Python package to access the most up-to-date and accurate info about countries and their associated subdivisons using the ISO3166-2 standard."
__author__ = 'AJ McKenna, https://github.com/amckenna41'
__authorEmail__ = 'amckenna41@qub.ac.uk'
__maintainer__ = "AJ McKenna"
__license__ = 'MIT'
__url__ = 'https://github.com/amckenna41/iso3166-2'
__download_url__ = "https://github.com/amckenna41/iso3166-2/archive/refs/heads/main.zip"
__status__ = 'Development'
__keywords__ = ["iso", "iso3166", "beautifulsoup", "python", "pypi", "countries", "country codes", \
            "iso3166-2", "iso3166-1", "alpha-2", "iso3166-updates", "rest countries"]
__test_suite__ = "tests"

#ensure python version is greater than 3
if (sys.version_info[0] < 3):
    sys.exit('Python 3 is the minimum version requirement.')

#get path to README file
HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(name=__name__,
      version=__version__,
      description=__description__,
      long_description = README,
      long_description_content_type = "text/markdown",
      author=__author__,
      author_email=__authorEmail__,
      maintainer=__maintainer__,
      license=__license__,
      url=__url__,
      download_url=__download_url__,
      keywords=__keywords__,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'License :: Free For Educational Use',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',	
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
      install_requires=[
          'requests>=2.28.1',
          'iso3166'
      ],
     test_suite=__test_suite__,
     packages=find_packages(),
     include_package_data=True,
     zip_safe=False)
