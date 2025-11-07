## [Unreleased]

### Added

- Add **quit option** to `swc-render`.
- Improve coverage and add tests for new code in **treem (tests)**.

### Changed

- Refactor code in **treem** to comply with SonarQube quality requirements.
- Re-enable flake8 lint testing in **treem (build)**.
- In **treem (render, measure, repair, morph)**, do not interpolate diameter if the parent is root.

### Removed

- Replace **TODO** file with **CHANGELOG.md**, following the keepachangelog.com format.
- Avoid wildcard import in `swc-render`.

## [1.1.2] - YYYY-MM-DD (Estimate based on TODO)

### Added

- Add **Arabic translation** to v1.1 (#444) [This item is already in your existing CHANGELOG.md for v1.1.1, but included here for completeness if you intended it for 1.1.2].
- Add **dendrogram view** to `swc-view`.
- Add **axes limits** to `swc-view`.
- Add **segment data option** (`-a seg`) to `swc-measure` (see `morph.py:get_segdata()`), and remove experimental `swc-meter`.
- Add script `scripts/swc2pts.py` to **treem**.
- Centralize all links into `/data/links.json` so they can be updated easily [This item is already in your existing CHANGELOG.md for v1.1.1, but included here for completeness if you intended it for 1.1.2].

### Fixed

- `swc-check`: Detect soma nodes (type 1) separated by other nodes (see Ilaria's `210525_s6_v4.swc`).
- `swc-repair`: Correctly apply centering option (`-n`) after shrinkage correction.
- `swc-view`: Ignore distance to object setting (`-d`) if 'ortho' projection is used (default).
- `swc-measure`: Wrong values of **segment order** (`-a seg`) limited to 1 and 2.
- **Attention**: `swc-view`: Need to run `gdk-pixbuf-register` to enable matplotlib backends.
- **Attention**: `swc-render`: 'no valid context' error in wayland, set `PYOPENGL_PLATFORM='glx'`.
- `swc-render (W, write image to file)`: Fixed `TypeError`.

### Changed

- `swc-repair`: Change distance-to-origin to **distance-to-root**.
- `swc-measure (Node.dist)`: Evaluate distance to root, not origin.
- `swc-modify`: Update scaling to allow **positive factors only**.
- `swc-repair`: Flip option (`-f {x,y,z}`) should **flip around root, not origin**.
- `swc-repair`: Add neurite to root if `id=1` is in the list of the cut points.
- `swc-modify`: Swap **2 nodes at a time**, randomly selected from the input list.

### Removed

- None explicitly marked as removed in the TODO list that weren't future tasks.
