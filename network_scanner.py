# multi-tool-network-scanner.


# program.python
import subprocess
import shutil
import datetime
import csv

def is_tool_available(tool_name):
    return shutil.which(tool_name) is not None

def save_scan_results(filename, lines):
    with open(filename, 'w') as f:
        timestamp = f"# Scan run at: {datetime.datetime.now()}\n\n"
        f.write(timestamp)
        f.write('\n'.join(lines))
    print(f"\nResults saved to {filename}")

def parse_port_status(lines):
    open_ports = closed_ports = filtered_ports = 0
    for line in lines:
        if "/tcp" in line or "/udp" in line:
            if "open" in line:
                open_ports += 1
            elif "closed" in line:
                closed_ports += 1
            elif "filtered" in line:
                filtered_ports += 1
    print("\nPort Summary:")
    print(f"Open: {open_ports} | Closed: {closed_ports} | Filtered: {filtered_ports}")

def run_nmap(target):
    if not is_tool_available("nmap"):
        print("Nmap is not installed or not in PATH.")
        return

    print("\nNmap Scan Profiles:")
    print("1. Quick Scan")
    print("2. Aggressive Scan")
    print("3. Stealth Mode")
    profile = input("Select profile (1/2/3): ")

    profiles = {
        "1": ["-T4", "-F"],
        "2": ["-A", "-T4"],
        "3": ["-sS", "-Pn"]
    }

    if profile not in profiles:
        print("Invalid profile.")
        return

    print("\nRunning Nmap scan...\n")
    process = subprocess.Popen(["nmap"] + profiles[profile] + [target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        lines = stdout.decode().split('\n')
        for line in lines:
            print(line.strip())
        parse_port_status(lines)

        export = input("\nSave scan results to file? (y/n): ").lower()
        if export == 'y':
            filename = input("Enter filename (e.g., scan.txt): ")
            save_scan_results(filename, lines)
    else:
        print("Nmap error:", stderr.decode())

def run_nslookup(target):
    if not is_tool_available("nslookup"):
        print("nslookup is not available.")
        return
    print("\nRunning nslookup...\n")
    subprocess.run(["nslookup", target])

def run_nikto(target):
    if not is_tool_available("nikto"):
        print("Nikto is not available.")
        return

    print("\nNikto Scan Options:")
    print("1. Default Scan")
    print("2. SSL Scan")
    choice = input("Select Nikto scan version (1/2): ")

    command = ["nikto", "-h", target]
    if choice == "2":
        command.append("-ssl")

    print("\nRunning Nikto scan...\n")
    subprocess.run(command)

def run_qualys(target):
    print("\nSimulated Qualys scan")
    print("This requires external API or CLI integration.")

def run_nessus(target):
    print("\nSimulated Nessus scan")
    print("This requires authenticated access via Nessus CLI or API.")

def main():
    print("\nMulti-Tool Network Scanner")
    print("Choose a tool:")
    print("1. Nmap")
    print("2. Nslookup")
    print("3. Nikto")
    print("4. Qualys (simulated)")
    print("5. Nessus (simulated)")

    tool_choice = input("Your choice (1-5): ")    
    target = input("Enter domain or IP: ")

    if tool_choice == "1":
        run_nmap(target)
    elif tool_choice == "2":
        run_nslookup(target)
    elif tool_choice == "3":
        run_nikto(target)
    elif tool_choice == "4":
        run_qualys(target)
    elif tool_choice == "5":
        run_nessus(target)
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
