import subprocess
import json
from src.save import save_json, save_csv

SU = "wlan.vht.mimo_control.feedbacktype == 0x0"
MU = "wlan.vht.mimo_control.feedbacktype == 0x1"
SA = "wlan.sa"
INFO = {}


def set_info(cbr_len, nc, nr, min_antenna):
    key = f"{cbr_len}_{nc}_{nr}_{min_antenna}"
    if key not in INFO.keys():
        INFO[key] = 1
    else:
        INFO[key] += 1


def get_info():
    return INFO.copy()


def get_pinfo(oinfo: dict):
    if len(oinfo.keys()) == 0:
        return {}

    k = oinfo.keys()
    k = list(k)
    k.sort()
    k_tup = [(c, '_'.join(c)) for c in [t.split('_') for t in k]]

    pretty_info = {}
    for k, v in k_tup:
        pretty_info[v] = {
            'nc': k[1],
            'nr': k[2],
            'min_antenna': k[3],
            'count': oinfo[v]
        }

    return pretty_info


def filter_option_arg(src_addr=None, single_user=False, multi_user=False):
    if src_addr:
        if single_user:
            return ["-Y", f"{SU} && {SA} == {src_addr}"]
        elif multi_user:
            return ["-Y", f"{MU} && {SA} == {src_addr}"]
        else:
            return ["-Y", f"{SA} == {src_addr}"]
    else:
        if single_user:
            return ["-Y", f"{SU}"]
        elif multi_user:
            return ["-Y", f"{MU}"]
        else:
            return []


def process_pcap(file_path, save_path=None, src_addr=None, single_user=False, multi_user=False):
    pass


def process_json(file_path, save_path=None, src_addr=None, single_user=False, multi_user=False, info=False, length=None):
    try:
        filter_option = filter_option_arg(src_addr, single_user, multi_user)
        result = subprocess.run(
            ["tshark", "-r", file_path, "-T", "json"] + filter_option,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        json_data = json.loads(result.stdout)

        total_cbr_len = 0
        values = []
        for packet in json_data:
            if "_source" in packet and "layers" in packet["_source"]:
                layers = packet["_source"]["layers"]

                if "wlan.mgt" in layers:
                    compressed_beamforming_report = layers["wlan.mgt"]["Fixed parameters"]["wlan.vht.compressed_beamforming_report"] # wlan.vht.compressed_beamforming_report
                    nc_index = layers["wlan.mgt"]["Fixed parameters"]['wlan.vht.mimo_control.control_tree']['wlan.vht.mimo_control.ncindex'] # wlan.vht.mimo_control.ncindex
                    nr_index = layers["wlan.mgt"]["Fixed parameters"]['wlan.vht.mimo_control.control_tree']['wlan.vht.mimo_control.nrindex'] # wlan.vht.mimo_control.nrindex

                    cbr_len = len(compressed_beamforming_report)
                    total_cbr_len += cbr_len

                    nc = int(nc_index, 16) + 1
                    nr = int(nr_index, 16) + 1
                    min_antenna = min(nc, nr)

                    if length:
                        # Resolve Wireshark Bug diff in length 12
                        if (abs(cbr_len - length) == 12) or (abs(cbr_len - length) == 0):
                            values.append(compressed_beamforming_report)
                            set_info(cbr_len, nc, nr, min_antenna)
                        else:
                            # print(f"{file_path}'s CBR Length ({cbr_len} != {length}).")
                            pass
                        continue

                    values.append(compressed_beamforming_report)
                    set_info(cbr_len, nc, nr, min_antenna)

        cbr_info = get_info()
        if info:
            cbr_info = get_pinfo(cbr_info)

        return values, total_cbr_len, cbr_info

    except Exception as e:
        print(f"Error: {e}")
        return -1, -1, -1
