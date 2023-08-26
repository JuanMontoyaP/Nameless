"""
Connection to DynamoDB
"""

import os
from typing import List
from dotenv import load_dotenv

import boto3
from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource
from boto3.dynamodb.conditions import Key
from fastapi.encoders import jsonable_encoder

from ..utils.logs import LOGGER

load_dotenv()


class Config:
    """
    This class is used to configure the DynamoDB connection.
    """
    DB_REGION_NAME = os.getenv('DB_REGION_NAME')
    DB_ACCESS_KEY_ID = os.getenv('DB_ACCESS_KEY_ID')
    DB_SECRET_ACCESS_KEY = os.getenv('DB_SECRET_ACCESS_KEY')


class DynamoDB():
    """
    This class is used to connect to DynamoDB.

    The `table` attribute is a DynamoDB table object.
    The `dynamo_resource` attribute is a DynamoDB resource object.
    """
    dynamo_resource = None
    table = None

    table = None
    dynamo_resource: ServiceResource = boto3.resource(
        'dynamodb',
        region_name=Config.DB_REGION_NAME,
        aws_access_key_id=Config.DB_ACCESS_KEY_ID,
        aws_secret_access_key=Config.DB_SECRET_ACCESS_KEY
    )

    def check_if_table_exists(self, table_name):
        """
        The function checks if a table exists in DynamoDB and returns a boolean value indicating its
        existence.

        Params 
            - table_name: The `table_name` parameter is a string that represents the name of the 
                table you want to check for existence in a DynamoDB database

        Returns 
            - A boolean value indicating whether the table exists or not. If the table exists, it 
                returns True. If the table does not exist, it returns False.
        """
        try:
            table = self.dynamo_resource.Table(table_name)
            table.load()
            exist = True
        except ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                exist = False
            else:
                print(f"Error: {err.response['Error']['Message']}")
                raise
        else:
            self.table = table
        return exist

    async def create_item(self, item):
        """
        The `create_item`method creates an item in a table, and logs an error message if the item 
        cannot be created.

        Params 
            - item: The "item" parameter is an object that represents the item you want to create 
            in a database table. It is passed to the "create_item" method as an argument
        """
        try:
            self.table.put_item(Item=jsonable_encoder(item))
        except ClientError as err:
            LOGGER.error("Item ca not be created: %s",
                         err.response['Error']['Message'])
            raise

    async def get_item_info(
        self,
        keys: List[str],
        item_keys: List[str],
        data_to_get: List[str] = None
    ):
        """
        The `get_item_info` method retrieves information about an item from a dynamo using the
        provided keys and data attributes.

        Params 
            - keys List[str]: A list of strings representing the keys used to identify the item 
                in the table
            - item_keys List[str]: A list of strings representing the values of the keys used to 
                retrieve the item from the table
            - data_to_get List[str]: The `data_to_get` parameter is a list of strings that specifies 
                the attributes of the item that you want to retrieve from the table. If this 
                parameter is provided, only the specified attributes will be returned in the 
                response. If it is not provided, all attributes of the item will be returned

        Returns 
            - The item retrieved from the table as a dictionary, or `None` if the item does not 
                exist.
        """
        item_to_get = dict(zip(keys, item_keys))
        try:
            if data_to_get:
                response = self.table.get_item(
                    Key=item_to_get,
                    AttributesToGet=data_to_get
                )
            else:
                response = self.table.get_item(
                    Key=item_to_get,
                )
        except ClientError as err:
            LOGGER.error("Could not get item: %s",
                         err.response['Error']['Message'])
            raise

        try:
            item = response['Item']
            return item
        except KeyError:
            return None

    async def scan_item(self, key: str, item: str):
        """
        The `scan_item` method scans a table for items that match a given key and returns a list of
        those items.

        Params
            - key str: The `key` parameter is a string that represents the key attribute of the 
                item you want to scan for. It is used in the filter expression to specify the 
                condition for scanning the items
            - item str: The `item` parameter is a string that represents the value you want to 
                filter on. The scan operation will return all items from the table that have a 
                matching value for the specified key

        Returns 
            - A list of items that match the given key and item.
        """
        items = []
        try:
            response = self.table.scan(**{
                'FilterExpression': Key(key).eq(item),
            })

            items.extend(response.get('Items', []))
        except ClientError as err:
            LOGGER.error("Could not scan user: %s",
                         err.response['Error']['Message'])
            raise

        return items
