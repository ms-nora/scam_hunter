import psutil
import time
import os
import hashlib
import pyautogui
import subprocess
import cv2

#define secure log file and evidence paths
log_file = os.path.expanduser("~/Desktop/scammer_log.txt")
screenshot_path = os.path.expanduser("~/Desktop/scammer_screenshot.png")
pcap_file = os.path.expanduser("~/Desktop/scammer_traffic.pcap")
photo_path = os.path.expanduser("~/Desktop/scammer_photo.jpg")

def write_secure_log(message):
    #writes a secured log file with sha-256 hashing
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} - {message}\n"

    with open(log_file, "a") as log:
        log.write(entry)

    #update hash of the log file
    with open(log_file, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    with open(log_file + ".hash", "w") as hash_file:
        hash_file.write(file_hash)

def is_anydesk_running():
    #checks if anydesk process is running
    for proc in psutil.process_iter(['name']):
        if "anydesk" in proc.info['name'].lower():
            return True
    return False

def get_anydesk_connections():
    #checks for active anydesk connections based on processes and ports
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        if "anydesk" in proc.info['name'].lower():
            for conn in proc.info['connections']:
                if conn.status == "ESTABLISHED" and conn.raddr:
                    return conn.raddr.ip  #scammer's external ip
    return None

def log_anydesk_ports():
    #logs all active ports used by anydesk
    ports = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr and conn.raddr:
            ports.append((conn.laddr.port, conn.raddr.port))

    with open(log_file, "a") as log:
        log.write("anydesk active ports:\n")
        for local, remote in ports:
            log.write(f"  local: {local}, remote: {remote}\n")

def capture_screenshot():
    #captures a screenshot of the screen as evidence
    pyautogui.screenshot(screenshot_path)
    write_secure_log(f"screenshot saved: {screenshot_path}")

def capture_webcam_image():
    #captures an image from the webcam if available
    cam = cv2.VideoCapture(0)  #use the first available camera
    if not cam.isOpened():
        write_secure_log("no active camera detected")
        return
    
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(photo_path, frame)
        write_secure_log(f"photo captured: {photo_path}")
    else:
        write_secure_log("camera access failed")
    
    cam.release()

def start_packet_capture():
    #starts a network traffic capture for anydesk activity (requires root privileges)
    write_secure_log("starting network traffic capture...")
    subprocess.Popen(["sudo", "tcpdump", "-i", "any", "-w", pcap_file],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_packet_capture():
    #stops the network traffic capture
    subprocess.run(["sudo", "pkill", "tcpdump"])
    write_secure_log(f"network traffic saved: {pcap_file}")

#wait until anydesk is running
while not is_anydesk_running():
    time.sleep(2)

write_secure_log("anydesk process detected, waiting for connection...")
start_packet_capture() #start capturing traffic as soon as anydesk runs
log_anydesk_ports() #log the active ports anydesk is using

#wait for an active anydesk connection
while True:
    scammer_ip = get_anydesk_connections()
    if scammer_ip:
        write_secure_log(f"active anydesk connection detected! scammer ip: {scammer_ip}")
        break
    time.sleep(5)

#collect forensic evidence while scammer is connected
while scammer_ip:
    write_secure_log(f"collecting forensic data for scammer at ip: {scammer_ip}")

    #log active network connections
    connections = psutil.net_connections(kind='inet')
    with open(log_file, "a") as log:
        log.write("network connections:\n")
        for conn in connections:
            log.write(f"  {conn.laddr} -> {conn.raddr} (status: {conn.status})\n")

    #log running processes
    processes = [(p.pid, p.name()) for p in psutil.process_iter(['pid', 'name'])]
    with open(log_file, "a") as log:
        log.write("running processes:\n")
        for pid, name in processes:
            log.write(f"  {pid} - {name}\n")

    #capture screenshot as evidence
    capture_screenshot()

    #capture webcam image
    capture_webcam_image()

    #recheck connection status
    time.sleep(5)
    scammer_ip = get_anydesk_connections()

stop_packet_capture()
write_secure_log("scammer disconnected. forensic logging stopped.")
