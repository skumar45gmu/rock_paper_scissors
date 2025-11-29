#!/usr/bin/env python
"""Simple script to run Rock Paper Scissors experiment"""

import sys
import os

# Add the experiment directory to path
sys.path.insert(0, '/root/mes')

# Import mTree components
from mTree.microeconomic_system.simulation_manager import SimulationManager
import json

# Load config
with open('/root/config/rps_config.json', 'r') as f:
    config = json.load(f)

print("=" * 60)
print("ROCK PAPER SCISSORS EXPERIMENT")
print("=" * 60)
print(f"Configuration loaded: {config['experiment_name']}")
print(f"Number of rounds: {config['properties']['num_rounds']}")
print("=" * 60)

# Create and run simulation
try:
    manager = SimulationManager(config)
    manager.run()
except Exception as e:
    print(f"Error running simulation: {e}")
    import traceback
    traceback.print_exc()