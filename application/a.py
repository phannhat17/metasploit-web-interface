from pymetasploit3.msfrpc import MsfRpcClient
import time
import itertools

# Initialize the MSF RPC Client with your password
password = 'WVDukaKdCW8veqQfavB1'  # Replace 'yourpassword' with the actual MSFRPC password
client = MsfRpcClient(password, port=55553, ssl=True)

# Check database status
console = client.consoles.console()
console.write('workspace')
time.sleep(1)  # Give it some time to respond
db_status = console.read()['data']
print("Database status:", db_status.strip())

# Define the target for nmap
nmap_targets = '192.168.204.138'
print("Starting nmap scan on target:", nmap_targets)
console.write(f'db_nmap -sV --script=vulners.nse {nmap_targets}')

# Monitor scan progress with an animation
loading = itertools.cycle(['-', '\\', '|', '/'])  # Loading animation sequence
data = ''
timer = 0
print("Monitoring scan progress...", end="")
while data == '' or console.is_busy():
    time.sleep(1)  # Interval to wait before checking console output
    new_data = console.read()['data']
    if new_data:
        data += new_data
        # Instead of printing each new data, you might just want to print it if it's meaningful, or log it to a file.
    else:
        print(f"\rMonitoring scan progress... {next(loading)}", end="", flush=True)  # Update the animation
    timer += 1
    if timer > 300:  # Timeout to prevent infinite loop
        print("\nScan timed out")
        break
print("\nScan completed.")

# Fetch and print vulnerabilities found after scan
console.write('vulns')
time.sleep(2)  # Wait for the command to complete
vulns_data = console.read()['data']
if vulns_data:
    print("Vulnerabilities found:\n", vulns_data.strip())
else:
    print("No vulnerabilities found.")

console.destroy()
