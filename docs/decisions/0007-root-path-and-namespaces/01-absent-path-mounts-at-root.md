# An absent path mounts the schema at the root

Date: 2026-09-01
Status: Accepted

## Context

`Configuration` addresses every value by a dotted path. When the caller
supplies no path, the path becomes the Python module name of the schema
class. Every lookup uses that value. Sub-configurations append their field
name to it, the tree header prints it, and the missing-value message builds
its file and environment guidance from it.

Three costs follow.

The module name leaks into the config file and into the environment. A file
must name its top section after a Python module, so moving or renaming a
module breaks a working file. The project's own test data carries the
workaround.
[Foundational ADR 04](../0000-foundational/04-module-path-namespace.md)
already records the module default as a compatibility retention, not the
preferred style.

The root is unreachable. The path is tested for truth, not for `None`, so an
empty string and an omitted argument produce the same module name. A
`Configuration` therefore never passes an empty path to a source, and the
no-path branch that every source carries is unreachable behind it.

The module name is also an accidental namespace. It separates two projects
that share one file only because their schemas sit in different packages.
The design gives neither project a namespace it chose.

The 1.0 freeze sets the schedule. Retiring the fallback changes the section
name a working file must use. That is a documented behaviour change, so
after the freeze it needs a major release.

## Decision

An absent or empty `path` mounts the schema at the root of the namespace.
`Configuration` no longer falls back to `config_class.__module__`. The
fallback is deprecated in 0.4.1 and removed in 0.5.0.

The spelling is the bare call, `Configuration(sources, MySchema)`. No
sentinel object and no reserved path string ship.

Schemas compose; the path anchors. One schema class mounts at the root when
it stands alone, and mounts under a field name when a larger schema holds
it. It resolves the same names either way.

## Options considered

### An absent path is the root (chosen)

- No reserved word exists, so nothing can collide with a module name, a
  config file key, or a future package name [pro]
- The root is the absence of a prefix, which is what the file formats
  already mean by it [pro]
- A schema needs no marker to stand alone or to nest, so composition needs
  no special case [pro]
- It changes the namespace of every configuration built without a path, so
  it must precede the 1.0 freeze [con]

### A reserved path token, `/ROOT/`

- Additive: a new accepted value for `path`, with the module fallback left
  in place [pro]
- A module name cannot contain `/`, so no value shadows the token [pro]
- `Configuration` must strip the token before any source sees it, and a
  source that receives it composes a nonsense key [con]
- The token is hand-spelled at every call site, and a misspelling reads as
  an ordinary namespace rather than as an error [con]

### A sentinel object, `batconf.ROOT`

- Explicit at the call site, visible to an IDE, and impossible to misspell
  in silence [pro]
- Additive, and the frozen `get(key, path)` signature is untouched [pro]
- Widens the type of a public constructor parameter that third-party code
  forwards [con]
- Cannot be written in a config file or on a command line, so a
  string-driven entry point still needs a spelling for the root [con]

### A structured path of segments, root is `()`

- Emptiness is unambiguous, and no source splits a string [pro]
- Changes the frozen `get(key, path)` signature and breaks every
  third-party source [con]
- Reopens [ADR 0002](../0002-get-path-parameter.md) for a benefit that is
  mostly internal tidiness [con]

## Rationale

This is the simplest change that reaches the goal. Every other option adds
a second way to work around the module default. This one removes the
default.

The token and the sentinel both keep a namespace the project never chose,
and both pay for the root with a new name that callers must learn. The
sentinel is the strongest of them: it is explicit and typo-proof. It was
rejected because the bare call already says the same thing, and because a
widened public parameter type is a permanent cost paid for a spelling.

An empty root also satisfies the multiple-top-level-schema request (#150)
by construction rather than by a strip step that every source, including
third-party sources, would have to perform correctly. No `ROOT` level
appears in the file and no `ROOT_` prefix appears in the environment,
because nothing is there to appear.

The shape matches the media the library reads. A TOML document has a
nameless root table. A JSON Pointer addresses the root with the empty
string. Comparable config libraries default their environment prefix to the
empty string. Path languages reserve a sigil for the root; config libraries
use no token at all, and this is a config library.

The cost is a break, which is why it lands under the deprecation cycle and
before the freeze: warn in 0.4.1, remove in 0.5.0.

## Consequences

- A configuration that relies on the module-name namespace must set `path=`
  explicitly. It warns from 0.4.1 and fails to resolve from 0.5.0.
- Root-level environment lookups lose their prefix. See
  [the environment prefix](02-env-source-prefix.md).
- INI cannot represent an unnamed section. See
  [the INI root section](03-ini-root-section.md).
- The root belongs to no project. See
  [the format and environment contract](05-format-environment-contract.md)
  for what a project in a shared file must declare.
- At the root there is no path to print. The tree header and the
  missing-value message need a display label that is not a lookup prefix.
- Several top-level schemas can hang under one configuration. A synthetic
  parent is a `Configuration` with an empty path (#150).
