
from src.index import default  # Import the default function from the src.index module
import argparse  # Import the argparse module to handle command-line arguments
import json  # Import the json module to handle JSON data
def main():
    # Create an argument parser to handle command-line input
    parser = argparse.ArgumentParser(description="py-import-parser")
    
    # Parse known and unknown arguments. We only need unknown arguments here.
    _, unknown_args = parser.parse_known_args()
    
    # Convert unknown arguments into a kwargs dictionary
    kwargs = {}
    for i in range(0, len(unknown_args), 2):
        key = unknown_args[i].lstrip("--")  # Remove the leading "--" from the argument name
        value = unknown_args[i + 1] if i + 1 < len(unknown_args) else None  # Handle key-value pairs
        kwargs[key] = value  # Add the key-value pair to the kwargs dictionary

    # Pass the kwargs to the default function
    result=default(**kwargs)
    
    print(result)  # Print the result as a string

# Entry point for the script
if __name__ == "__main__":
    main()
