Welcome to ISO 3166-2's documentation 🌎!
=========================================

.. image:: https://img.shields.io/pypi/v/iso3166-2
   :target: https://pypi.org/project/iso3166-2/
   :alt: iso3166_2

.. image:: https://github.com/amckenna41/iso3166-2/workflows/Building%20and%20Testing/badge.svg
   :target: https://github.com/amckenna41/iso3166-2/actions?query=workflow:Building%20and%20Testing
   :alt: pytest

.. image:: https://img.shields.io/github/license/amckenna41/iso3166-2
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

.. image:: https://codecov.io/gh/amckenna41/iso3166-2/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/amckenna41/iso3166-2
   :alt: codecov

.. image:: https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png

Introduction
============
**iso3166-2** is a lightweight custom-built Python package, and accompanying RESTfulAPI, that can be 
used to access all of the world's ISO 3166-2 subdivision data. Here, subdivision can be used 
interchangeably with regions/states/provinces etc. Currently, the package and API supports 
data from **250** countries/territories, according to the ISO 3166-1 standard. The software uses 
another custom-built Python package called |iso3166_updates_repo_link| to ensure all the subdivision 
data is **accurate, reliable and up-to-date**. The ISO 3166-2 was first published in 1998 and as of 
December 2025 there are **5,046** codes defined in it.

The ISO 3166-2 standard is part of the broader ISO 3166 family, maintained by the International Organization 
for Standardization (ISO). It provides codes for the names of the principal subdivisions (e.g., provinces or states) 
of all countries that have codes defined in ISO 3166-1. These codes are widely used in geopolitics, logistics, 
statistics, and software systems for consistent country and region identification.

There are 7 main data attributes available for each subdivision/subdivision code within the **iso3166-2** software:

* **Name** - subdivision name, as it is commonly known in English
* **Local/other name** - subdivision name in local language or any alternative names its known by
* **Latitude/Longitude** - subdivision coordinates
* **Flag** - subdivision flag from the custom-built |iso3166_flag_icons_repo_link| repo
* **Parent Code** - subdivision's parent code
* **Type** - subdivision type, e.g. region, state, canton, parish etc
* **History** - historical updates/changes to the subdivision and its data, from the custom-built |iso3166_updates_repo_link| repo

Bespoke Features
----------------
There are three main attributes supported by the software that make it stand out and add a significant amount of value and data per subdivision,  
in comparison to some the other iso3166-2 datasets, these are the **local/other name**, **flag** and **history** attributes.

Local/other name
~~~~~~~~~~~~~~~~
The ``localOtherName`` attribute is built from a custom dataset of local language variants and alternative names/nicknames for the **over 5000** subdivisions. In total 
there are **\>3700** local/other names for the **\>5000** subdivisions. Primarily the attribute contains local language translations for the 
subdivisions related to the subdivision, but many also include **nicknames** and **other variants** that the subdivision may be known by, 
either locally or globally. 

For each local/other name, the **ISO 639** 3 letter language code is used to identify the language of the name. Some translations do not have 
available ISO 639 codes, therefore the |glottolog_link| or other databases (e.g |ietf_link|) language codes are used. Some example local/other name entries are: 

* **Sindh (Pakistan PK-SD)** - "سِنْدھ (urd), Sindh (eng), SD (eng), Mehran/Gateway (eng), Bab-ul-Islam/Gateway of Islam (eng)"
* **Central Singapore (Singapore SG-01)** - "Pusat Singapura (msa), 新加坡中部 (zho), மத்திய சிங்கப்பூர் (tam)"
* **Bobonaro (East Timor TL-BO)** - "Bobonaru (tet), Buburnaru (tet), Tall eucalypt (eng)"
* **Wyoming (USA US-WY)** - "Equality State (eng), Cowboy State (eng), Big Wyoming (eng)"

The full dataset of local/other names is available in the repo here |local_other_names_link|.

Flags
~~~~~
The other equally important and bespoke/unique attribute that the software package supports is the ``flag`` attribute, which is a link to the subdivision's 
flag on the |iso3166_flag_icons_repo_link| repo. This is another **custom-built** repository, (alongside |iso3166_2_repo_link| and |iso3166_updates_repo_link|) 
that stores a rich and comprehensive dataset of over **2800** official individual subdivision flags, alongside ~250 ISO 3166-1 country/territory flags.

