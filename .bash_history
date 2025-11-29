cd /root
ls
python -m mTree.run config/rps_config.json
mTree_runner config/rps_config.json
exit
cd /root
ls
mTree_runner config/rps_config.json
exit
cd /root
python run_experiment.py
python -c "import mTree; print(dir(mTree))"
find /mtree -name "*.py" | grep -i simulation | head -20
python -c "from mTree.simulation import *; print(dir())"
cat /mtree/mTree/simulation/__init__.py
cat /opt/conda/bin/mTree_runner | head -50
cat /mtree/mTree/runner/runner.py | head -100
ls -la /mtree/mTree/runner/
find /mtree -type f -name "*.json" 2>/dev/null
ls -la /mtree/ | grep -i example
ls -la /auctions/
cd /auctions
ls -la
cat /mtree/mTree/generator/templates/basic_simulation.json
cd /root
mTree_runner config/rps_config.json
exit
cd /root
mTree_runner config/rps_config.json
exit
cd /root
python3 << 'EOF'
import sys
sys.path.insert(0, '/root/mes')
from mTree.microeconomic_system.simulation_container import SimulationContainer
import json
with open('/root/config/rps_config.json') as f:
    config = json.load(f)
print("=" * 60)
print("Starting Rock Paper Scissors simulation...")
print("=" * 60)
container = SimulationContainer(config, '/root')
container = SimulationContainer(config, '/root')

docker run --rm -v "C:/Users/suren/OneDrive - George Mason University - O365 Production/final term project/rock_paper_scissors:/root" -p 5000:5000 -it --entrypoint bash mtree/mtree:1.0.11c
cd /root
exit
cd /root
python3 << 'EOF'
import sys
sys.path.insert(0, '/root/mes')
from mTree.microeconomic_system.simulation_container import SimulationContainer
import json
with open('/root/config/rps_config.json') as f:
    config = json.load(f)
print("=" * 60)
print("Starting Rock Paper Scissors simulation...")
print("=" * 60)
container = SimulationContainer(config, '/root')
container.run()
EOF

python3 -c "from mTree.microeconomic_system.simulation_container import SimulationContainer; import inspect; print(inspect.signature(SimulationContainer.__init__))"
python3 -c "from mTree.microeconomic_system.simulation_container import SimulationContainer; print([m for m in dir(SimulationContainer) if not m.startswith('_')])"
grep -A 10 "SimulationContainer" /mtree/mTree/runner/runner.py
cat > run_sim.py << 'EOF'
import sys
sys.path.insert(0, '/root/mes')

from mTree.microeconomic_system.simulation_container import SimulationContainer
import json

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
container.create_dispatcher()
container.send_dispatcher_simulation_configurations(config)

print("Simulation dispatched! Check browser at http://localhost:5000")
print("Press Ctrl+C to stop")

# Keep running

import time
while True:
    time.sleep(1)
EOF

python3 run_sim.py
cat > run_sim.py << 'EOF'
import sys
sys.path.insert(0, '/root/mes')

from mTree.microeconomic_system.simulation_container import SimulationContainer
import json

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
container.create_dispatcher()
container.send_dispatcher_simulation_configurations([config])

print("Simulation dispatched! Check browser at http://localhost:5000")
print("Press Ctrl+C to stop")

# Keep running

import time
while True:
    time.sleep(1)
EOF

python3 run_sim.py
cat > run_sim.py << 'EOF'
import sys
sys.path.insert(0, '/root/mes')

from mTree.microeconomic_system.simulation_container import SimulationContainer
import json

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

# Add source hash by zipping the source

source_hash = container.zip_source('/root/mes')
config['source_hash'] = source_hash
config['mes_directory'] = '/root'

container.create_dispatcher()
container.send_dispatcher_simulation_configurations([config])

print("Simulation dispatched! Check browser at http://localhost:5000")
print("Press Ctrl+C to stop")

# Keep running

import time
while True:
    time.sleep(1)
EOF

python3 run_sim.py
ls -la /root/mes/
grep -B5 -A10 "zip_source" /mtree/mTree/runner/runner.py
sed -n '100,120p' /mtree/mTree/microeconomic_system/dispatcher.py
cat > run_sim.py << 'EOF'
import sys
sys.path.insert(0, '/root/mes')

from mTree.microeconomic_system.simulation_container import SimulationContainer
import json
import hashlib
import os

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

# Create a simple source hash

config['source_hash'] = hashlib.md5(b'rps_simulation').hexdigest()
config['mes_directory'] = '/root'

container.create_dispatcher()
container.send_dispatcher_simulation_configurations([config])

print("Simulation dispatched! Check browser at http://localhost:5000")
print("Press Ctrl+C to stop")

# Keep running

import time
while True:
    time.sleep(1)
EOF

python3 run_sim.py
cat > run_sim.py << 'EOF'
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
EOF

python3 run_sim.py
exit
cd /root
cat mes/human_agent.py | grep -A20 "__init__"
python3 run_sim.py
exit
mTree
exit
