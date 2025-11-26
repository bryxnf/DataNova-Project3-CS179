from manifestParser import ManifestParser

def format_entry(entry):
    (row, col), weight, desc = entry
    return f"[{row:02d},{col:02d}], {{{weight:05d}}}, {desc}"

def main():
    # Path to manifest file
    manifest_file = "manifests/testManifest.txt"

    #Parses the file
    parser = ManifestParser()
    parsed_entries = parser.parse_manifest(manifest_file)

    #Print formatted output
    for entry in parsed_entries:
        print(format_entry(entry))


if __name__ == "__main__":
    main()
