import subprocess
import datetime
import os
import threading
import time
import sys

# Function to execute the nmap command and save its output
def execute_nmap(command, filename):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    with open(filename, 'w') as file:
        file.write(result.stdout)
    print("\nScan complete. Results saved.")

# Function to display a simple progress indicator
def display_progress():
    print("Scanning", end="", flush=True)
    while not nmap_done.is_set():
        time.sleep(1)  # Continue to sleep while nmap runs
    print("\rScanning...done          ") 

# Function to run the nmap scan
def run_nmap_scan(target_ip):
    directory = "../scan_results"
    os.makedirs(directory, exist_ok=True)

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{directory}/{timestamp}_res_{target_ip.replace('.', '_')}.txt"
    command = f"nmap -sV --script vulners.nse {target_ip}"

    # Create a threading event to signawhen the nmap scan is done
    global nmap_done
    nmap_done = threading.Event()

    # Thread to run the nmap scan
    nmap_thread = threading.Thread(target=execute_nmap, args=(command, filename))
    
    # Start the nmap scan thread
    nmap_thread.start()

    # Display progress while the nmap scan runs
    display_progress_thread = threading.Thread(target=display_progress)
    display_progress_thread.start()

    nmap_thread.join()
    nmap_done.set()  
    display_progress_thread.join()
    
    print(f"Scan results saved to {filename}")

target_ip = "192.168.204.138"  
run_nmap_scan(target_ip)
