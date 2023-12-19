import os
import sys
import shutil
from pathlib import Path

file_types = {".pickle": "picklefiles", ".xlsx": "excelfiles"}

output_template_path = Path(f"C:/users/{os.getlogin()}/local_peers_data") / "templates" / "output.xlsx"
basepath = Path(f"C:/users/{os.getlogin()}/local_peers_data/scenarios")

output_file_prefix = "output__"


def copy_input_data(input_path, output_folder):
    shutil.copy(input_path, output_folder / input_path.name)

def create_folder(folder):
    folder.mkdir(parents=True, exist_ok=True)

def get_default_output_folder(input_path: Path) -> Path:
    output_folder = basepath / input_path.stem / "output"
    create_folder(output_folder)
    return output_folder

def get_default_sequence_folder(input_path: Path, type_: str) -> Path:
    output_folder = basepath / input_path.stem / type_ / "sequence"
    create_folder(output_folder)
    return output_folder


def get_default_input_data_backup_folder(input_path: Path) -> Path:
    input_data_backup_folder = basepath / input_path.stem / "input"
    create_folder(input_data_backup_folder)
    return input_data_backup_folder

def execute_model_run(input_path, output_path) -> None:
    """ Load input data, solve scenario and save output. """
    output_method = file_types[input_path.suffix]
    usr = os.getlogin()
    local_peers_root = f"C:/users/{usr}/code/peers_ewe"

    # Hacky way to make Peers available from within the northsea repo
    sys.path.append(local_peers_root)
    from peers.peers import Peers

    peers = Peers('empty')
    peers.load(input_path)
    peers.solve()
    peers.save(output_method, output_path, output_template_path)