"""
UDS Diagnostics Simulator
-------------------------

This script simulates basic UDS (Unified Diagnostic Services) behavior:
- Diagnostic Session Control (0x10)
- Read DTC Information (0x19)
- Clear Diagnostic Information (0x14)

Inspired by the DST/DMT diagnostic testing workflows I performed at Bosch.
"""

import json
from typing import Dict, List, Optional


# -----------------------------
# Simple DTC "database"
# -----------------------------

DTC_DB = {
    "P0300": "Random/Multiple Cylinder Misfire Detected",
    "P0420": "Catalyst System Efficiency Below Threshold (Bank 1)",
    "P0113": "Intake Air Temperature Sensor 1 Circuit High",
}


# -----------------------------
# UDS Request / Response Models
# -----------------------------

class UDSRequest:
    def __init__(self, service_id: str, sub_function: Optional[str] = None):
        self.service_id = service_id
        self.sub_function = sub_function

    def __repr__(self):
        return f"UDSRequest(SID={self.service_id}, SF={self.sub_function})"


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
    """
    A simple ECU simulator that handles a subset of UDS services.
    """

    def __init__(self):
        self.current_session = "Default"
        self.dtcs: List[str] = list(DTC_DB.keys())  # ECU currently has these DTCs

    def handle_request(self, request: UDSRequest) -> UDSResponse:
        sid = request.service_id

        if sid == "0x10":  # Diagnostic Session Control
            return self._handle_session_control(request)

        if sid == "0x19":  # Read DTC Information
            return self._handle_read_dtc(request)

        if sid == "0x14":  # Clear Diagnostic Information
            return self._handle_clear_dtc(request)

        # Service not supported
        return UDSResponse("0x7F", {"Error": "Service Not Supported"})

    def _handle_session_control(self, request: UDSRequest) -> UDSResponse:
        self.current_session = "Extended"
        return UDSResponse("0x50", {"Message": "Session changed to Extended"})

    def _handle_read_dtc(self, request: UDSRequest) -> UDSResponse:
        if not self.dtcs:
            return UDSResponse("0x59", {"DTCs": [], "Message": "No DTCs stored"})

        return UDSResponse("0x59", {"DTCs": self.dtcs})

    def _handle_clear_dtc(self, request: UDSRequest) -> UDSResponse:
        self.dtcs.clear()
        return UDSResponse("0x54", {"Message": "All DTCs cleared"})


# -----------------------------
# Helper Functions
# -----------------------------

def send_uds_request(service_id: str, sub_function: Optional[str] = None) -> UDSRequest:
    req = UDSRequest(service_id, sub_function)
    print(f"[TX] Sending UDS Request: {req}")
    return req


def print_response(res: UDSResponse):
    print(f"[RX] ECU Response: {res}")
    print(f"      Payload: {json.dumps(res.payload, indent=6)}")


# -----------------------------
# Demo Flow (Main)
# -----------------------------

def demo_flow():
    ecu = ECUSimulator()

    print("\n--- UDS Diagnostics Demo Flow ---\n")

    # 1. Switch diagnostic session
    req_session = send_uds_request("0x10", "0x03")
    res_session = ecu.handle_request(req_session)
    print_response(res_session)

    # 2. Read DTCs
    req_read_dtc = send_uds_request("0x19", "0x02")
    res_read_dtc = ecu.handle_request(req_read_dtc)
    print_response(res_read_dtc)

    # 3. Clear DTCs
    req_clear_dtc = send_uds_request("0x14", "0xFF")
    res_clear_dtc = ecu.handle_request(req_clear_dtc)
    print_response(res_clear_dtc)

    # 4. Read DTCs again
    req_read_dtc2 = send_uds_request("0x19", "0x02")
    res_read_dtc2 = ecu.handle_request(req_read_dtc2)
    print_response(res_read_dtc2)

    # 5. Unsupported service
    req_unsupported = send_uds_request("0x22")
    res_unsupported = ecu.handle_request(req_unsupported)
    print_response(res_unsupported)


if __name__ == "__main__":
    demo_flow()
