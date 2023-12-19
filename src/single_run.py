from pathlib import Path
import time

from peers_exec_tools import basepath, get_default_output_folder, \
    copy_input_data, execute_model_run, get_default_input_data_backup_folder, output_file_prefix

if __name__ == "__main__":
    start_time = time.time()

    # Specific input file using a basepath and an input_scenario_filename name
    # ===============================================================

    input_scenario_filename = "DK_hourly_high_eff_elyz.xlsx"  # <======== Specify name of input data sheet (including file extension)
    input_path = basepath / f"{input_scenario_filename}"

    input_data_backup_folder = get_default_input_data_backup_folder(input_path)
    copy_input_data(input_path, input_data_backup_folder)

    output_folder = get_default_output_folder(input_path)
    output_file = output_folder / f"{output_file_prefix}{input_scenario_filename}"

    # Execute single PEERS run
    # ========================

    execute_model_run(input_path, output_file)

    # Display execution time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Model execution took {elapsed_time:.2f} seconds.")
    print(f"Model results have been written to file: {output_file}")
