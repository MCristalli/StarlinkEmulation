
import grpc
from grpc_python.spacex.api.device import device_pb2
from grpc_python.spacex.api.device import device_pb2_grpc
from grpc_python.spacex.api.device import command_pb2

import sys

from google.protobuf.json_format import MessageToJson

import os
from protofuzz import protofuzz
import json
import keyboard

TARGET = "192.168.100.1:9200"
CHANNEL = grpc.insecure_channel(TARGET)
STUB = device_pb2_grpc.DeviceStub(CHANNEL)

EnableDebugTelemRequest_string = """
message EnableDebugTelemRequest {
    required uint32 duration_m = 1;
}
"""

PingHostRequest_string = """
message PingHostRequest {
    required string address = 3;
}
"""

SpeedTestRequest_string = """
message SpeedTestRequest {
    required uint32 id = 4;
    required SpeedTestStats client_speedtest = 1;
    required float client_rssi = 2;
    required ClientPlatform client_platform = 3;
}
"""

SetTrustedKeysRequest_string = """
message SetTrustedKeysRequest {
    required repeated PublicKey keys = 1;
}
"""

SetSkuRequest_string = """
message SetSkuRequest {
    required string sku = 1;
    required string country_code = 2;
    required bool apply_country_code = 4;
    required bool pin_country_code = 5;
    required bool custom_power_table = 6;
}
"""

GetLocationRequest_string = """
message GetLocationRequest {
    required PositionSource source = 1;
}
"""

DishSetEmcRequest = """
message DishSetEmcRequest {
    required double theta = 1;
    required double phi = 2;
    required uint32 rx_chan = 3;
    required uint32 tx_chan = 4;
    required uint32 modulation = 5;
    required double desired_tilt_angle = 7;
    required bool chan_override = 8;
    required bool theta_enabled = 9;
    required bool phi_enabled = 10;
    required bool idle = 11;
    required bool fast_switching = 12;
    required bool sky_search = 13;
    required bool force_pll_unlock = 14;
    required bool force_eirp_failure = 15;
    required bool snow_active_override = 16;
    required bool manual_tilting = 18;
    required bool tilt_to_stowed = 19;
    required bool reboot = 20;
    required bool continuous_motor_test = 21;
    required double distance_override_meters = 22;
    required uint32 amplitude_taper_override = 23;
    required uint32 country_code_override = 24;
    required int32 tx_duty_cycle_override = 25;
    required int32 rx_duty_cycle_override = 26;
    required double eirp_legal_limit_dbw_override = 27;
    required double eirp_adjustment_db = 28;
}
"""

ReportClientSpeedtestRequest_string = """
message ReportClientSpeedtestRequest {
    required uint32 id = 1;
    required SpeedTestStats client_speedtest = 2;
    required SpeedTestStats wifi_speedtest = 5;
    required float client_rssi = 3;
    required ClientPlatform client_platform = 4;
}
"""

DishPowerSaveRequest_string = """
message DishPowerSaveRequest {
    required uint32 power_save_start_minutes = 1;
    required uint32 power_save_duration_minutes = 2;
    required bool enable_power_save = 3;
}
"""



def send_EnableDebugTelemRequest():
    with open("fuzz_EnableDebugTelemRequest.json") as fuzz_file:
        data = json.load(fuzz_file)

        for obj in data:
             if len(obj) == 0:
                 continue

             request=device_pb2.Request(
                 id=1,
                 target_id="buffer",
                 epoch_id=1,
                 enable_debug_telem=device_pb2.EnableDebugTelemRequest(duration_m=int(obj["durationM"])),
             )

             try:
                 response = STUB.Handle(request)
                 print(response)
             except grpc.RpcError as e:
                 print(e)
                 #print(e.debug_error_string)
                 #sys.exit(1)

#send_EnableDebugTelemRequest()

def send_PingHostRequest():
    with open("fuzz_PingHostRequest.json") as fuzz_file:
        data = json.load(fuzz_file)

        for obj in data:
             if len(obj) == 0:
                 continue

             request=device_pb2.Request(
                 id=1,
                 target_id="buffer",
                 epoch_id=1,
                 ping_host=device_pb2.PingHostRequest(duration_m=int(obj["address"])),
             )

             try:
                 response = STUB.Handle(request)
                 print(response)
             except grpc.RpcError as e:
                 print(e)
                 #print(e.debug_error_string)
                 #sys.exit(1)


def send_SetSkuRequest():
    with open("fuzz_SetSkuRequest.json") as fuzz_file:
        data = json.load(fuzz_file)

        for obj in data:
             if len(obj) == 0:
                 continue

             request=device_pb2.Request(
                 id=1,
                 target_id="buffer",
                 epoch_id=1,
                 set_sku=device_pb2.SetSkuRequest(
                     sku=obj["sku"],
                     country_code=obj["countryCode"],
                     apply_country_code=obj["applyCountryCode"]=="True",
                     pin_country_code=obj["pinCountryCode"]=="True",
                     custom_power_table=obj["custom_power_table"]=="True",
                 )
             )

             try:
                 response = STUB.Handle(request)
                 print(response)
             except grpc.RpcError as e:
                 print(e)

def send_DishPowerSaveRequest():
    with open("fuzz_DishPowerSaveRequest.json") as fuzz_file:
        data = json.load(fuzz_file)

        for obj in data:
             if len(obj) == 0:
                 continue

             request=device_pb2.Request(
                 id=1,
                 target_id="buffer",
                 epoch_id=1,
                 dish_power_save=device_pb2.DishPowerSaveRequest(
                     power_save_start_minutes = obj["powerSaveStartMinutes"],
                     power_save_duration_minutes = obj["powerSaveDurationMinutes"],
                     enable_power_save = obj["enablePowerSave"],
                 )
             )

             
             print(str(obj["powerSaveStartMinutes"]))
             print(str(obj["powerSaveDurationMinutes"]))
             print(str(obj["enablePowerSave"]))
             try:
                 response = STUB.Handle(request)
                 print(response)
             except grpc.RpcError as e:
                 print(e)

send_DishPowerSaveRequest()

def mutate(file, description_string, message):
    f = open(file, "a")
    f.write("[\n{}\n")

    message_fuzzers = protofuzz.from_description_string(description_string)

    counter = 0

    for obj in message_fuzzers[message].permute():
        #print("Generated object: {}".format(obj))
        f.write(",\n")
        f.write(MessageToJson(obj))

    f.write("]")
    f.close()

#mutate("fuzz_EnableDebugTelemRequest.json", EnableDebugTelemRequest_string, "EnableDebugTelemRequest")
#mutate("fuzz_SetSkuRequest.json", SetSkuRequest_string, "SetSkuRequest")
#mutate("fuzz_DishPowerSaveRequest.json", DishPowerSaveRequest_string, "DishPowerSaveRequest")

def read_fuzz_file():
    with open("fuzz.json") as fuzz_file:
        data = json.load(fuzz_file)

        print("Number of messages read: {}".format(len(data)))
        counter = 79100

        for obj in data:
            if counter % 100 == 0:
                print(str(counter))

            send_json_as_proto(data[counter])
            counter = counter + 1

def send_json_as_proto(message):
    request = device_pb2.Request(
        id=int(message["id"]),
        target_id=message["targetId"],
        epoch_id=int(message["epochId"]),
        get_device_info=device_pb2.GetDeviceInfoRequest(),
    )

    try:
        response = STUB.Handle(request)
        #print(response)
    except grpc.RpcError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    print("start")
    #mutate()
    #read_fuzz_file()

