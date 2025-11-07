# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

The following items are marked as pending tasks and will be part of the next major release, likely v1.2.0.

### Added

- treem: Start `v1.2.0.dev` line.

### Fixed

- Attention: `swc-render`: 'no valid context' error in wayland; set `PYOPENGL_PLATFORM='glx'`.
- Attention: `swc-view`: Run `gdk-pixbuf-register` to enable matplotlib backends.

### Changed

- treem (build): Re-enable flake8 lint testing.
- treem (tests): Improve coverage and add tests for new code.
- treem (render, measure, repair, morph): Do not interpolate diameter if the parent is root.
- treem: Refactor code to comply with SonarQube quality requirements.

### Removed

- treem: Replace TODO file with `CHANGELOG.md`.

---

## [1.1.2] - 2025-11-06

### Added

- `swc-render`: Add quit option.
- `treem`: Use tox to test against several python versions and OS platforms.
- `treem` (tests): Run CLI tests in the same process as `pytest` (`coverage run -m pytest tests/`).

### Fixed

- `swc-render`: Avoid wildcard import.

### Changed

- `treem`: Replace legacy `setup.py` bdist_wheel mechanism with `pyproject.toml`.

---

## [1.1.1] - 2025-10-21

### Fixed

- `swc-render` (W, write image to file): Fixed `TypeError`.
- `swc-measure`: Fixed wrong values of segment order (`-a seg`) limited to 1 and 2.
- `swc-view`: Fixed: distance to object setting (`-d`) is ignored if 'ortho' projection is used (default).

### Changed

- `swc-modify`: Swap 2 nodes at a time, randomly selected from the input list.

---

## [1.1.0] - 2023-08-19

### Added

- `treem`: Add script `scripts/swc2pts.py`.
- `swc-measure`: Add segment data option (`-a seg`) (see `morph.py:get_segdata()`) and remove experimental `swc-meter`.
- `swc-measure`: Make distance (`-a dist`) a standard feature.
- `swc-measure`: Add optional features (`-a {sholl,dist,path,sec}`).
- `swc-view`: Add dendrogram view.
- `swc-view`: Add axes limits.
- `swc-view`: Add color options.
- `morph` (`get_segdata`): Extract extended segment data (two-pass parsing).
- `swc-repair`: Add `--seed` for reproducible results.
- `swc-find`: Distance to origin.

### Fixed

- `swc-check`: Detect soma nodes (type 1) separated by other nodes.
- `swc-repair`: Fixed: centering option (`-n`) not applied after shrinkage correction.

### Changed

- `swc-measure`: Rewrite for parallel execution (see experimental `swc-meter`).
- `swc-find`: Change distance-to-origin to distance-to-root.
- `swc-measure` (`Node.dist`): Evaluate distance to root, not origin.
- `swc-modify`: Scaling with positive factors only.
- `swc-repair`: Add flip option (`-f {x,y,z}`); flip around root, not origin.
- `swc-repair`: Add neurite to root if `id=1` is in the list of the cut points.
- `swc-repair`: Assumes centered input morphology; should do this internally if needed and return original root coordinates unless `-n` explicitly applied.

---

## [1.0.0] - 2021-06-01

### Added

- `treem`: First release since initial commit 2020-08-07.
