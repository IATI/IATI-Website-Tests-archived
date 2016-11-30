IATI Website Tests - Detail
===========================

The tests contained within this repository are high level smoke and sanity tests to check that IATI websites and web tools are available and functioning roughly as expected. They are not designed to test every last user interaction, input, etc.

There are two categories of tests - website tests, and server tests. The website tests check the functionality of public-facing websites and web tools. The server tests check the functionality of the server(s) that run the afore-mentioned services.

All tests utilise `py.test` as the test framework.

Website Tests
-------------

The website tests are based upon a core shared functionality located within `web_test_base.py`. All other web tests inherit from this core functionality.

Server Tests
------------

The server tests also use py.test, however do not inherit from the same base class as the website tests.
