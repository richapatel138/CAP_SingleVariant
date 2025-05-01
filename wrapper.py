import configparser
import subprocess
import os
import argparse

# Set up argument parser to take config_path as an input flag
parser = argparse.ArgumentParser(description="Run R script with a config file")
parser.add_argument(
    '--config', 
    type=str, 
    help='Path to the config file'
)

# Parse the command-line arguments
args = parser.parse_args()

# Load the provided config file
config = configparser.ConfigParser()
config.read(args.config)
params = config['default']

# Start constructing the Rscript command
r_command = ["Rscript", "SVA.R"]

# Conditionally add 'process' only if it is not empty
if 'process' in params and params['process'].strip():
    r_command.extend(["--process", params['process']])

# Conditionally add 'genes' (this is required, so it's always included)
r_command.extend(["--genes", params['genes']])

# Conditionally add 'seqIDdir' only if it is not empty
if 'seqIDdir' in params and params['seqIDdir'].strip():
    r_command.extend(["--seqIDdir", params['seqIDdir']])

# Conditionally add 'pQTLdir' only if it is not empty
if 'pQTLdir' in params and params['pQTLdir'].strip():
    r_command.extend(["--pQTLdir", params['pQTLdir']])

# Conditionally add 'eQTLdir' only if it is not empty
if 'eQTLdir' in params and params['eQTLdir'].strip():
    r_command.extend(["--eQTLdir", params['eQTLdir']])

# Conditionally add 'ID_input' only if it is not empty
if 'ID_input' in params and params['ID_input'].strip():
    r_command.extend(["--ID_input", params['ID_input']])

# Add other parameters
r_command.extend([
    "--GWASdir", params['GWASdir'],
    "--CHR_input", params['CHR_input'],
    "--BP_input", params['BP_input'],
    "--A1_input", params['A1_input'],
    "--A2_input", params['A2_input'],
    "--BETA_input", params['BETA_input'],
    "--SE_input", params['SE_input'],
    "--outputdir", params['outputdir']
])

# Create output log file path
log_file_path = os.path.join(os.getcwd(), 'SVA.log')

# Run the R script and log stdout/stderr
with open(log_file_path, 'w') as log_file:
    try:
        subprocess.run(r_command, check=True, stdout=log_file, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"Error running R script. Check the log file at {log_file_path} for details.")
