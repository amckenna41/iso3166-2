from .iso3166_2 import *
from .exceptions import *
from importlib.metadata import version as _pkg_version

#software metadata
__name__ = 'iso3166-2'
try:
    __version__ = _pkg_version("iso3166-2")
except Exception:
    __version__ = "1.8.3"  # fallback for development installs
__description__ = "A lightweight Python package, and accompanying RESTful API, used to access ALL of the world's most up-to-date and accurate ISO 3166-2 subdivision/regional data, including: subdivision code, name, local/other names, parent code, type, latitude/longitude, flag and history."
__author__ = 'AJ McKenna, https://github.com/amckenna41'
__authorEmail__ = 'amckenna41@qub.ac.uk'
__maintainer__ = "AJ McKenna"
__license__ = 'MIT'
__url__ = 'https://github.com/amckenna41/iso3166-2'
__download_url__ = "https://github.com/amckenna41/iso3166-2/archive/refs/heads/main.zip"
__status__ = 'Production/Stable'
__keywords__ = ["iso", "iso3166", "python", "pypi", "countries", "subdivisions",
            "country codes", "iso3166-2", "iso3166-1", "alpha-2", "iso3166-updates", "iso3166-flags", "regions", "dataset"]
__test_suite__ = "tests"