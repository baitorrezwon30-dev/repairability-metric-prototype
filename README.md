# Repairability Metric Prototype

This project provides a Python prototype for calculating
a **Repairability score (0–100)** for a software codebase.

## Metric Description
Repairability reflects how easily a codebase can be modified
without causing cascading changes. The metric emphasizes:
- Low coupling
- High cohesion
- Modular design

## Methodology
- Static analysis using Python AST
- Function length and dependency analysis
- AI-assisted repairability evaluation (stubbed)

## Usage

```bash
python repairability.py path/to/codebase
