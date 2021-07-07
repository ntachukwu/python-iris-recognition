# -----------------------------------------------------------------------------
# Import
# -----------------------------------------------------------------------------
import argparse
import re
import os
from pathlib import Path
from time import time

from fnc.extractFeature import extractFeature
from fnc.matching import matching


# ------------------------------------------------------------------------------
#	Argument parsing
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str,
                    help="Path to the file that you want to verify.")

parser.add_argument("--temp_dir", type=str, default="./templates/",
                    help="Path to the directory containing templates.")

parser.add_argument("--thres", type=float, default=0.38,
                    help="Threshold for matching.")

args = parser.parse_args()

def main():
    # -----------------------------------------------------------------------------
    # Execution
    # -----------------------------------------------------------------------------
    # Extract feature
    start = time()
    print('>>> Start verifying {}\n'.format(args.file))
    template, mask, file = extractFeature(args.file)


    # Matching
    result = matching(template, mask, args.temp_dir, args.thres)


    if result == -1:
        print('>>> No registered sample.')

    elif result == 0:
        print('>>> No sample matched.')

    else:
        print('>>> {} samples matched (descending reliability):'.format(len(result)))
        for res in result:
            print("\t", res)

            # To return the path to the original file
            reg_pattern = re.compile(res[:-4] + '$')
            for root, dirs, files in os.walk(os.path.abspath("../")):
                for file in files:
                    if reg_pattern.match(file):
                        filepath = os.path.join(root, file)
                        print("\t", "Path to original Image: ",
                            filepath)


    # Time measure
    end = time()
    print('\n>>> Verification time: {} [s]\n'.format(end - start))

if __name__ == '__main__':
    main()

