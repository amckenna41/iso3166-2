Welcome to ISO 3166-2's documentation 🌎!
=========================================

.. image:: https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png

**iso3166-2** is a lightweight custom-built Python package, and accompanying API, that can be 
used to access all of the world's ISO 3166-2 subdivision data. Here, subdivision can be used 
interchangeably with regions/states/provinces etc. Currently, the package and API supports 
data from 250 countries/territories, according to the ISO 3166-1 standard. The software uses 
another custom-built Python package called |iso3166_updates_repo_link| to ensure all the subdivision 
data is **accurate, reliable and up-to-date**. The ISO 3166-2 was first published in 1998 and as of 
June 2024 there are **5,039** codes defined in it.

.. |iso3166_updates_repo_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-updates" target="_blank">iso3166-updates</a>

There are 7 main data attributes available for each subdivision within the **iso3166-2** software:

* Name - subdivision name, as it is commonly known in English
* Local name - subdivision name in local language
* Code - ISO 3166-2 subdivision code
* Parent Code - subdivision's parent code
* Type - subdivision type, e.g. region, state, canton, parish etc
* Latitude/Longitude - subdivision coordinates
* Flag - subdivision flag from |iso3166_flag_icons_repo_link| repo

.. |iso3166_flag_icons_repo_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-flag-icons" target="_blank">iso3166-flag-icons</a>

.. note::

    A demo of the software and accompanying API is available |demo_link|!

    A Medium article about the **iso3166-2** software and API is available |medium_link|!

.. |demo_link| raw:: html

   <a href="https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing" target="_blank">here</a>

.. |medium_link| raw:: html

   <a href="https://ajmckenna69.medium.com/iso3166-2-71a13d9157f7" target="_blank">here</a>

Last Updated
============
The ISO 3166-2 data was last updated on **March 2024**. A log of the latest ISO 3166-2 updates can be seen in the 
|updates_md_link| file in the repository.

.. |updates_md_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-updates/blob/main/UPDATES.MD" target="_blank">UPDATES.md</a>

.. |license_repo_link| raw:: html

   <a href="https://github.com/amckenna41/iso3166-2/blob/main/LICENSE" target="_blank">MIT</a>

License
=======
**iso3166-2** is distributed under the |license_repo_link| License.

Contents
========
.. toctree::
   usage
   api
   contributing