import platform
import psutil
import socket
import uuid
import shutil
import os
import requests
import subprocess

def get_os_info():
    print("🖥️ Operating System Info")
    print(f"OS: {platform.system()}")
    print(f"OS Version: {platform.version()}")
    print(f"Release: {platform.release()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print()

def get_memory_info():
    print("🧠 Memory Info")
    mem = psutil.virtual_memory()
    print(f"Total Memory: {mem.total // (1024 ** 3)} GB")
    print(f"Available Memory: {mem.available // (1024 ** 3)} GB")
    print()

def get_disk_info():
    print("💾 Disk Info")
    partitions = psutil.disk_partitions()
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"Drive: {p.device}")
            print(f"  Total: {usage.total // (1024 ** 3)} GB")
            print(f"  Used: {usage.used // (1024 ** 3)} GB")
            print(f"  Free: {usage.free // (1024 ** 3)} GB")
        except PermissionError:
            continue
    print(f"Total Drives: {len(partitions)}")
    print()

def get_network_info():
    print("🌐 Network Info")
    interfaces = psutil.net_if_addrs()
    eth_count = sum(1 for i in interfaces if 'eth' in i)
    wlan_count = sum(1 for i in interfaces if 'wlan' in i)
    print(f"Number of eth interfaces: {eth_count}")
    print(f"Number of wlan interfaces: {wlan_count}")
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                    for ele in range(0,8*6,8)][::-1])
    print(f"MAC Address: {mac}")
    try:
        ip = socket.gethostbyname(socket.gethostname())
        print(f"Host IP: {ip}")
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()
        print(f"ISP: {data.get('org', 'Unknown')}")
        print("Internet: Connected")
    except:
        print("Internet: Not Connected")
    print()

def get_browser_info():
    print("🌐 Browser Info")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_path):
        try:
            version = subprocess.check_output([chrome_path, "--version"]).decode().strip()
            print(f"Chrome Version: {version}")
        except:
            print("Chrome Version: Unable to retrieve")
    else:
        print("Chrome: Not Installed")
    print()

def get_firewall_status():
    print("🛡️ Windows Firewall Status")
    try:
        status = subprocess.check_output("netsh advfirewall show allprofiles", shell=True).decode()
        if "State ON" in status or "State                    ON" in status:
            print("Firewall: Enabled")
        else:
            print("Firewall: Disabled")
    except:
        print("Firewall: Unknown")
    print()

def get_usb_info():
    print("🔌 USB Info")
    try:
        result = subprocess.check_output("wmic path CIM_LogicalDevice where \"Description like 'USB%'\" get /value", shell=True).decode()
        usb_ports = result.count("DeviceID=")
        print(f"USB Ports Detected: {usb_ports}")
    except:
        print("USB Info: Unable to retrieve")
    print()

# Run all functions
get_os_info()
get_memory_info()
get_disk_info()
get_network_info()
get_browser_info()
get_firewall_status()
get_usb_info()
