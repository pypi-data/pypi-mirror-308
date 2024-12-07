"""
This module contains classes and functions for running Fairspace pipelines on AWS S3 buckets. It includes classes
for processing source files, writing ttl files, and uploading data to Fairspace.

Classes:
    AwsS3IOHandler: Class to handle running pipeline on AWS S3 buckets.

"""

import logging
import os
import pathlib
import sys
from typing import List, override

import boto3
from botocore.exceptions import NoCredentialsError
from rdflib import Graph

from fairspace_pipeline.api_client.fairspace_api_client import FairspaceApi
from fairspace_pipeline.graph.fairspace_graph import FairspaceGraph
from fairspace_pipeline.io_handler.io_handler_interface import IOHandlerInterface

log = logging.getLogger()


class AwsS3IOHandler(IOHandlerInterface):
    """
    IOHandler implementation for interacting with AWS S3.

    This class provides methods for extraction, transformation and loading of data while interacting with AWS S3 bucket.
    """

    def __init__(self, source_bucket_name: str, output_bucket_name: str, fairspace_graph: FairspaceGraph,
                 aws_profile_name='default', encoding='utf-8-sig'):
        super().__init__(fairspace_graph)
        self.aws_profile_name = aws_profile_name
        session = boto3.Session(profile_name=aws_profile_name)
        self.s3_client = session.client('s3')
        self.source_bucket_name = source_bucket_name
        self.output_bucket_name = output_bucket_name
        self.encoding = encoding

    def initialize_s3_client(self):
        log.info(f"Initializing new session for S3 client with profile {self.aws_profile_name}...")
        session = boto3.Session(profile_name=self.aws_profile_name)
        self.s3_client = session.client('s3')

    def get_object_s3(self, bucket_name, file_key, retry=True):
        try:
            return self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
        except Exception as e:
            log.error(f"Error getting object {file_key} from {bucket_name} AWS S3 bucket.")
            if retry:
                log.info("Retrying upload with new session...")
                self.initialize_s3_client()
                return self.get_object_s3(bucket_name, file_key, False)
            else:
                raise

    def read_paginated_list_s3(self, bucket_name: str, path: str, page_size: int, retry=True):
        try:
            paginator = self.s3_client.get_paginator("list_objects_v2")
            return paginator.paginate(Bucket=bucket_name, Prefix=path, PaginationConfig={"PageSize": page_size})
        except Exception as e:
            log.error(f"Error listing paginated objects from {bucket_name} AWS S3 bucket with prefix {path}.")
            if retry:
                log.info("Retrying upload with new session...")
                self.initialize_s3_client()
                return self.read_paginated_list_s3(bucket_name, path, page_size, False)
            else:
                raise

    def get_objects_by_suffix_s3(self, bucket_name: str, path: str, page_size: int, suffix: str):
        page_iterator = self.read_paginated_list_s3(bucket_name, path, page_size)
        objects = page_iterator.search(f"Contents[?ends_with(Key, `{suffix}`)][]")
        return objects

    def get_object_list_s3(self, bucket_name, source_directory, retry=True):
        try:
            return self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=source_directory)
        except Exception as e:
            log.error(f"Error listing objects from {bucket_name} AWS S3 bucket with prefix {source_directory}.")
            if retry:
                log.info("Retrying upload with new session...")
                self.initialize_s3_client()
                return self.get_object_list_s3(bucket_name, source_directory, False)
            else:
                raise

    def read_file_content_s3(self, bucket_name: str, file_key: str):
        file_object = self.get_object_s3(bucket_name, file_key)
        file_content = file_object['Body'].read().decode('utf-8', errors="ignore")
        return file_content

    def upload_file_s3(self, bucket_name: str, s3_object_name: str, object_to_upload=None, retry=True):
        try:
            self.s3_client.put_object(Body=object_to_upload, Bucket=bucket_name, Key=s3_object_name)
            log.info(f"Successfully uploaded {s3_object_name} to {bucket_name} AWS S3 bucket.")
            return True
        except NoCredentialsError:
            log.error("AWS S3 bucket credentials not available.")
            raise
        except Exception as e:
            log.error(f"Error uploading {s3_object_name} to {bucket_name} AWS S3 bucket.")
            if retry:
                log.info("Retrying upload with new session...")
                self.initialize_s3_client()
                self.upload_file_s3(bucket_name, s3_object_name, object_to_upload, False)
                return True
            else:
                raise

    def upload_file_to_fairspace(self, api, file_name):
        try:
            file_content = self.read_file_content_s3(self.output_bucket_name, file_name)
            if not file_content:
                raise FileNotFoundError(f"File {file_name} not found.")
            log.info(f"Start uploading file {file_name} to Fairspace...")
            api.upload_metadata('turtle', file_content, False)
            log.info(f"File {file_name} uploaded.")
        except Exception as e:
            log.error(f"Error uploading file {file_name}")
            log.error(e)
            sys.exit(1)

    def write_to_ttl(self, graph: Graph, filename: str, output_directory: str, prefix: str = ""):
        log.info(f"Writing {filename} graph to ttl file in {output_directory} directory ...")
        new_file_name = prefix + pathlib.Path(filename).with_suffix('.ttl').name
        output = os.path.join(output_directory, new_file_name)
        file = graph.serialize(format="turtle")
        self.upload_file_s3(self.output_bucket_name, output, file)

    @override  # Extracts data from the source directories and transforms it into graph data and saves it as TTL files
    def transform_data(self, source_study_directories: List[str], source_study_prefixes: List[str]):
        log.warning("transform_data method not implemented, skipping...")
        pass

    @override  # Uploads data to Fairspace by sending the saved TTl files to the Fairspace API
    def send_to_api(self, api: FairspaceApi, source_study_directories: List[str]):
        log.warning("send_to_api method not implemented, skipping...")
        pass
