import os
import logging
import azure.functions as func
from utils import send_response
import azure.cosmos as cosmos_func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connection_host = os.environ.get('CONNECTION_HOST')
    key_db = os.environ.get('KEY_DB')

    try:
        page_parameter = req.get_json().get('page')

        if page_parameter is None:
            return send_response({ "message":'Page Parameter is required', "code": 400 }, status_code=400)

        client = cosmos_func.CosmosClient(connection_host, key_db)

        database_name = os.environ.get('DATABASE_NAME')

        database = client.create_database_if_not_exists(id=database_name)

        container_name= os.environ.get('CONTAINER_NAME')

        container = database.create_container_if_not_exists(
            id=container_name, 
            partition_key=cosmos_func.PartitionKey(path="/page"),
            offer_throughput=400
        )

        response = container.query_items(
            query='SELECT * FROM c WHERE c.page = @page',
            parameters=[ dict(name="@page", value=page_parameter) ],
            enable_cross_partition_query=True,
        )

        page = list(response)

        if len(page) == 0:
            return send_response(
                { "message": 'There is ot any page with the id "{}"'.format(page_parameter) , "code": 404 }
                , status_code=404
            )

        item = page[0]

        item['counter'] = item['counter'] + 1
        
        container.upsert_item(item)
        
        return send_response( { "message": 'Page counter updated successfully', "code": 200 } )
        
    except Exception as error:
        logging.error(error)
        response_message = {
            'message': 'Something went wrong'
            , 'code': 500
        }
        return send_response(response_message, status_code=500)
