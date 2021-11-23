# Description: Launches virtual environment to test speakers
# Usage: . ~/testSensors/speaker/env-speaker/bin/activate

printf "Launching test speaker environment\n"

. ~/testSensors/speaker/env-speaker/bin/activate

printf "Virtual environment launched for the following directory: "
pwd

printf "Python version = "
python --version