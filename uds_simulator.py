"""
UDS Diagnostics Simulator (Extended Version)
--------------------------------------------

This simulator now supports:
- 0x10 Diagnostic Session Control
- 0x19 Read DTC Information
- 0x14 Clear DTC Information
- 0x22 Read Data By Identifier (DID)
- 0x2E Write Data By Identifier
- 0x27 Security Access (simple unlock simulation)

Inspired by DST/DMT diagnostic testing workflows performed at Bosch.
"""

import json
from typing import Dict, List, Optional


# -----------------------------
# Load DTC database
# -----------------------------

with open("dtc_database.json", "r") as f:
    DTC_DB = json.load(f)


# -----------------------------
# DID Database (Read/Write)
# -----------------------------

DID_DB = {
    "F190": "VIN123456789ABCDEFG",
    "F18A": "ECU_SW_VERSION_1.0",
    "F1A0": "ENGINE_SPEED_800_RPM"
}


# -----------------------------
# Security Access
# -----------------------------

SECURITY_SEED = "ABCD"
SECURITY_KEY = "1234"   # simple unlock key


# -----------------------------
# UDS Request / Response Models
# -----------------------------

class UDSRequest:
    def __init__(self, service_id: str, sub_function: Optional[str] = None, data: Optional[str] = None):
        self.service_id = service_id
        self.sub_function = sub_function
        self.data = data

    def __repr__(self):
        return f"UDSRequest(SID={self.service_id}, SF={self.sub_function}, DATA={self.data})"


class UDSResponse:
    def __init__(self, response_code: str, payload: Dict):
        self.response_code = response_code
        self.payload = payload

    def __repr__(self):
        return f"UDSResponse(RC={self.response_code}, Payload={self.payload})"


# -----------------------------
# ECU Simulator
# -----------------------------

class ECUSimulator:
    def __init__(self):
        self.current_session = "Default"
        self.dtcs: List[str] = list(DTC_DB.keys())
        self.security_unlocked = False

    def handle_request(self, request: UDSRequest) -> UDSResponse:
        sid = request.service_id

        if sid == "0x10":
            return self._session_control(request)

        if sid == "0x19":
            return self._read_dtc(request)

        if sid == "0x14":
            return self._clear_dtc(request)

        if sid == "0x22":
            return self._read_did(request)

        if sid == "0x2E":
            return self._write_did(request)

        if sid == "0x27":
            return self._security_access(request)

        return UDSResponse("0x7F", {"Error": "Service Not Supported"})

    # -----------------------------
    # UDS Service Implementations
    # -----------------------------

    def _session_control(self, request: UDSRequest):
        self.current_session = "Extended"
        return UDSResponse("0x50", {"Message": "Session changed to Extended"})

    def _read_dtc(self, request: UDSRequest):
        if not self.dtcs:
            return UDSResponse("0x59", {"DTCs": [], "Message": "No DTCs stored"})
        return UDSResponse("0x59", {"DTCs": self.dtcs})

    def _clear_dtc(self, request: UDSRequest):
        self.dtcs.clear()
        return UDSResponse("0x54", {"Message": "All DTCs cleared"})

    def _read_did(self, request: UDSRequest):
        did = request.data
        if did in DID_DB:
            return UDSResponse("0x62", {"DID": did, "Value": DID_DB[did]})
        return UDSResponse("0x7F", {"Error": "DID Not Found"})

    def _write_did(self, request: UDSRequest):
        if not self.security_unlocked:
            return UDSResponse("0x7F", {"Error": "Security Access Required"})

        did = request.sub_function
        value = request.data
        DID_DB[did] = value
        return UDSResponse("0x6E", {"Message": f"DID {did} updated", "NewValue": value})

    def _security_access(self, request: UDSRequest):
        if request.sub_function == "0x01":  # request seed
            return UDSResponse("0x67", {"Seed": SECURITY_SEED})

        if request.sub_function == "0x02":  # send key
            if request.data == SECURITY_KEY:
                self.security_unlocked = True
                return UDSResponse("0x67", {"Message": "Security Unlocked"})
            return UDSResponse("0x7F", {"Error": "Invalid Key"})

        return UDSResponse("0x7F", {"Error": "Invalid SubFunction"})


# -----------------------------
# Helper Functions
# -----------------------------

def send_uds_request(service_id: str, sub_function=None, data=None):
    req = UDSRequest(service_id, sub_function, data)
    print(f"[TX] {req}")
    return req


def print_response(res: UDSResponse):
    print(f"[RX] {res}")
    print(f"      Payload: {json.dumps(res.payload, indent=6)}")


# -----------------------------
# Demo Flow
# -----------------------------

def demo_flow():
    ecu = ECUSimulator()

    print("\n--- Extended UDS Demo Flow ---\n")

    # Session Control
    print_response(ecu.handle_request(send_uds_request("0x10", "0x03")))

    # Read DTC
    print_response(ecu.handle_request(send_uds_request("0x19")))

    # Read DID
    print_response(ecu.handle_request(send_uds_request("0x22", data="F190")))

    # Security Access
    print_response(ecu.handle_request(send_uds_request("0x27", "0x01")))  # request seed
    print_response(ecu.handle_request(send_uds_request("0x27", "0x02", data="1234")))  # send key

    # Write DID (requires security unlock)
    print_response(ecu.handle_request(send_uds_request("0x2E", "F1A0", data="ENGINE_SPEED_900_RPM")))

    # Clear DTC
    print_response(ecu.handle_request(send_uds_request("0x14")))


if __name__ == "__main__":
    demo_flow()
