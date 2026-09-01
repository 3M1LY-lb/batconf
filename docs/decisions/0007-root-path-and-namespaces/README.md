# Root Path and Namespaces (5 decisions)

Issues: #152 (root / default config path naming), #150 (multiple top-level
schemas)

A schema mounts at the root of a namespace the caller declares. No namespace
is derived from the source tree, and no reserved word stands in for the
root.

Five decisions build that up: what an absent path means, how the
environment namespace is named, how INI reaches a root it cannot spell, where
environment selection happens, and what a shared file and a shared process
environment can express. Each option below was measured against the
behaviour of the sources on the 1.0 line before the decision was taken.

| #  | Title                                                                                    | Status   |
| -- | ---------------------------------------------------------------------------------------- | -------- |
| 01 | [An absent path mounts the schema at the root](01-absent-path-mounts-at-root.md)          | Accepted |
| 02 | [A caller-declared environment-variable prefix](02-env-source-prefix.md)                  | Accepted |
| 03 | [The INI root section](03-ini-root-section.md)                                            | Accepted |
| 04 | [Environment selection layers above the sources](04-environment-selection-bootstrap.md)   | Accepted |
| 05 | [What a format and the process environment can express](05-format-environment-contract.md) | Accepted |

## Release schedule

Two deprecations land in 0.4.1 and are removed in 0.5.0: the
`path = config_class.__module__` fallback (01) and the hardcoded `BAT`
environment prefix (02). Both change documented behaviour, so both precede
the 1.0 freeze.

Decisions 03, 04 and 05 add capability or state a contract. None of them
removes a working behaviour.
