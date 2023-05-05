# Workflows used in iso3166-2

* `build_test.yml` - build and test the iso3166-2 application, running all unit tests.
* `deploy_test_pypi.yml` - after test workflow successful, deploy to test pypi server.
* `deploy_pypi.yml` - after deployment to test pypi server successful, deploy to main pypi server.