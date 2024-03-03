Welcome to ISO 3166-2's documentation 🌎!
=========================================

.. image:: https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png

**iso3166-2** is a lightweight custom-built Python package, and accompanying API, that can be 
used to access all of the world's ISO 3166-2 subdivision data. Here, subdivision can be used 
interchangably with regions/states/provinces etc. Currently, the package and API supports 
data from 250 countries/territories, according to the ISO 3166-1 standard. The software uses 
another custom-built Python package called `iso3166-updates <https://github.com/amckenna41/iso3166-updates/>`_ 
to ensure all the subdivision data is **accurate, reliable and up-to-date**. The ISO 3166-2 was first published in 1998 
and as of November 2023 there are **5,039** codes defined in it.

There are 7 main data attributes available for each subdivision within the **iso3166-2** software:

* Name - subdivsion name, as it is commonly known in English
* Local name - subdivision name in local language
* Code - ISO 3166-2 subdivision code
* Parent Code - subdivision's parent code
* Type - subdivision type, e.g. region, state, canton, parish etc
* Latitude/Longitude - subdivision coordinates
* Flag - subdivsion flag from `iso3166-flag-icons <https://github.com/amckenna41/iso3166-flag-icons/>`_ repo

.. note::

    A demo of the software and accompanying API is 
    available `here <https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing/>`_!

Last Updated
============
The ISO 3166-2 data was last updated on March 2023. A log of the latest ISO 3166-2 updates can be seen in the 
`UPDATES.md <https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.md/>`_ file in the repository.

License
=======
**iso3166-2** is distributed under the MIT License.
   
.. Changelog
.. =========

.. Latest Version: **1.5.0**.

.. ******
.. v1.5.0
.. ******
.. * Change data encapsulation making data accessible only via creating an instance of ISO3166_2 class
.. * Update search functionality algorithm in search functionality - chaning from difflib to thefuzz library
.. * Bug fixes for search by subdivision name algorithm in software and API
.. * Update unit tests to reflect changes made to the softwar
.. * Update name of iso3166_2_updates dir
.. * Update software and API documentation

.. ******
.. v1.4.0
.. ******
.. * Add readthedocs documentation
.. * Add search by subdivision name functionality
.. * Add custom subdivision functionality
.. * Update requirements.txt to include iso3166-2
.. * Update software pypi description
.. * Update unit tests to reflect changes made to the software
.. * Fix issue with accessing the function outputs for test_get_iso3166_2 unit tests

.. ******
.. v1.3.0
.. ******
.. * Add UPDATES.md file that outlines all subdivision added to json object
.. * Add iso3166-2-updates/subdivision_updates.csv file that lists changes that need to be applied to the ISO 3166-2 object taken from the `iso3166-updates <https://github.com/amckenna41/iso3166-updates>`_ software
.. * Add iso3166-2-updates/local_names.csv that lists the names of subdivisions in their local language
.. * Add iso3166_2_scripts/update_subdivisions.py script that is used to parse the subdivision_updates.csv file and append the data to the main object
.. * Update unit tests to reflect changes made to the software
.. * Update software keywords and description
.. * Update API.md
.. * Fix subdivision sorting in main software script
.. * Fix list of requirements for get_iso3166_2.py script

Contents
========
.. toctree::
   usage
   api
   contributing