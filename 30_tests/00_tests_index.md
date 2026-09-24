# EAGOS regression checks

Run `python3 30_tests/06_test_workflows.py -v` for complete offline paths: preview/setup, reversible output creation, fresh-process resumption after a folder move, missing-output detection, gate correction, receipt and revocation. Investigation without invented selection is tested in the portfolio owner’s workspace. Temporary artifacts are real; inputs/authority are synthetic. These checks do not measure an AI conversation or enforce a running worker's permissions.

The fixture suite checks project creation, refusals to overwrite, profile sizes, placeholder handling, link resolution, malformed properties, duplicate IDs, dependency cycles, lifecycle evidence, expiry, drift detection, and read-only behavior. It runs in temporary directories, requires no network or third-party package, and makes no real project commitment.

Run `python3 30_tests/01_test_eagos.py -v` from the package root. Direct execution supports the numbered filename; standard unittest discovery skips module names beginning with digits. These checks validate toolkit behavior; they do not replace a live project pilot or human handover acceptance.

Run `python3 30_tests/02_test_discovery.py -v` for the retired discovery CLI compatibility boundary. The original discovery investigation workflow tests moved with the portfolio owner. Core tests remain standalone.

The core suite reads `00_eagos.md` and checks version 4.0.0 and all 24 consolidated sections. `EAGOS_SPEC_PATH` can select an explicit candidate. Meaning and actual authority still require content review.

Run `python3 30_tests/03_test_unified.py -v` for the unified interface integration checks. Run affected suites directly, then the core suite for toolkit changes. Portable guides are checked byte-for-byte against `04_operating_guide.md`, and disposable initialization verifies their installed paths and manifests. Optional lifecycle stages neither activate projects nor require old workspaces to adopt the field.

[Conversation scenarios](04_conversation_scenarios.md) define expected behavior across ideation, incubation, development, launch, operation, correction, pause/resumption, and missing tools. They are an evaluation specification, not passing model tests. Collect actual responses, owner feedback, and outcome evidence for live pilots.

Core audit regression coverage checks excluded anchor/entrypoint reads, blank evidence entries, declared self-approval and activation-decision date bounds. Detailed opportunity-selection and claim-evidence scenarios are maintained with the portfolio owner’s discovery records.

Run `python3 30_tests/05_test_governance.py -v` for synthetic delegation, Task compatibility, runtime declarations, evidence impact, attempts, malformed inputs, legacy manifests and CLI parity. These tests cannot establish real runtime enforcement or operational acceptance. See [assurance](../08_validation_and_assurance.md).