The flags repo uses the |iso3166_2_repo_link| software to get the full list of ISO 3166-2 subdivision codes which is kept up-to-date and accurate via the |iso3166_updates_repo_link| software.

.. raw:: html

   <div align="center">❤️ iso3166-2 🤝 iso3166-updates 🤝 iso3166-flags ❤️</div>


History
~~~~~~~
The ``history`` attribute has any applicable historical updates/changes to the individual subdivisions. The data source for this is another 
custom-built software package previously mentioned called |iso3166_updates_repo_link|. This package keeps track of all the published changes that the ISO make to 
the ISO 3166 standard which include addition of new subdivisions, deletion of existing subdivisions or amendments to existing subdivisions. Thus 
|iso3166_updates_repo_link| helps ensure that the data in the `iso3166-2` package is also kept **up-to-date** and **accurate**. If any updates are found for the subdivision 
a short description of the change, it's publication date as well as its source will be included.

.. raw:: html

   <div align="center">❤️ iso3166-2 🤝 iso3166-updates ❤️</div>

.. Demographics
.. ~~~~~~~~~~~
.. Two additional bespoke attributes that have been recently added to the software are the ``area`` and ``population`` attributes. These attributes
.. provide the latest key demographic information about each subdivision. The data for these attributes is sourced via the |wikidata_link| SPARQL 
.. endpoint and is regularly updated to ensure accuracy. 

Upcoming Features
=================
There are several new features and attributes that are currently being worked on and will be added to the software package in the near future. These include:
* **Demographics** - addition of key demographic data attributes such as area, population, population density etc for each subdivision
* **Enhanced Geo Data** - addition of more detailed geo data attributes such as bounding box and geojson (these attributes are exportable via the custom scripts but yet to be implemented into the dataset)

Version
=======
The **iso3166-2** software is currently at version |version_link|.

Last Updated
============
The ISO 3166-2 data was last updated on **June 2025**. A log of the latest ISO 3166-2 updates can be seen in the 
|updates_md_link| file in the repository.

License
=======
**iso3166-2** is distributed under the |license_repo_link| license.

Contributing
============

If you have found a bug or an issue in the software or API then please raise an issue on the 
repository's |issues_link| tab.

If you would like to contribute any functional/feature changes to the software, please make a pull
request on the |repo_link|.

Any other queries or issues, please contact me via email: amckenna41@qub.ac.uk.

Credits
=======
The Python software and accompanying API are solely developed and maintained by |me_link| 😁. 


.. note:: 


    A demo of the software and accompanying API is available |demo_link|!

    A Medium article about the **iso3166-2** software and API is available |medium_link|!

.. |iso3166_2_repo_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-2" target="_blank">iso3166-2</a>

.. |iso3166_updates_repo_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-updates" target="_blank">iso3166-updates</a>

.. |iso3166_flag_icons_repo_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-flags" target="_blank">iso3166-flags</a>

.. |local_other_names_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-2/iso3166_2_resources/local_other_names.csv" target="_blank">local_other_names.csv</a>

.. |glottolog_link| raw:: html

   <a href="https://glottolog.org/" target="_blank">Glottolog</a>

.. |ietf_link| raw:: html

   <a href="https://support.elucidat.com/hc/en-us/articles/6068623875217-IETF-language-tags" target="_blank">IETF</a>

.. |version_link| raw:: html

   <a href="https://pypi.org/project/iso3166-2/" target="_blank">v1.8.1</a>

.. |updates_md_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.MD" target="_blank">UPDATES.md</a>

.. |license_repo_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-2/blob/main/LICENSE" target="_blank">MIT</a>

.. |issues_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-2/issues/" target="_blank">Issues</a>

.. |repo_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-2/" target="_blank">repository</a>

.. |demo_location_link| raw:: html

   <a href="" target="_blank">here</a>

.. |demo_link| raw:: html

   <a href="https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing" target="_blank">here</a>

.. |medium_link| raw:: html

   <a href="https://ajmckenna69.medium.com/iso3166-2-71a13d9157f7" target="_blank">here</a>

.. |me_link| raw:: html

   <a href="https://github.com/amckenna41" target="_blank">me</a>

.. |wikidata_link| raw:: html

   <a href="https://query.wikidata.org/" target="_blank">Wikidata</a>


Contents
========
.. toctree::
   :maxdepth: 2

   usage
   api
   changelog

`Back to top ↑ <#welcome-to-iso-3166-2-s-documentation>`_