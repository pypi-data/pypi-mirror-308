import argparse

def main():
    parser = argparse.ArgumentParser(description="extract Compressed Beamforming Data from PCAP file")

    parser.add_argument("input_file", help="Input pcap file path", type=str)
    parser.add_argument('-W', '--write', help="Write the extracted data as JSON file", type=str)

    args = parser.parse_args()

    result = f"Processing {args.input_file} and generating output..."

    if args.write:
        with open(args.write, "w") as file:
            file.write(result)
        print(f"Output saved to {args.write}")
    else:
        print(result)

if __name__ == "__main__":
    main()
