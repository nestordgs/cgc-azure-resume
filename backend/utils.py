import json
import azure.functions as func

def send_response(message, **kwargs):

    if kwargs.get('is_json') is False:
        response = message
    else:
        response = json.dumps(message)

    return func.HttpResponse(response, status_code=kwargs.get('status_code', 200), mimetype='application/json')