# Environment selection layers above the sources

Date: 2026-09-01
Status: Proposed

## Context

A file source resolves the active environment from the `config_env`
argument, and otherwise from the `default_env` key in the file.
[Foundational ADR 05](../0000-foundational/05-multi-environment-file-format.md)
records the environment override as something the caller reads and passes
as `config_env`.

Users want a shell-level selector: one variable that names the environment
for every tool started in that shell. Nothing in the library reads such a
variable, and no batconf-owned variable exists. The question is whether the
sources should read one.

The same question governs other pre-configuration facts. Which config file
to read, and where to look for it, must be known before the configuration
that would describe them can be built.

## Decision

Sources never read `BATCONF_ENVIRONMENT`. The variable is the canonical
shell-level environment selector, and it is permanent. It is canonical, not
enforced: a project may select its environment another way.

The blessed layering pattern is the two-stage bootstrap. A bootstrap
`Configuration` mounts at the root over `EnvSource(prefix='batconf')`, and
optionally over a bootstrap file. Every field it declares therefore lands in
the reserved namespace: `environment` reads `BATCONF_ENVIRONMENT`, and
`config_file` reads `BATCONF_CONFIG_FILE`. It carries the environment name,
the config file paths, and other pre-configuration metadata. The real
configuration is then built with `config_env=` taken from the bootstrap
value.

Precedence is: an explicit `config_env=` first, `BATCONF_ENVIRONMENT` next
through the bootstrap, and the file's `default_env` last.

The file key stays `default_env`. The argument stays `config_env=`.

Reading `BATCONF_ENVIRONMENT` through the bootstrap prefix is the sanctioned
use of the reserved namespace. A bootstrap that also needs a genuinely
ambient value, such as `$HOME`, adds a second `EnvSource(raw=True)`. The two
are separate sources because a prefix applies to every lookup its source
serves. See [the environment prefix](02-env-source-prefix.md).

## Options considered

### A two-stage bootstrap, with sources left as readers (chosen)

- The environment is decided once, at construction, where the caller can
  see it [pro]
- The bootstrap is an ordinary `Configuration`, so the pattern needs no new
  machinery [pro]
- No source gains a semantic contract that third-party sources would have
  to honour [pro]
- The caller writes two constructions instead of one [con]

### Every source reads the variable

- The shell selects the environment with no code in the caller [pro]
- Each source must implement the same read, third-party sources included,
  and none of them can be made to [con]
- A source's answer then depends on ambient state that its arguments do not
  show [con]

### `Configuration` reads the variable and passes it down

- One implementation, and the sources stay pure [pro]
- Bakes one variable name into the manager, where a project cannot
  substitute its own [con]
- Construction depends on ambient state invisibly, so two identical calls
  differ by shell [con]

### No blessed pattern; each caller reads the variable

- The status quo, and it costs nothing [pro]
- Every project invents its own bootstrap [con]
- No canonical name exists, so tools sharing one shell disagree about which
  variable selects the environment [con]

## Rationale

Context belongs at construction time. A source reads one medium and answers
for one key. Which environment the program runs in is not a fact about a
medium, and a source that decided it would be answering a question nobody
asked it.

Keeping the decision above the sources leaves no cross-source semantic
contract to enforce. That matters because the source interface is open:
anyone may implement `SourceInterfaceP`, and a rule that only the shipped
sources follow is not a rule.

The bootstrap needs no new machinery because it is the library reading its
own settings with its own tool. The root mount is what makes it cheap: a
bootstrap configuration mounts at the root and needs no namespace of its
own.

The names do not change. `default_env` and `config_env=` are documented
surface, and renaming them buys nothing.

The pattern also has room to grow. A future default-configuration factory
absorbs it, so a caller gets both stages from one call. Under that factory,
operating-system config-directory defaults become field values on the
bootstrap schema, rather than search behaviour baked into every source.

## Consequences

- `BATCONF_ENVIRONMENT` is permanent and documented. It is canonical, not
  enforced.
- No source reads an environment variable to decide its own environment. A
  source that did would break the precedence order.
- The bootstrap is the only sanctioned reader of the reserved `BATCONF_*`
  namespace.
- Precedence is fixed: `config_env=`, then `BATCONF_ENVIRONMENT`, then
  `default_env`.
- A future default-configuration factory implements this pattern; it does
  not change it. Config-directory defaults belong on the bootstrap schema.
- The environment layer applies to files. Environment variables carry no
  environment. See
  [the format and environment contract](05-format-environment-contract.md).
