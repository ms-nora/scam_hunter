# scam_hunter
This script is a **forensic monitoring tool** designed to detect and log AnyDesk connections on the local system, providing evidence for investigations. It operates as follows:

### **Script Functionality**
1. **Process Monitoring**  
   - Continuously checks if the **AnyDesk process** is running.  
   - Once AnyDesk is detected, it starts logging forensic data.

2. **Network Monitoring**  
   - Captures the **active network ports used by AnyDesk** dynamically.  
   - Monitors **all established network connections** to detect a remote IP.  
   - Logs **all network traffic** using `tcpdump` for forensic analysis.

3. **Forensic Evidence Collection**  
   - **Logs network connections**: Captures all active network communication.  
   - **Logs running processes**: Saves a snapshot of all active processes on the system.  
   - **Captures a screenshot**: Takes a full-screen snapshot when a scammer is connected.  
   - **Captures a webcam image** (if available): Attempts to photograph the scammer using the default camera.

4. **Data Integrity & Security**  
   - **SHA-256 hash verification**: Ensures log file integrity by generating and storing a hash.  
   - **Forensic logging**: Saves all collected data in a structured format for later analysis.  

5. **Automated Packet Capture**  
   - Starts a **network traffic capture** when AnyDesk runs.  
   - Logs all **packets related to AnyDesk activity** into a PCAP file.  
   - Stops packet capture when the scammer disconnects.

6. **Automatic Detection & Response**  
   - The script continuously monitors AnyDesk activity.  
   - It only starts forensic data collection when a **connection is actively established**.  
   - It stops logging once the connection is terminated.

This script is designed for **law enforcement and forensic investigations** to track and document scam-related AnyDesk sessions while maintaining **data integrity and legal compliance**.

## License
This project is licensed under the **MIT Research-Only License**.

**Allowed Uses:**
- Academic research
- Law enforcement investigations
- Forensic analysis

**Restrictions:**
- No commercial use without permission
- No use for unauthorized surveillance, cybercrime, or malicious intent

See the [LICENSE](LICENSE) file for details.
