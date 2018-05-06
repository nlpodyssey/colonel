Colonel Changelog
=================


v1.2.0
------

New features
^^^^^^^^^^^^

- Added direct access from the root package to the main classes, including
  `Sentence`, sentence elements and `UposTag` (also refer to the newly
  introduced `colonel.__all__`)


v1.1.1
------

Fixes and housekeeping
^^^^^^^^^^^^^^^^^^^^^^

- Fixed missing version in sphinx configuration script
- Updated sphinx documentation, better showing modules and packages and
  defining a meaningful TOC
- Upgraded sphinx related development dependencies
- Upgraded mypy development dependency to version `0.600` and fixed some new
  related minor complaints


v1.1.0
------

New features
^^^^^^^^^^^^

- Added new utility functions `conllu.parse()` and `conllu.to_conllu()` for
  easy *CoNLL-U* objects/string transformations


v1.0.0
------

First public release.
