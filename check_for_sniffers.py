import os
import shutil
import psutil
import logging

# Logging configuration
logging.basicConfig(filename='/var/log/check_sniffers.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to log events
def log_event(event):
    logging.info(event)

# Function to check if any network interface is in promiscuous mode
def check_promiscuous_mode():
    interfaces = os.popen("ip link show").read()
    promiscuous_interfaces = []

    lines = interfaces.splitlines()
    for line in lines:
        if "PROMISC" in line:
            parts = line.split(':')
            if len(parts) > 1:
                interface_name = parts[1].strip()
                promiscuous_interfaces.append(interface_name)

    return promiscuous_interfaces

# Function to check if packet capture tools are installed
def check_installed_tools(tools):
    installed_tools = []
    for tool in tools:
        if shutil.which(tool):
            installed_tools.append(tool)
    return installed_tools

# Function to check if packet capture tools are running
def check_running_processes(tools):
    running_tools = []
    for proc in psutil.process_iter(['pid', 'name']):
        for tool in tools:
            if tool in proc.info['name']:
                running_tools.append(tool)
    return running_tools

# Function to remove installed packet capture tools
def remove_tools(tools):
    for tool in tools:
        os.system(f"sudo apt-get remove -y {tool}")

# Check for promiscuous mode
promiscuous_interfaces = check_promiscuous_mode()
if promiscuous_interfaces:
    promiscuous_interfaces_string = ', '.join(promiscuous_interfaces)
    log_event(f"Interfaces in promiscuous mode: {promiscuous_interfaces_string}")
else:
    log_event("No network interface is in promiscuous mode.")

# Check for installed packet capture tools
tools = ["tcpdump", "wireshark", "tshark", "ethereal"]
installed_tools = check_installed_tools(tools)

if installed_tools:
    log_event(f"Installed tools: {', '.join(installed_tools)}")

# Check for running packet capture tools
running_tools = check_running_processes(tools)

if running_tools:
    log_event(f"Running tools: {', '.join(running_tools)}")

# Remove installed packet capture tools
if installed_tools:
    remove_tools(installed_tools)

log_event("Verification complete.")
