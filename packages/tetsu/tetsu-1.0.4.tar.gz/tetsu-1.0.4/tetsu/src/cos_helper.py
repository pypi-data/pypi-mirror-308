# COS Helper --- Interact with COS via Python

import os
import ast
import ibm_boto3
import pandas as pd

from ibm_botocore.client import Config
from ibm_boto3.s3.transfer import TransferConfig

from tetsu.src import cloudant_helper
from tetsu.src.log_helper import logger

logger = logger(name=__name__, handler="console")


class COSHelper:
    def __init__(
        self,
        environment: str,
        cloudant_doc=None,
        creds=None
    ):
        """
        Instantiation of the COSHelper class

        :param environment: The environment (prod/metrics or staging)
        :param cloudant_doc: The cloudant document object that will be used to retrieve credentials
                             If None, user env will be searched for a document
        """
        if cloudant_doc is None:
            try:
                self.cloudant_doc = ast.literal_eval(os.getenv("cloudant_document"))
            except Exception as e:
                raise RuntimeError("cloudant_document environment variable not set", e)
        else:
            self.cloudant_doc = cloudant_doc

        if creds is None:
            self.creds = {
                "cos_api_key": [environment, "cos", "apikey"],
                "cos_resource_crn": [environment, "cos", "resource_instance_id"],
                "cos_endpoint": [environment, "cos", "endpoints"],
                "cos_auth_endpoint": [environment, "cos", "auth_endpoint"],
            }
        else:
            self.creds = creds
        self.creds = cloudant_helper.get_credentials(
            doc=self.cloudant_doc, creds=self.creds
        )

        self.cos_object = ibm_boto3.client(
            service_name="s3",
            ibm_api_key_id=self.creds["cos_api_key"],
            ibm_service_instance_id=self.creds["cos_resource_crn"],
            ibm_auth_endpoint=self.creds["cos_auth_endpoint"],
            config=Config(signature_version="oauth"),
            endpoint_url=self.creds["cos_endpoint"],
        )

        # This allows for multi-part uploads for files greater than 5MB
        self.config = TransferConfig(
            multipart_threshold=1024 * 1024 * 25,
            max_concurrency=10,
            multipart_chunksize=1024 * 1024 * 25,
            use_threads=True,
        )

    def upload_file(self,
                    files_list: list,
                    cos_bucket: str,
                    file_key_list: list = None,) -> None:
        """
        This function takes a list of files and uploads them to the specified COS bucket

        :param files_list: The list of files that will be uploaded to the bucket
                           (Needs to be a list even if there is only one file)
        :param cos_bucket: The COS bucket to upload the files to
        :param file_key_list: The list of file keys that will be uploaded to the COS bucket
        """
        if file_key_list is None:
            file_key_list = files_list
        for i in range(len(files_list)):
            try:
                self.cos_object.upload_file(
                    Filename=files_list[i], Bucket=cos_bucket, Key=file_key_list[i], Config=self.config
                )
            except Exception as e:
                logger.exception(
                    f"Could not upload file to {cos_bucket} due to {e}"
                )
            else:
                logger.info(f"File uploaded to {cos_bucket} successfully")

    def upload_df(
        self,
        df: pd.DataFrame,
        file_name: str,
        cos_bucket: str,
        file_key: str = None,
        file_type: str = None
    ) -> None:
        """
        This function takes a dataframe and uploads it to the specified COS bucket

        :param df: The dataframe to be uploaded
        :param file_name: The name of the file once uploaded
        :param file_type: The file type
        :param cos_bucket: The COS bucket to upload the df to
        :param file_key: The key of the file to be uploaded
        """
        if file_type == "csv":
            filename = file_name + ".csv"
            df.to_csv(filename, sep=",", index=False)
        elif file_type == "parquet":
            filename = file_name + ".csv"
            df.to_parquet(filename)
        elif file_type == "pickle":
            filename = file_name + ".pkl"
            df.to_pickle(filename)
        else:
            raise RuntimeError("Please pick from csv, parquet, or pickle")

        if file_key is None:
            file_key = filename
        try:
            self.cos_object.upload_file(
                Filename=filename,
                Bucket=cos_bucket,
                Key=file_key,
                Config=self.config,
            )
        except Exception as e:
            logger.exception(
                f"Could not upload {filename} to {cos_bucket} due to {e}"
            )
        else:
            logger.info(f"{filename} uploaded to {cos_bucket} successfully")

    def download_file(self,
                      cos_bucket: str,
                      files_list: list,
                      file_key_list: list = None) -> None:
        """
        This function takes a list of files and downloads them from a COS bucket to the project's WORKDIR

        :param files_list: The list of files that will be downloaded from the bucket
                           (Needs to be a list even if there is only one file)
        :param cos_bucket: The COS bucket to download the files from
        :param file_key_list: The list of file keys that will be downloaded from the COS bucket
        """
        if file_key_list is None:
            file_key_list = files_list
        for i in range(len(files_list)):
            try:
                self.cos_object.download_file(
                    Filename=files_list[i], Bucket=cos_bucket, Key=file_key_list[i]
                )
            except Exception as e:
                logger.exception(
                    f"Could not download file from {cos_bucket} due to {e}"
                )
            else:
                logger.info(f"File downloaded from {cos_bucket} successfully")
