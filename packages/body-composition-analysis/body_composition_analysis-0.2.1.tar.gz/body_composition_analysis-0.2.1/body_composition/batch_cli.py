import argparse
import os
from body_composition.python_batch_api import BatchAPIProcessor

def main():
    parser = argparse.ArgumentParser(description="Batch process multiple cases for body composition analysis.")
    
    parser.add_argument(
        "-master_list_path",
        type=str,
        required=True,
        help="Path to the master CSV file containing case information."
    )
    parser.add_argument(
        "-batch_run_save_file",
        type=str,
        required=True,
        help="Output file path to save the combined batch results."
    )
    parser.add_argument(
        "-verbose",
        type=int,
        default=1,
        help="Verbosity level: 0 for silent, 1 for verbose."
    )

    args = parser.parse_args()

    # Run the BatchAPIProcessor with provided arguments
    BatchAPIProcessor(
        master_list_path=args.master_list_path,
        batch_run_save_file=args.batch_run_save_file,
        verbose=args.verbose
    )

if __name__ == "__main__":
    main()
