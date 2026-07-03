# UDS Diagnostics Simulator (Extended Version)

This project is a Python-based simulation of UDS (Unified Diagnostic Services) communication, inspired by the
DST/DMT diagnostic testing workflows I performed at Bosch. It recreates how an ECU responds to diagnostic
requests such as reading DTCs, switching diagnostic sessions, reading/writing DIDs, and performing security
unlock operations.

The goal of this project is to demonstrate practical understanding of UDS services, ECU behavior, diagnostic
workflows, and automated testing — all in an open-source, beginner-friendly format.

---

## 🔧 Supported UDS Services

This extended version includes the most commonly used UDS services:

### **0x10 – Diagnostic Session Control**
Switches the ECU into Extended Diagnostic Session.

### **0x19 – Read DTC Information**
Reads Diagnostic Trouble Codes stored in the ECU.  
DTCs are loaded from `dtc_database.json`.

### **0x14 – Clear Diagnostic Information**
Clears all stored DTCs.

### **0x22 – Read Data By Identifier (DID)**
Reads ECU parameters such as VIN, software version, or engine speed.

### **0x2E – Write Data By Identifier**
Writes new values to ECU parameters.  
This operation requires **Security Access**.

### **0x27 – Security Access**
Implements a simple seed/key unlock mechanism:
- SubFunction 0x01 → Request Seed  
- SubFunction 0x02 → Send Key  
Once unlocked, protected services (like 0x2E) become available.

---

## 📁 Project Structure

