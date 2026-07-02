from uds_simulator import send_uds_request, ECUSimulator

def test_read_dtc():
    ecu = ECUSimulator()
    req = send_uds_request("0x19")
    res = ecu.handle_request(req)
    assert res.response_code == "0x59"
    assert len(res.payload["DTCs"]) > 0

def test_clear_dtc():
    ecu = ECUSimulator()
    req = send_uds_request("0x14")
    res = ecu.handle_request(req)
    assert res.response_code == "0x54"
    assert ecu.dtcs == []
