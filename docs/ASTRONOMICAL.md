# AstronomicAL integration

How the astro-science research portfolio is exposed through a local
[AstronomicAL](https://github.com/grant-m-s/AstronomicAL) instance, how that
instance was installed, and how to keep it working.

- AstronomicAL checkout: `/home/dawe/tools/AstronomicAL` (git repo — leave uncommitted)
- Python environment: `/home/dawe/tools/AstronomicAL/.venv` (Python 3.12.15, uv 0.13.1)
- Portfolio plugin: `~/.astronomical/plugins/astro_science_portfolio/`
- Research workspace (read-only for the plugin): `/home/dawe/Projects/astro-science`

---

## 1. What AstronomicAL is

AstronomicAL is a local, human-in-the-loop workspace for exploring, labelling,
integrating and modelling scientific data. It is built on Panel/Bokeh and is a
**plugin host**: the core provides a shared runtime (`datasets`, `selection`,
`artifacts`, `events`, `jobs`, `services`, `workspace`) and almost all visible
functionality — catalogue browsing, plotting, spectra, ML, annotation — is
contributed by plugins.

A plugin is a directory with a `plugin.py` that exposes a `PluginManifest` and a
`register(api)` function. `register` declares panels, actions, services,
artifact viewers and workflows. Panels are Panel components returned by a
factory `factory(context, **kwargs) -> (view, controller)`.

The practical consequence for this project: the research portfolio is packaged
as one self-contained plugin instead of patching AstronomicAL, so the upstream
checkout stays clean and the plugin can be copied to another machine.

---

## 2. Environment used

The upstream `requirements-core.txt` pins `numpy>=1.26,<2`. This instance
deliberately runs a NumPy 2 stack, installed with uv:

```bash
cd /home/dawe/tools/AstronomicAL
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python \
    -r requirements-core.txt -r requirements-astro.txt -r requirements-ml.txt

# deliberate deviations from the pins
uv pip uninstall --python .venv/bin/python sparclclient
uv pip install --python .venv/bin/python "numpy==2.5.4" "pandas==3.0.6" "pyarrow==26.0.0"
```

Resulting versions (verified with `importlib.metadata`):

| Package | Version |
| --- | --- |
| panel | 1.9.4 |
| bokeh | 3.9.2 |
| param | 2.4.2 |
| holoviews | 1.23.2 |
| pandas | 3.0.6 |
| numpy | 2.5.4 |
| pyarrow | 26.0.0 |
| astropy | 8.0.2 |
| numba | 0.68.0 |
| datashader | 0.19.1 |
| scikit-learn | 1.9.1 |
| duckdb | 1.5.6 |

`numba`, `datashader`, `holoviews` and `duckdb` all import cleanly against
NumPy 2.5.4.

### Why the deviation

- **pandas 3 / NumPy 2 / pyarrow 26.** The portfolio CSVs are read with modern
  pandas (`read_csv`, nullable/string dtypes). pandas 3 and pyarrow 26 are built
  against the NumPy 2 C ABI; keeping `numpy<2` would force pandas 2.x and older
  pyarrow wheels, and mixing a NumPy 1 build with NumPy 2 extensions is the
  classic source of `numpy.dtype size changed` crashes. One consistent ABI is
  safer than a mixed environment.
- **sparclclient removed.** It is only needed by the bundled `astro.spectra`
  plugin for SDSS/SciServer spectral queries and drags in constraints that
  conflict with the NumPy 2 stack. Removing it keeps the core stable at the cost
  of that one plugin. In the server log this appears as:

  ```text
  [plugins] failed to enable astro.spectra: Missing dependency: sparclclient
  ```

  This is expected. Install `sparclclient` in a separate environment if you need
  SDSS spectra.
- **Plotly is intentionally not installed.** The figure panel embeds the
  pre-rendered Plotly HTML files produced by the research pipeline; no Python
  Plotly runtime is needed inside AstronomicAL.

Do **not** run `pip install -r requirements-core.txt` again inside this venv: it
would downgrade NumPy to 1.x and break the pandas/pyarrow wheels.

---

## 3. Launch

```bash
cd /home/dawe/tools/AstronomicAL
.venv/bin/python -m panel serve astronomicAL \
    --port 5104 --address 127.0.0.1
```

Open <http://127.0.0.1:5104/astronomicAL>. The app is served under
`/astronomicAL` (the directory being served is the package).

When accessing through a proxy or a non-default origin, add:

```bash
--allow-websocket-origin=127.0.0.1:5104
```

The panels are opened from the workspace panel menu / plugin manager under the
category **Astro Science**.

---

## 4. The plugin

Location:

```text
~/.astronomical/plugins/astro_science_portfolio/
├── plugin.py                  # PluginManifest + register(api)
├── panels.py                  # five panel factories + dataset registry
├── theme.py                   # dark CSS (scoped under .asp-*)
├── astronomical-plugin.json   # static manifest required by user plugin roots
└── README.md
```

Manifest:

```text
id           astro.science.portfolio
name         Astro Science Portfolio
version      0.1.0
capabilities ["panel"]
tags         ["astro", "portfolio", "research"]
```

### Panels

| Panel id | Title | Contents |
| --- | --- | --- |
| `overview` | Portfolio: Overview | Hero header, six metric cards computed from the files at build time (verification snapshot: 12 datasets, 391 GWTC events, 86 AGN masses, 26 notebooks, 21 theory documents, 30 interactive HTML figures), research areas, workspace paths |
| `catalogs` | Portfolio: Catalogues | Select over 12 catalogues; `head(500)` Tabulator, row/column counts, column dictionary (dtype, non-null, null %, example), link to the CSV on disk |
| `figures` | Portfolio: Figures | Select + gallery of every premium figure (HTML/GIF/MP4, counted at render time: 43 at integration, 44 while the figure set is being extended); inlined one at a time, never all at once |
| `research` | Portfolio: Research Index | Index of all notebooks (26), premium theory documents (13) and reports (8 at verification; the loop adds refresh reports); Tabulator index + markdown reader (notebooks show a structural summary) |
| `pipeline` | Portfolio: Pipeline | Badges for `refresh-data`, `notebook-health`, `refresh-graphs`, graph-drift signal, timestamps and log link |

Full panel ids are prefixed by the plugin id, e.g.
`astro.science.portfolio.catalogs`.

### Enabling user plugins

`~/.astronomical/plugins` is a **user** root. AstronomicAL treats plugins there
as community code and only enables them when community plugins are enabled and
the id is enabled in `~/.astronomical/plugin-state.json`:

```json
{
  "schema_version": 1,
  "community_plugins_enabled": true,
  "plugins": {
    "astro.science.portfolio": { "enabled": true }
  }
}
```

This file was created for this instance. A user-directory plugin also **must**
ship a static manifest (`astronomical-plugin.json`); without it, discovery
reports a "must provide a static astronomical-plugin.json" error.

### Data and performance

- Nothing is copied: panels read `research/projects/**` and `.opencode/loops/`
  in place.
- `load_dataset()` uses `pn.cache(max_items=4)`, so the 50 000-row Gaia table is
  only read when selected (13 MB CSV, ~0.1 s here).
- Only `head(500)` is sent to the browser for previews; column profiles are
  computed on the full frame.
- HTML figures are inlined via `srcdoc` (so Chrome's `file://` restriction does
  not blank them) up to 12 MB. Larger documents (`wormhole_traversal.html`,
  42 MB; `kerr_ergosphere_precession.html`, 26 MB) fall back to a `file://`
  iframe plus an "Open file" link. Plotly.js is loaded from the CDN, so those
  figures need network access.
- Override the workspace root with `ASTRO_SCIENCE_ROOT=/path/to/checkout`.

---

## 5. Adding a dataset

Edit `DATASETS` in `~/.astronomical/plugins/astro_science_portfolio/panels.py`:

```python
{
    "key": "my_catalogue",
    "label": "My catalogue",
    "rows": 1234,                       # expected row count (warning badge if it drifts)
    "path": EXTERNAL / "my_catalogue.csv",
    "note": "Provenance in one line",
},
```

`PROCESSED`, `RESULTS` and `EXTERNAL` already point at the exotic-compact-objects
project. The catalogue select box, preview, column dictionary and overview
metric update automatically; no other code change is needed. Because the count
is read from the file, `expected`/`rows` only drives a drift warning.

Restart the server (or reload the browser session) after editing the plugin.

---

## 6. Verification performed

```text
$ .venv/bin/python -c "from astronomicAL.platform.plugins import PluginManifest"
PluginManifest import OK

$ .venv/bin/python -m panel serve astronomicAL --port 5105 --address 127.0.0.1 \
      --allow-websocket-origin=127.0.0.1:5105
HTTP 200  (http://127.0.0.1:5105/astronomicAL)

[plugins] discovered plugin id=astro.science.portfolio ... origin=user
[plugins] main.py: enabling plugin id=astro.science.portfolio
[plugins] main.py: enabled plugin id=astro.science.portfolio
          panels=['astro.science.portfolio.overview',
                  'astro.science.portfolio.catalogs',
                  'astro.science.portfolio.figures',
                  'astro.science.portfolio.research',
                  'astro.science.portfolio.pipeline']
```

`[plugins] failed to enable astro.science.portfolio` does not occur. All five
factories were also built directly and saved as standalone Panel documents to
catch model/serialization errors (overview, catalogues, research, pipeline, and
figures with both an HTML and a GIF selection).

---

## 7. Troubleshooting

### `Missing dependency: sparclclient` (astro.spectra)

Expected — see the deviation above. Nothing else is affected. If SDSS spectra
are required, create a second venv with `numpy<2` + `sparclclient` and run that
copy of AstronomicAL for spectral work.

### pyarrow / NumPy ABI errors

Symptoms:

```text
ImportError: numpy.core.multiarray failed to import
ValueError: numpy.dtype size changed, may indicate binary incompatibility
pyarrow.lib.ArrowInvalid  (while reading a CSV/Parquet)
```

Cause: a wheel compiled against NumPy 1.x in a NumPy 2 environment (or the
reverse). Reinstall the pair together so both match:

```bash
cd /home/dawe/tools/AstronomicAL
uv pip install --python .venv/bin/python --reinstall \
    "numpy==2.5.4" "pyarrow==26.0.0" "pandas==3.0.6"
```

Check with:

```bash
.venv/bin/python -c "import numpy, pyarrow, pandas; print(numpy.__version__, pyarrow.__version__, pandas.__version__)"
```

### Community plugin not listed / not enabled

1. Does the directory contain both `plugin.py` and `astronomical-plugin.json`?
2. Does `~/.astronomical/plugin-state.json` set
   `"community_plugins_enabled": true` and
   `"plugins": {"astro.science.portfolio": {"enabled": true}}`?
3. Start with `ASTRONOMICAL_DEBUG_BOOT=1` and look for
   `discovered plugin id=astro.science.portfolio` and `[plugins] discovery errors`.

### `403` / websocket refused

Panel serves the websocket from the same host/port. If you changed the port or
use a proxy, pass the matching `--allow-websocket-origin=host:port`.

### Figure panel is blank

- Plotly figures fetch `plotly.js` from `cdn.plot.ly`; without network they stay
  blank. Hover shows the iframe but no chart.
- Figures over 12 MB are not inlined. Use the "Open file ↗" link (or open the
  HTML directly in a browser).
- Browsers block `file://` subresources from `http://` pages; that is why inline
  embedding is the default.

### Catalogue shows an "expected N" badge

The CSV on disk no longer matches the `rows` value in the registry. Update it;
this is a drift indicator, not an error.

### Port already in use

```bash
ss -ltnp | grep 5104
# then stop that process, or serve on another port
```

## 7. Using the plugin in a workspace

The five panels are registered under category **Astro Science** and appear in
the platform's *Add Panel* catalogue. To build a working workspace:

1. Launch AstronomicAL (section 4).
2. Open the workspace, choose **Add Panel** and add, in order:
   `Astro Science Portfolio: Overview`, `Catalogs`, `Figures`, `Research`,
   `Pipeline`.
3. Use the *Catalogs* panel to load any of the 12 bundled CSVs into the
   platform dataset store; the *Figures* panel then renders the matching Plotly
   document (HTML inlined, large files via `file://`).
4. Save the workspace as a layout JSON in `~/tools/AstronomicAL/layouts/` so the
   arrangement survives a restart (the bundled layout files in that directory
   are the schema reference).

Panels are read-only with respect to the research data: they never write into
`/home/dawe/Projects/astro-science`.

## 8. Extending

To add a dataset, edit the `DATASETS` list in `panels.py` (label, relative path,
category, description, source) and restart. Counts are computed at panel build
time, so they cannot go stale. To add a panel, register it in `plugin.py` and
implement a factory in `panels.py` following the existing ones.
