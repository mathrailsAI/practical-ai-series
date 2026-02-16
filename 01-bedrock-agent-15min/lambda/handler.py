import json
import urllib3
import os

http = urllib3.PoolManager()

def lambda_handler(event, context):
    """
    Handles API calls from Bedrock Agent and forwards them to your API server.
    """
    print(f"Received event: {json.dumps(event)}")

    # Extract information from the agent event
    api_path = event.get('apiPath', '')
    http_method = event.get('httpMethod', 'GET')
    parameters = event.get('parameters', [])

    # Build the full API URL
    api_base_url = os.environ.get('API_BASE_URL', 'https://jsonplaceholder.typicode.com/')
    full_url = f"{api_base_url}{api_path}"

    # Build query parameters
    query_params = {}
    for param in parameters:
        param_name = param.get('name')
        param_value = param.get('value')
        if param_name and param_value:
            query_params[param_name] = param_value

    # Add query params to URL
    if query_params:
        query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
        full_url = f"{full_url}?{query_string}"

    try:
        # Make the API call
        response = http.request(http_method, full_url)
        response_data = json.loads(response.data.decode('utf-8'))

        # Return in Bedrock Agent format
        return {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': event.get('actionGroup', ''),
                'apiPath': api_path,
                'httpMethod': http_method,
                'httpStatusCode': response.status,
                'responseBody': {
                    'application/json': {
                        'body': json.dumps(response_data)
                    }
                }
            }
        }

    except Exception as e:
        print(f"Error calling API: {str(e)}")
        return {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': event.get('actionGroup', ''),
                'apiPath': api_path,
                'httpMethod': http_method,
                'httpStatusCode': 500,
                'responseBody': {
                    'application/json': {
                        'body': json.dumps({'error': str(e)})
                    }
                }
            }
        }