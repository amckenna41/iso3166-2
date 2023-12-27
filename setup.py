###############################################################################
#####   Setup.py - installs all the required packages and dependancies    #####
###############################################################################

import pathlib
from setuptools import setup, find_packages

#software metadata
__name__ = 'iso3166-2'
__version__ = "1.4.0"
__description__ = "A lightweight Python package, and accompanying API, that can be used to access all of the world's most up-to-date and accurate ISO 3166-2 subdivision data, including: name, local name, code, parent code, type, latitude/longitude and flag."
__author__ = 'AJ McKenna, https://github.com/amckenna41'
__authorEmail__ = 'amckenna41@qub.ac.uk'
__maintainer__ = "AJ McKenna"
__license__ = 'MIT'
__url__ = 'https://github.com/amckenna41/iso3166-2'
__download_url__ = "https://github.com/amckenna41/iso3166-2/archive/refs/heads/main.zip"
__status__ = 'Production'
__keywords__ = ["iso", "iso3166", "beautifulsoup", "python", "pypi", "countries", "country codes", \
            "iso3166-2", "iso3166-1", "alpha-2", "iso3166-updates", "subdivisions"]
__test_suite__ = "tests"

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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'License :: Free For Educational Use',
        'Natural Language :: English',
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
          'iso3166',
          'natsort'
      ],
     test_suite=__test_suite__,
     packages=find_packages(),
     include_package_data=True,
     zip_safe=False)
