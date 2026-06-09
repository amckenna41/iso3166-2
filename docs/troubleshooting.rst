Troubleshooting
===============

This page lists common issues and how to resolve them quickly.

Invalid Country Or Subdivision Code
-----------------------------------
If you pass an invalid country or subdivision code, the package now raises a custom error
with suggestions:

.. code-block:: python

   from iso3166_2 import Subdivisions

   iso = Subdivisions()
   iso["DE-BER"]  # raises SubdivisionNotFound with "Did you mean..."

Tips:

* Use ISO 3166-1 alpha-2/alpha-3/numeric country codes.
* For subdivision lookups, use valid ISO 3166-2 format (for example ``DE-BE``).

Search Returns Too Many Results
-------------------------------
Tune search relevance and filter down the result set:

.. code-block:: python

   iso.search(
       "Berlin",
       likeness_score=90,
       subdivision_type="Land",
       region="DE",
       exclude_match_score=False,
   )

Tips:

* Increase ``likeness_score`` for stricter matching.
* Use ``subdivision_type``, ``parent_code`` and ``region`` filters together.

Search Returns No Results
-------------------------
Try one or more of the following:

* Lower ``likeness_score`` (for example from 100 to 80).
* Enable local name search: ``local_other_name_search=True``.
* Remove strict filters like ``subdivision_type`` or ``parent_code``.

Reverse Lookup (Coordinates) Returns Empty List
------------------------------------------------
When using ``reverse_lookup``, an empty list usually means no subdivision centroid is
inside your search radius.

.. code-block:: python

   iso.reverse_lookup(52.5174, 13.3951, radius_km=75, region="DE")

Tips:

* Increase ``radius_km``.
* Remove ``region`` filter if you are close to a border.
* Verify latitude/longitude order is ``(lat, lng)``.

CLI Command Errors
------------------
Use ``--help`` with any command:

.. code-block:: console

   iso3166-2 --help
   iso3166-2 search --help
   iso3166-2 reverse --help

If you receive an import error in a local clone, run commands from the repository root
or install editable mode:

.. code-block:: console

   pip install -e .

Typing Support In IDEs
----------------------
The package ships a ``py.typed`` marker so type checkers can consume package type hints.

If your IDE still does not show hints:

* Rebuild/reload your Python environment.
* Ensure the interpreter points to the environment where ``iso3166-2`` is installed.
