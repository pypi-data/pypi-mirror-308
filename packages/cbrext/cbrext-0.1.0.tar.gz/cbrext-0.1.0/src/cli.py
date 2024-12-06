import os
import argparse
from src.extract import process_pcap, process_json
from src.save import save_json, save_csv


def main():
    parser = argparse.ArgumentParser(description="extract Compressed Beamforming Data from PCAP file")

    parser.add_argument("input",         help="Input .pcap or .pcapng file path or directory", type=str)
    parser.add_argument("-d", "--dir",   help="Treat the input as a directory.",               action="store_true")
    parser.add_argument('-W', '--write', help="Write the extracted data as JSON file",         type=str)

    parser.add_argument("-sa", "--src-addr",    help="Source MAC address", type=str)
    parser.add_argument("-su", "--single-user", help="Single user mode",   action="store_true")
    parser.add_argument("-mu", "--multi-user",  help="Multi user mode",    action="store_true")

    parser.add_argument("-j", "--json", help="Output as JSON", action="store_true", default=True)
    parser.add_argument("-c", "--csv",  help="Output as CSV",  action="store_true")
    parser.add_argument("-p", "--pcap", help="Output as PCAP", action="store_true")
    parser.add_argument("-b", "--binary", help="Output as binary", action="store_true")

    parser.add_argument("-i", "--info",   help="Show the information of the CBR", action="store_true")
    parser.add_argument("-l", "--length", help="Setting the length of the CBR",   type=int)

    parser.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")

    args = parser.parse_args()

    result = f"Processing {args.input} and generating output..."
    print(result)

    if args.dir:
        if os.path.isdir(args.input):
            values = []
            total_report_len = 0
            for root, _, files in os.walk(args.input):
                idx = 0
                for file in files:
                    idx += 1
                    print(f"[ {idx}/{len(files)} ]", end=" ")

                    if file.endswith(".pcap") or file.endswith(".pcapng"):
                        file_path = os.path.join(root, file)
                        
                        cbr_list, cbr_len, cbr_info = process_json(file_path, args.write, args.src_addr, args.single_user, args.multi_user, args.info, args.length)
                        values.append(cbr_list)
                        total_report_len += cbr_len
                        print(f"{file} -> CBR Length: {cbr_len}")
                    else:
                        print(f"{file} -> Error not a valid pcap or pcapng file.")
            
            if (not args.write) and (args.verbose):
                print(values)
            print(f"PCAP Count: {len(values)}")
            print(f"Total CBR Length: {total_report_len}")
            if args.info: print(cbr_info)

            if args.write:
                if args.json:
                    save_json(args.write, values, args.binary)
                elif args.csv:
                    save_csv(args.write, cbr_list, args.binary)
        else:
            print(f"Error: {args.input} is not a valid directory.")
    else:
        if os.path.isfile(args.input) and (args.input.endswith(".pcap") or args.input.endswith(".pcapng")):
            file_path = args.input
            cbr_list, cbr_len, cbr_info = process_json(file_path, args.write, args.src_addr, args.single_user, args.multi_user, args.info, args.length)

            if (not args.write) and (args.verbose):
                print(cbr_list)
            print(f"Total CBR Length: {cbr_len}")

            if (not args.write) and (args.verbose):
                print(values)
            if args.info: print(cbr_info)

            if args.write:
                if args.json:
                    save_json(args.write, cbr_list, args.binary)
                elif args.csv:
                    save_csv(args.write, cbr_list, args.binary)
        else:
            print(f"Error: {args.input} is not a valid pcap or pcapng file.")

if __name__ == "__main__":
    main()
