# What a format and the process environment can express

Date: 2026-09-01
Status: Accepted

## Context

Several projects share one config file and one process environment, and the
user moves between environments. The behaviour available to them today was
measured on the 1.0 line.

The `flat` and `sections` formats accept `config_env` and discard it. No
error is raised. Only `environments` holds several environments in one
file. A `flat` file has one key space, so two projects cannot both declare
`host`. Environment variables have no environment layer at all: a variable
exported while working in dev keeps overriding the file in stage and in
test until the user unsets it.

Once [an absent path is the root](01-absent-path-mounts-at-root.md), the
root of a file and the root of the process environment belong to no
project. Today the module name separates two projects by accident. After
the change, sharing is explicit and the rules for it must be stated.

## Decision

The environment dimension exists only where the medium expresses it.
batconf documents the contract and adds no layer.

- `flat` and `sections` carry no environment and ignore `config_env`. Only
  `environments` expresses a shared multi-environment file.
- `sections` holds several projects in one file, for one environment.
- Environment variables are environment-agnostic. The process environment
  is the environment.
- In a shared file or a shared process environment, every project declares
  its own name — its `path`, and its environment prefix — for every source
  it builds. The file root and the process-environment root belong to no
  one.

## Options considered

### Document the contract; each format keeps what it expresses (chosen)

- Each format states what it can hold, so a user picks the format from the
  requirement [pro]
- A caller that builds several sources and passes one `config_env` to all
  of them stays legal [pro]
- No source gains a dimension its medium does not have [pro]
- An ignored `config_env` is still silent, so the guide has to teach
  it [con]

### Raise when a format cannot use `config_env`

- A misunderstanding surfaces at construction instead of at the first
  wrong value [pro]
- Makes one uniform `config_env` illegal across a mixed source list, which
  is a legitimate configuration [con]
- Changes documented behaviour, so it needs the same pre-freeze window as
  the rest of this group and adds no capability [con]

### Give every source an environment layer

- One rule everywhere, and a `sections` file could then hold
  environments [pro]
- The process environment holds one environment because it is one; a second
  layer inside it invents state the medium does not have [con]
- Two sources could then disagree about the active environment, and nothing
  decides between them [con]

## Rationale

A file describes three environments at once because a file is data. A
process environment cannot, because it is the environment the process runs
in. The contract follows that difference instead of papering over it, and
each format keeps the capability it actually has.

The root is an ownership claim. A project that leaves its name unset claims
the shared root, and every other project that does the same reads the same
values, with no error. The library cannot detect this: it cannot know that
a file is shared. So the rule is a documented discipline rather than a
check.

Declaring the name is cheap because one declaration covers the files.
`path=` reaches every source through the frozen `get(key, path)` parameter,
so a project names itself once on `Configuration`. Only the environment
prefix is stated separately, and only because a project may want its
environment namespace to differ from its file namespace. See
[the environment prefix](02-env-source-prefix.md).

## Consequences

- A user who moves between environments needs the `environments` format, or
  one file per environment.
- `flat` is single-tenant. A shared file cannot use it.
- Every project reading a shared file must agree on one `file_format`. An
  `environments` file read as `sections` returns nothing.
- One file holds one `default_env`, and the file owns it. A project that
  wants a different environment passes `config_env=`. See
  [environment selection](04-environment-selection-bootstrap.md).
- An exported variable outlives every edit to the file and keeps overriding
  until it is unset. This is the sharpest hazard in the shared case, and
  the guide must state it.
- In INI, `[DEFAULT]` keys inherit into every declared section, so one
  project can leak a key into every other project's sections.
