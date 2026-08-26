# 🛡️ Advanced Counter-Drone System — Localized Network Monitoring

A defensive research prototype focused on **drone-detection telemetry and local-network monitoring**. The project does not attempt to jam, hijack, disable, or interfere with aircraft or radio communications.

## Objective

Explore how a localized monitoring service could ingest telemetry records, detect suspicious patterns, and generate alerts for human review.

## Current Implementation

The initial implementation provides a lightweight telemetry anomaly detector. It reads structured observations and flags records that cross configurable thresholds.

## Example telemetry

```csv
node_id,signal_strength,packet_rate,altitude
node-01,-42,18,85
node-02,-91,2,120
```

## Run

```bash
python src/anomaly_detector.py --input data/sample_telemetry.csv
```

## Safety Boundary

This repository is limited to **detection, logging, and analysis**. It intentionally excludes signal jamming, spoofing, takeover, weaponization, or instructions for interfering with aircraft.

## Future Work

- Sensor fusion using multiple benign telemetry sources
- Time-series anomaly scoring
- Alert dashboard
- Offline evaluation using labelled telemetry
- Authentication and integrity checks for telemetry messages
