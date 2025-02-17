import argparse
import os
from pathlib import Path
import pickle
import json
import random
from typing import Union

import third_party.midi_processor.processor as midi_processor

JSON_FILE = "maestro-v2.0.0.json"

# prep_midi
def prep_maestro_midi(maestro_root:Union[str,Path], output_dir:Union[str,Path]):
    """
    ----------
    Author: Damon Gwinn
    Changes : David Pardigol
    ----------
    Pre-processes the maestro dataset, putting processed midi data (train, eval, test) into the
    given output folder
    ----------
    """
    maestro_root = Path(maestro_root)
    output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)
    train_dir = output_dir / "train"
    train_dir.mkdir(exist_ok=True)
    val_dir = output_dir / "val"
    val_dir.mkdir(exist_ok=True)
    test_dir = output_dir / "test"
    test_dir.mkdir(exist_ok=True)

    maestro_json_file = maestro_root / JSON_FILE
    if(not maestro_json_file.is_file()):
        print("ERROR: Could not find file:", maestro_json_file)
        return False

    maestro_json = json.load(open(maestro_json_file, "r"))
    print("Found", len(maestro_json), "pieces")
    print("Preprocessing...")

    total_count = 0
    train_count = 0
    val_count   = 0
    test_count  = 0

    for piece in maestro_json:
        mid         = os.path.join(maestro_root, piece["midi_filename"])
        split_type  = piece["split"]
        f_name      = mid.split("/")[-1] + ".pickle"

        if(split_type == "train"):
            o_file = train_dir / f_name
            train_count += 1
        elif(split_type == "validation"):
            o_file = val_dir / f_name
            val_count += 1
        elif(split_type == "test"):
            o_file = test_dir / f_name
            test_count += 1
        else:
            print("ERROR: Unrecognized split type:", split_type)
            return False

        prepped = midi_processor.encode_midi(mid)

        with open(o_file, "wb") as o_stream:
            pickle.dump(prepped, o_stream)

        total_count += 1
        if(total_count % 50 == 0):
            print(total_count, "/", len(maestro_json))

    print("Num Train:", train_count)
    print("Num Val:", val_count)
    print("Num Test:", test_count)
    return True

# parse_args
def parse_args():
    """
    ----------
    Author: Damon Gwinn
    ----------
    Parses arguments for preprocess_midi using argparse
    ----------
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("root", type=str, help="Root folder for the Maestro dataset or for custom data.")
    parser.add_argument("-output_dir", type=str, default="./dataset/e_piano", help="Output folder to put the preprocessed midi into.")
    return parser.parse_args()

# main
def main():
    """
    ----------
    Author: Damon Gwinn
    ----------
    Entry point. Preprocesses maestro and saved midi to specified output folder.
    ----------
    """

    args            = parse_args()
    root    = args.root
    output_dir      = args.output_dir

    print("Preprocessing midi files and saving to", output_dir)

    prep_maestro_midi(root, output_dir)
    
    print("Done!")
    print("")

if __name__ == "__main__":
    main()
