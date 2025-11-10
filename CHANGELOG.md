# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

The following items are marked as pending tasks and will be part of the next major release.

### Added

- Start v1.2.0.dev line.

### Fixed

- **[Persistent]** Set 'PYOPENGL_PLATFORM=glx' if executing swc-render on Wayland in X11 Linux environment to avoid 'no valid context' error.
- **[Persistent]** Run gdk-pixbuf-register to enable Matplotlib backends in swc-view.

### Planned

- Improve test coverage.
- Re-enable flake8 lint testing.
- Revise documentation for consitency.
- Refactor code to address SonarQube findings.
- Do not interpolate diameter if the parent is root (render, measure, repair, morph).

### Changed

- Major code refactoring (view, morph, check, measure).
- Medium code refactoring.
- Minor code refactoring.

### Removed

- Replace TODO file with CHANGELOG.md.


## 1.1.2 - 2025-11-06

### Added

- Add quit option to swc-render.
- Use tox to test against several python versions and OS platforms.
- Run CLI tests in the same process as pytest "coverage run -m pytest tests/".

### Fixed

- Avoid wildcard import in swc-render.

### Changed

- Replace legacy setup.py bdist_wheel mechanism with pyproject.toml.


## 1.1.1 - 2025-10-21

### Fixed

- TypeError in swc-render (W, write image to file).
- Wrong values of segment order "-a seg", limited to 1 and 2 in swc-measure.

### Removed

- Distance to object setting "-d" in swc-view (ignored since 'ortho' projection is used).

### Changed

- Swap 2 nodes at a time in swc-modify.


## 1.1.0 - 2023-08-19

### Added

- Add script scripts/swc2pts.py.
- Add segment data option "-a seg" in swc-measure (get_segdata in morph.py) and remove experimental swc-meter.
- Make distance "-a dist" a standard feature in swc-measure.
- Add optional features "-a {sholl,dist,path,sec}" in swc-measure.
- Add dendrogram view, axes limits and color options in swc-view.
- Add extended segment data extraction in swc-measure (two-pass parsing by get_segdata).
- Add "--seed" for reproducible results in swc-repair.
- Add distance to origin in swc-find.

### Fixed

- Detect soma nodes (type 1) separated by other nodes in swc-check.
- Centering option "-n" was not applied after shrinkage correction in swc-repair.

### Changed

- Rewrite swc-measure for parallel execution (see experimental swc-meter).
- Change distance-to-origin to distance-to-root in swc-find.
- Scaling with positive factors only in swc-modify.
- Add flip option "-f {x,y,z}", flip around root, not origin in swc-repair.
- Add neurite to root if id=1 is in the list of the cut points in swc-repair (i.e., *repair* root).
- Return original root coordinates unless "-n" is explicitly applied in swc-repair.


## 1.0.0 - 2021-06-01

### Added

- First release since initial commit 2020-08-07.
