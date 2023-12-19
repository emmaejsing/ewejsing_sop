"""BatchRunPeers_hub.py - Batch run of Peers with multiple scenarios and consolidated outputs."""

from pathlib import Path
import shutil
import sys
import os
import time
import pickle
import pandas as pd


def get_paths(analysis_label, input_data_file):
    usr = os.getlogin()
    paths = {}
    # Location of PEERS repo on local machine
    paths['local_peers_root'] = Path(f"C:/users/{usr}/code/peers_ewe")

    # Location of folder with local (C-drive) with Excel input data files and results from model runs
    paths['northsea_data_path'] = Path(f"C:/users/{usr}/local_peers_data/excel")
    paths['analysis_path'] = paths['northsea_data_path'] / analysis_label
    paths['output_path'] = paths['analysis_path'] / "output"
    paths['output_path'].mkdir(parents=True, exist_ok=True)

    # Location of PEERS template files (output datafile single model run + considated
    #paths['xls_template_file'] = Path(f"C:/users/{usr}/code/northsea/templates") / "output.xlsx"
    paths['xls_template_file'] = paths['northsea_data_path'] / "templates" / "output.xlsx"
    paths['xls_template_batch_file'] = paths['northsea_data_path'] / "templates" / "output_batch.xlsx"
    paths['xls_template_dashboard'] = paths['northsea_data_path'] / "templates" / "dashboard.xlsx"

    paths['xls_input_file'] = paths['northsea_data_path'] / input_data_file
    paths['xls_baseline'] = str(paths['output_path'] / f"baseline__{analysis_label}.xlsx")
    paths['xls_output_batch'] = str(paths['output_path'] / f"overview__{analysis_label}.xlsx")
    return paths


def copy_input_data(paths):
    shutil.copy(paths['xls_input_file'], paths['analysis_path'] / paths['xls_input_file'].name)


def execute_model_runs(analysis_label, paths):

    # Create empty objects for PEERS and batchruns
    peers = Peers('empty')
    batchrun = PeersBatchOutput(peers, '')

    scenarios = []

    # Load base data and solve base scenario
    label = "baseline"
    scenario_info = dict(label=label, description=label)
    peers = Peers('empty')
    peers.load(paths['xls_input_file'])


    peers.solve()
    peers.save("excelfiles", paths['xls_baseline'], paths['xls_template_file'])
    batchrun.add_scenario(peers, label)
    scenarios.append(scenario_info)

    # Save assets and balance for all scenarios to one file
    # batchrun.save_excel(paths['xls_output_batch'], paths['xls_template_batch_file'])

    #with open(paths['analysis_path'] / "scenario_info.pickle", "wb") as f:
    #    pickle.dump(scenarios, f)


if __name__ == "__main__":


    RUN_MULTIPLE_VARIATIONS = False

    start_time = time.time()

    if RUN_MULTIPLE_VARIATIONS:
        version = "24"  # <----------- SET VERSION
        capa_levels = range(0, 65, 5)
        variations = [f"{x:02}GW" for x in capa_levels]
    else:
        variations = ["DK_hourly_simple_no_h2.xlsx"]  # <----------- SET FILENAME IF EXECUTING SINGLE SCENARIO RUN
        if variations[0].endswith(".xlsx"):
            variations[0] = variations[0].split(".xlsx")[0]

    for variation in variations:
        if RUN_MULTIPLE_VARIATIONS:
            input_data_file = f"AF23_base_round{version}_{variation}.xlsx"
        else:
            input_data_file = f"{variation}.xlsx"

        analysis_label = input_data_file.split(".")[0]

        paths = get_paths(analysis_label, input_data_file)
        copy_input_data(paths)
        sys.path.append(str(paths['local_peers_root']))

        from peers.peers import Peers
        from peers.batchoutput import PeersBatchOutput

        execute_model_runs(analysis_label, paths)

    # Display time consumption
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{len(variations)} model runs took {elapsed_time:.2f} seconds to execute.")