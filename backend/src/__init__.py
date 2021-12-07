import logging

import os
import json
from itertools import tee
import azure.cosmos as cosmos_func
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connection_host = '<connection_host>'
    key_db = '<key_db>'

    try:
        # with cosmos_func.CosmosClient(connection_host, key_db) as client:
        client = cosmos_func.CosmosClient(connection_host, key_db)

        database_name = 'database_name'

        database = client.create_database_if_not_exists(id=database_name)

        container_name= '<container_name>'
        
        container = database.create_container_if_not_exists(
            id=container_name, 
            partition_key=cosmos_func.PartitionKey(path="/page"),
            offer_throughput=400
        )

        items = container.query_items('SELECT * FROM c')

        print("   items   ")
        print(items)
        print("   json.dumps(items)   ")
        result = tee(items)
        print(result)
        for i, r in enumerate(result):
            print(r)

        return func.HttpResponse(f"Hablame, 'Testing'. This HTTP triggered function executed successfully.")
    except Exception as error:
        print(error)
        response_message = {
            'message': 'Something went wrong'
            , 'error': error
        }
        return func.HttpResponse('Something went Wrong', status_code=500)

    # url = os.environ.get('ACCOUNT_ID')
    # key = os.environ.get('ACCOUNT_KEY')

    
    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hablame, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #         "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #         status_code=200
    #     )
