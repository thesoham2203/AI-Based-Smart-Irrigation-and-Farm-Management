# Architecture

See high-level diagrams (hardware, processing, interface layers).

## Backend Decision Logic
Current logic: simple threshold rule in `sensors/decision.py`.
Future upgrades: crop stage dependent thresholds, evapotranspiration (ET) model, forecast integration, ML model.

## Offline Behavior
Edge agent counts consecutive dry readings; triggers irrigation when threshold breached repeatedly and backend unreachable.
