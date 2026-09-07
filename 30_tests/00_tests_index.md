# ELAEF regression checks

The fixture suite checks project creation, refusals to overwrite, profile sizes, placeholder handling, link resolution, malformed properties, duplicate IDs, dependency cycles, lifecycle evidence, expiry, drift detection, and read-only behavior. It runs in temporary directories, requires no network or third-party package, and makes no real project commitment.

Run `python3 30_tests/01_test_elaef.py -v` from the package root. Direct execution supports the numbered filename; standard unittest discovery skips module names beginning with digits. These checks validate toolkit behavior; they do not replace a live project pilot or human handover acceptance.
