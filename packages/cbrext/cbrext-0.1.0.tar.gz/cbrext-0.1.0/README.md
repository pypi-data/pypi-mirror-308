# Compressed Beamforming Extractor

## Overview

This tool extracts the Compressed Beamforming Report data from a PCAP file and saves it to a JSON or CSV file.

## Dependencies

```plaintext
python >= 3.9
wireshark >= 4.4.0
```

## Usage

```sh
cbrext test/pcaps/beamforming.pcap -W test_out.json
```

### Options

```plaintext
-h,  --help                     Show this help message and exit

-d,  --dir                      Extract all PCAP files in a directory
-W,  --write    <file or dir>   Write the extracted data to a file

-sa, --src-addr <wlan.sa>       Filter by source address
-su, --single-user              Extract SU
-mu, --multi-user               Extract MU

-j,  --json                     Write the extracted data to a JSON file (default)
-c,  --csv                      Write the extracted data to a CSV file  # in progress
-p,  --pcap                     Write the extracted data to a PCAP file # in progress
-b,  --binary                   Decode the CBR hex to binary

-i,  --info                     Print the CBR info
-l,  --length                   Setting the length of the CBR data

-v,  --verbose                  Print verbose output
```

### Examples

#### Directory Option: `-d`

```sh
cbrext -d tests/pcaps/ -W test_out.json
```

shell out:
```plaintext
$ cbrext -d tests/pcaps/ -W test_out.json
Processing tests/pcaps/ and generating output...
[ 1/2 ] filtered_4F_0.pcap -> CBR Length: 7900612
[ 2/2 ] filtered_4F_m0.pcap -> CBR Length: 12088706
PCAP Count: 2
Total CBR Length: 19989318
```

json out:
```plaintext
[
    [
        "75:2e:a9:68 ...",
        "75:2f:69:68 ...",
        ...
    ],
    [
        "69:70:77:f5 ...",
        "69:70:77:f5 ...",
        ...
    ]
]
```

#### Binary Option: `-b`

```sh
cbrext tests/pcaps/filtered_4F_0.pcap -W test_out.json -i -l 2639
```

shell out:
```plaintext
$ cbrext tests/pcaps/filtered_4F_0.pcap -W test_out.json -i -l 2639
Processing tests/pcaps/filtered_4F_0.pcap and generating output...
Total CBR Length: 7900612
{'2639_2_3_2': {'nc': '2', 'nr': '3', 'min_antenna': '2', 'count': 126}, '2651_2_3_2': {'nc': '2', 'nr': '3', 'min_antenna': '2', 'count': 2153}}
```

#### Length Option: `-l`

```sh
cbrext tests/pcaps/filtered_4F_0.pcap -W test_out.json -i -l 2639
```

json out:

__Note: It is recommended to determine and set an appropriate value to limit the length information of CBRs after analyzing it with the `-i` option. Currently, Wireshark has a bug where the CBR length is recognized as 4 bytes longer in portion of packets. Therefore, you can use the `-l` option to extract only the desired length and the `-i` option to check the number of antennas.__

```plaintext
[
    "75:2e:a9:68 ...",
    "75:2f:69:68 ...",
    ...
]
```


## Development

### Installation

```sh
python -m pip install .
```

### Updating

```sh
python -m pip install --upgrade .
```

### Testing

```sh
python -m unittest discover -s tests
```

### Uninstalling

```sh
python -m pip uninstall cbrext
```

## Citation

Meneghello, Francesca, Rossi, Michele, and Restuccia, Francesco. "DeepCSI: Rethinking Wi-Fi Radio Fingerprinting Through MU-MIMO CSI Feedback Deep Learning." In IEEE International Conference on Distributed Computing Systems, 2022.

See: https://github.com/francescamen/DeepCSI for more details.
