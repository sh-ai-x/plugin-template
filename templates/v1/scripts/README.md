# Scripts

Put deterministic, testable helpers here when a behavior is shared by more than one skill or hook.
Scripts should accept explicit inputs, avoid global state, and resolve paths from the current plugin
root. Keep host-specific wrappers in the host adapter rather than branching shared logic silently.
