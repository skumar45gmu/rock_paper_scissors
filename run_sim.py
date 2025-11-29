import sys
sys.path.insert(0, '/root/mes')

from mTree.microeconomic_system.simulation_container import SimulationContainer
import json
import hashlib
import uuid

# Load config
with open('/root/config/rps_config.json') as f:
    config = json.load(f)

print("=" * 60)
print("Starting Rock Paper Scissors simulation...")
print("=" * 60)
print(f"Config: {config['name']}")
print("=" * 60)

# Create container and run
container = SimulationContainer()

# Add required fields
config['source_hash'] = hashlib.md5(b'rps_simulation').hexdigest()
config['mes_directory'] = '/root'
config['simulation_run_id'] = str(uuid.uuid4())

container.create_dispatcher()
container.send_dispatcher_simulation_configurations([config])

print("Simulation dispatched! Check browser at http://localhost:5000")
print(f"Run ID: {config['simulation_run_id']}")
print("Press Ctrl+C to stop")

# Keep running
import time
while True:
    time.sleep(1)
