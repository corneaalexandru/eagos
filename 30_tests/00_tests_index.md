# ELAEF regression checks

The fixture suite checks project creation, refusals to overwrite, profile sizes, placeholder handling, link resolution, malformed properties, duplicate IDs, dependency cycles, lifecycle evidence, expiry, drift detection, and read-only behavior. It runs in temporary directories, requires no network or third-party package, and makes no real project commitment.

Run `python3 30_tests/01_test_elaef.py -v` from the package root. Direct execution supports the numbered filename; standard unittest discovery skips module names beginning with digits. These checks validate toolkit behavior; they do not replace a live project pilot or human handover acceptance.

Run `python3 30_tests/02_test_discovery.py -v` for the optional ODS extension. Disposable scenarios cover no-overwrite initialization, read-only checks, stable references, unknown ratings, track/claim scope, synthetic and unavailable sources, cumulative caps, hard filters, scoped selection, receiver acceptance, conditional handoffs, expired authority, and validation-slot continuity across cycles. All approvals and acknowledgments in fixtures are explicitly synthetic and are never copied into a live portfolio.

Discovery also covers portable interactive-starter initialization, a prose idea without formal research records, readable 1.0.0 workspaces and rejection of unsupported versions. These are file/validator checks, not automated tests of an AI conversation. Review the playbook's examples and the revision's scenario walkthrough separately.

The core suite reads `00_evidence_led_agent_execution_framework.md` and checks version 4.0.0 and all 24 consolidated sections. `ELAEF_SPEC_PATH` can select an explicit candidate. Meaning and actual authority still require content review.

Run `python3 30_tests/03_test_unified.py -v` for the unified interface integration checks. Run affected suites directly, then the core suite for toolkit changes. Portable guides are checked byte-for-byte against `04_operating_guide.md`, and disposable initialization verifies their installed paths and manifests. Optional lifecycle stages neither activate projects nor require old workspaces to adopt the field.

[Conversation scenarios](04_conversation_scenarios.md) define expected behavior across ideation, incubation, development, launch, operation, correction, pause/resumption, and missing tools. They are an evaluation specification, not passing model tests. Collect actual responses, owner feedback, and outcome evidence for live pilots.

Run `python3 30_tests/05_test_governance.py -v` for synthetic delegation, Task compatibility, runtime declarations, evidence impact, attempts, malformed inputs, legacy manifests and CLI parity. These tests cannot establish real runtime enforcement or operational acceptance. See [assurance](../08_validation_and_assurance.md).
