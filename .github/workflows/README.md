# Workflows used in iso3166-2

* `build_test.yml` - build and test the iso3166-2 application, running all unit tests.
* `deploy_test_pypi.yml` - after test workflow successful, deploy to test pypi server.
* `deploy_pypi.yml` - after deployment to test pypi server successful, deploy to main pypi server.
* `check_for_updates.yml` - workflow run using a CRON schedule every 3-6 months to check for the latest ISO 3166-2 updates using a custom-built GCP Cloud Function that updates the relevant ISO 3166-2 objects.