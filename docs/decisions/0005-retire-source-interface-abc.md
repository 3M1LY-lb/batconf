# ADR 0005 — Retire the `SourceInterface` ABC

Date: 2026-08-29
Status: Accepted

## Context

Two names express one contract — "an object with
`get(key, path) -> str | None`":

- `SourceInterfaceP`, a `Protocol` in `batconf.sources.types`
- `SourceInterface`, an `ABCMeta` class in `batconf.source`

Foundational ADR 07 blessed the Protocol as canonical and recorded the ABC
as a pragmatic workaround for mypy false positives, to be removed "once the
underlying type-checker limitations are resolved". It set no date, so the
duality persisted and spread: the file sources subclass the Protocol while
the environment and namespace sources subclassed the ABC, and the user
guide taught the ABC as a supported extension point.

Two costs follow. Contributors meet two answers to one question. More
seriously, `SourceInterface` is public API: leaving it in place through the
1.0 freeze turns a workaround into a permanent compatibility promise.

The type-checker limitation that motivated the ABC no longer reproduces.

## Decision

`SourceInterfaceP` is the sole source extension point. The built-in
sources all declare it, `SourceInterface` emits a `DeprecationWarning`
naming v0.5.0 as its removal version, and the guide and introduction teach
the Protocol only.

Classes already scheduled for removal in v0.5.0 keep the ABC as their base
through a private alias, so importing them raises no warning for a defect
their users cannot fix.

## Options considered

### Deprecate the ABC, bless `SourceInterfaceP` (chosen)

- One documented extension point before the 1.0 freeze [pro]
- Custom sources stay decoupled: no inheritance required [pro]
- Completes the direction foundational ADR 07 already set [pro]
- Code that subclasses the ABC must change before v0.5.0 [con]

### Keep both indefinitely

- No migration for existing subclassers [pro]
- Freezes a documented workaround into the 1.0 contract [con]
- Contributors keep meeting two answers to one question [con]

### Bless the ABC, drop the Protocol

- Type checkers have no ambiguity [pro]
- Forces third-party sources to inherit from batconf internals [con]
- Reverses ADR 07 and rewrites every file source [con]

## Rationale

The Protocol states the real contract: batconf calls `get`, and nothing
else. Requiring inheritance to express that couples every third-party
source to a batconf import for no checking the Protocol does not already
provide.

Timing decides the rest. The extension point is what third-party sources
build against, so it must be settled before the API freezes. The adopted
deprecation policy — deprecate and document in a patch release, remove in
the next minor — makes v0.4.1 the last patch line before v0.5.0, so the
warning ships now or the ABC survives into 1.0 by default.

Keeping the deprecated classes on the ABC through a private alias is
deliberate. They are removed in the same release as the ABC itself, so
migrating them would create churn and emit warnings that point users at a
base class they never chose.

## Consequences

- `from batconf.source import SourceInterface` emits a
  `DeprecationWarning`. The name still resolves to the ABC, so existing
  subclasses keep working until v0.5.0.
- Custom sources need no base class. Those wanting type-checker
  enforcement subclass `SourceInterfaceP` instead.
- v0.5.0 removes `SourceInterface`. The private alias and the deprecated
  classes holding it go in the same release.
- `isinstance` checks against `SourceInterface` must move to
  `SourceInterfaceP`, which is `runtime_checkable`.
