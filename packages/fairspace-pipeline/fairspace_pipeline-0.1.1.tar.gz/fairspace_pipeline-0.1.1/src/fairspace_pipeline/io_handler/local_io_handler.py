"""
This module contains classes and functions for running Fairspace pipelines locally. It includes classes
for processing source files, writing ttl files, and uploading data to Fairspace.

Classes:
    LocalIOHandler: Class to handle running pipeline locally.

"""
import csv
import json
import logging
import os
import pathlib
from typing import List, override

from fairspace_pipeline.api_client.fairspace_api_client import FairspaceApi
from fairspace_pipeline.graph.fairspace_graph import FairspaceGraph
from fairspace_pipeline.io_handler.io_handler_interface import IOHandlerInterface
from rdflib import Graph

log = logging.getLogger()


class LocalIOHandler(IOHandlerInterface):
    """
    Handles local input/output operations for Fairspace integration.
    """
    def __init__(self, output_data_directory: str, fairspace_graph: FairspaceGraph, encoding='utf-8'):
        super().__init__(fairspace_graph)
        self.encoding = encoding
        self.output_data_directory = output_data_directory

    def read_json(self, file_path: str):
        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                return data
        except Exception as e:
            log.error('Error reading source file content: ' + str(e))
            return None

    def read_csv(self, file_path: str):
        try:
            with open(file_path, "r", encoding=self.encoding, errors='replace') as file:
                data = csv.DictReader(file.read().splitlines(), escapechar='\\')
                return data
        except Exception as e:
            log.error('Error reading source file content: ' + str(e))
            return None

    def write_to_ttl(self, graph: Graph, filename: str, output_directory: str, prefix: str = ""):
        new_file_name = prefix + pathlib.Path(filename).with_suffix('.ttl').name  # tmp
        output = os.path.join(output_directory, new_file_name)
        if graph:
            graph.serialize(destination=output, format="turtle")
            log.info('Data saved to: ' + output)

    @override  # Extracts data from the source directories and transforms it into graph data and saves it as TTL files
    def transform_data(self, source_study_directories: List[str], source_study_prefixes: List[str]):
        log.warning("transform_data method not implemented, skipping...")
        pass

    @override  # Uploads data to Fairspace by sending the saved TTl files to the Fairspace API
    def send_to_api(self, api: FairspaceApi, source_study_directories: List[str]):
        log.warning("send_to_api method not implemented, skipping...")
        pass
