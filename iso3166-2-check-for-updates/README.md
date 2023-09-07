# ISO 3166-2 Check for Updates Function

<!-- [![check-for-updates](https://github.com/amckenna41/iso3166-2/workflows/Check%20for%20ISO3166%20Updates/badge.svg)](https://github.com/amckenna41/iso3166-2/actions?query=workflowCheck%20for%20ISO3166%20Updates) -->

**Checking for ISO 3166-2 Updates**

This Google Cloud Function is periodically called (usually every 3-6 months) automatically using a CRON sceduler. The function uses the `iso3166-2` Python software and API to pull all latest ISO 3166-2 data using the various data sources used in the software within a certain period e.g the past 3 - 6 months. The function compares the generated output with that of the existing ISO 3166-2 JSON in the Google Cloud Storage bucket and will replace this JSON to integrate the latest data found such that the main API returns the latest data. Ultimately, this function ensures that the software and assoicated APIs are up-to-date with the latest ISO 3166-2 information for all countries/territories/subdivisions etc. 

There is also functionality implemented that automatically creates a GitHub Issue on the [iso3166-2](https://github.com/amckenna41/iso3166-2), and [iso3166-flag-icons](https://github.com/amckenna41/iso3166-flag-icons) repositories. Each of these repos require the latest and most accurate ISO 3166-2 data. The creation of these Issues will notify the repository owner that changes are outstanding that need to be implemented into the JSONs of the [iso3166-2](https://github.com/amckenna41/iso3166-2) and [iso3166-flag-icons](https://github.com/amckenna41/iso3166-flag-icons) repos. 

Note, in the `check_for_updates.yml` workflow that is used to call the function periodically, the Cloud Function is created, called and then deleted. This is to save on resources and makes sense given the frequency the Function is called.

GCP Cloud Architecture 
------------------------

<p align="center">
  <img src="https://raw.githubusercontent.com/amckenna41/iso3166-2/main/iso3166-2-check-for-updates/gcp_architecture.png" alt="gcp_arch" height="200" width="400"/>
</p>