# Gravitational-Wave Catalogs

The LIGO/Virgo/KAGRA collaborations publish compact-binary merger events in the
Gravitational-Wave Transient Catalog (GWTC), served through the Gravitational
Wave Open Science Center (GWOSC).

## What the catalog contains

Each event records source-frame component masses $m_1,m_2$, the chirp mass
$\mathcal M_c$, the effective spin $\chi_{\rm eff}$, luminosity distance,
redshift, network matched-filter SNR, and the final (remnant) mass and spin.
The catalog endpoint is a public read-only JSON service; the local workspace
snapshot contains a deduplicated table of 391 events plus a 301-event O4 table.
A catalog event is not a continuously monitored observation, and missing
parameters must not be read as zero.

## The remnant sample

Remnant masses are inferred from the inspiral and ringdown. GW150914, the first
detection, had $m_1=36^{+5}_{-4}M_\odot$, $m_2=29\pm4M_\odot$, a final mass
$M_f=62\pm4M_\odot$, and spin $a_f=0.67^{+0.05}_{-0.07}$, radiating about
$3M_\odot c^2$. GW190521 produced a $\sim142M_\odot$ remnant in the
pair-instability mass gap. The remnant spins cluster at moderate $a_*$, a
constraint on formation channels.

## Using the sample

The events underpin the parameter-estimation forecasts in
[[Fisher Information Matrix]] and the waveform analysis in
[[Gravitational Wave Analysis]]. Remnant mass and spin connect to
[[Kerr Metric]], and the most massive remnants to growth models in
[[Early Supermassive Black Hole Growth]].

See also: [[Gravitational Wave Analysis]], [[Fisher Information Matrix]], [[Kerr Metric]], [[Early Supermassive Black Hole Growth]]

Categories: Observations & Catalogs
