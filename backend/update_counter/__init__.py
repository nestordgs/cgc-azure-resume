import logging

import os
import json
from itertools import tee
import azure.cosmos as cosmos_func
from azure.cosmos import partition_key
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connection_host = os.environ.get('CONNECTION_HOST')
    key_db = os.environ.get('KEY_DB')

    try:
        client = cosmos_func.CosmosClient(connection_host, key_db)

        database_name = os.environ.get('DATABASE_NAME')

        database = client.create_database_if_not_exists(id=database_name)

        container_name= os.environ.get('CONTAINER_NAME')

        container = database.create_container_if_not_exists(
            id=container_name, 
            partition_key=cosmos_func.PartitionKey(path="/page"),
            offer_throughput=400
        )

        page_parameter = req.params.get('page')

        if page_parameter is None:
            return func.HttpResponse('Page parameter is required', status_code=400)

        response = container.query_items(
            query='SELECT * FROM c WHERE c.page = @page',
            parameters=[ dict(name="@page", value=page_parameter) ],
            enable_cross_partition_query=True,
        )

        page = list(response)

        if len(page) is 0:
            return func.HttpResponse('There is not any page with the id "{}"'.format(page_parameter), status_code=404)

        item = page[0]

        item['counter'] = item['counter'] + 1
        
        container.upsert_item(item)
        
        return func.HttpResponse(f"Page counter updated successfully")
        
    except Exception as error:
        print(error)
        response_message = {
            'message': 'Something went wrong'
            , 'error': error
        }
        return func.HttpResponse('Something went Wrong', status_code=500)
