import os
import logging
import azure.functions as func
from utils import send_response
import azure.cosmos as cosmos_func
from azure.cosmos import partition_key


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connection_host = os.environ.get('CONNECTION_HOST')
    key_db = os.environ.get('KEY_DB')

    try:

        page_parameter = req.params.get('page')

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

        response_query = container.query_items(
            query='SELECT * FROM c WHERE c.page = @page'
            , parameters = [ dict(name="@page", value=page_parameter) ]
            , enable_cross_partition_query = True
        )

        list_pages = list(response_query)

        if len(list_pages) == 0:
            return send_response(
                { "message": 'There is ot any page with the id "{}"'.format(page_parameter) , "code": 404 }
                , status_code=404
            )

        page = list_pages[0]

        return send_response({
            "page": page.get('page')
            , "counter": page.get('counter')
        })
        
    except Exception as error:
        logging.error(error)
        response_message = {
            'message': 'Something went wrong'
            , 'code': 500
        }
        return send_response(response_message, status_code=500)
