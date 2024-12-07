import os
import argparse

def copy_files_with_extension(extension, output_file):
    # Directories and files to ignore
    ignore_dirs = {'__pycache__', 'tests', 'test', 'venv', 'node_modules', 'build'}
    ignore_files = {'__init__.py'}

    # Open the output file in write mode
    with open(output_file, 'w') as outfile:
        # Walk through the current directory
        for root, dirs, files in os.walk('.'):
            # Remove ignored directories from the search
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files:
                # Check if the file has the desired extension and is not in the ignore list
                if file.endswith(f'.{extension}') and file not in ignore_files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as infile:
                        # Write the file path and content to the output file
                        relative_path = os.path.relpath(file_path, start='.')
                        outfile.write(f'# {relative_path}\n\n')
                        outfile.write(infile.read())
                        outfile.write('\n\n')

def main():
    parser = argparse.ArgumentParser(description='Copy content of files with a specific extension to a single file.')
    parser.add_argument('--ext', required=True, help='File extension to search for (e.g., py, ts, tf)')
    args = parser.parse_args()

    # Define the output file path in the current directory
    output_file = 'cpo.txt'

    # Copy files with the specified extension
    copy_files_with_extension(args.ext, output_file)
    print(f'Content copied to {output_file}')

if __name__ == '__main__':
    main()