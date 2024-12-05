#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# Author: Lalith Kumar Shiyam Sundar | Sebastian Gutschmayer
# Institution: Medical University of Vienna
# Research Group: Quantitative Imaging and Medical Physics (QIMP) Team
# Date: 04.07.2023
# Version: 0.1.0
#
# Description:
# This module downloads the necessary binaries and models for the orca.
#
# Usage:
# The functions in this module can be imported and used in other modules within the orca to download the necessary
# binaries and models for the orca.
#
# ----------------------------------------------------------------------------------------------------------------------

import logging
import os
import zipfile

import requests
from orcaz import file_utilities
from orcaz import constants
import falconz.resources as falcon_resources

from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, FileSizeColumn, TransferSpeedColumn
import time
import emoji

def download_binaries():
    # ----------------------------------
    # DOWNLOADING THE BINARIES
    # ----------------------------------

    print('')
    print(f'{constants.ANSI_BLUE} {emoji.emojize(":globe_with_meridians:")} BINARIES DOWNLOAD:{constants.ANSI_RESET}')

    print('')
    binary_path = constants.BINARY_PATH
    file_utilities.create_directory(binary_path)
    system_os, system_arch = file_utilities.get_system()
    print(f'{constants.ANSI_ORANGE} Detected system: {system_os} | Detected architecture: {system_arch}'
          f'{constants.ANSI_RESET}')
    download(item_name=f'falcon-{system_os}-{system_arch}', item_path=binary_path,
                      item_dict=falcon_resources.FALCON_BINARIES)
    file_utilities.set_permissions(constants.GREEDY_PATH, system_os)
    file_utilities.set_permissions(constants.DCM2NIIX_PATH, system_os)
    file_utilities.set_permissions(constants.C3D_PATH, system_os)


def download(item_name, item_path, item_dict):
    """
    Downloads the item (model or binary) for the current system.
    :param item_name: The name of the item to download.
    :param item_path: The path to store the item.
    :param item_dict: The dictionary containing item info.
    """
    item_info = item_dict[item_name]
    url = item_info["url"]
    filename = os.path.join(item_path, item_info["filename"])
    directory = os.path.join(item_path, item_info["directory"])

    if not os.path.exists(directory):
        logging.info(f" Downloading {directory}")

        # show progress using rich
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("Content-Length", 0))
        chunk_size = 1024 * 10

        console = Console()
        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            FileSizeColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
            expand=True
        )

        Download_Message = f"ORCA specific executables" if "falcon" in item_name else f"sCT models for {item_name}"

        with progress:  
            task = progress.add_task(f"Downloading {Download_Message}", total=total_size)
            for chunk in response.iter_content(chunk_size=chunk_size):
                open(filename, "ab").write(chunk)
                progress.update(task, advance=chunk_size)

        # Unzip the item
        progress = Progress(  # Create new instance for extraction task
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            FileSizeColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
            expand=True
        )

        with progress:
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                total_size = sum((file.file_size for file in zip_ref.infolist()))
                task = progress.add_task(f"[white] Extracting {Download_Message}",
                                         total=total_size)
                # Get the parent directory of 'directory'
                parent_directory = os.path.dirname(directory)
                for file in zip_ref.infolist():
                    zip_ref.extract(file, parent_directory)
                    extracted_size = file.file_size
                    progress.update(task, advance=extracted_size)

        logging.info(f" {os.path.basename(directory)} extracted.")

        # Delete the zip file
        os.remove(filename)
        print(f"{constants.ANSI_GREEN} Download complete. {constants.ANSI_RESET}")
        logging.info(f" Download complete.")
    else:
        Message = f"ORCA specific executables" if "falcon" in item_name else f"sCT models for {item_name}"
        print(f"{constants.ANSI_GREEN} A local instance of the {Message} has been detected. "
              f"{constants.ANSI_RESET}")
        logging.info(f" A local instance of the {Message} has been detected.")

    return os.path.join(item_path, item_name)
