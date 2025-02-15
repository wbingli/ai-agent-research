import json
import boto3
import os
import uuid
from datetime import datetime
from typing import Dict, Any

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TASKS_TABLE_NAME', 'Tasks'))

def lambda_handler(event: Dict[Any, Any], context: Any) -> Dict[Any, Any]:
    """
    Lambda function handler for processing Bedrock Agent actions.

    Args:
        event: The Lambda event containing the action request
        context: Lambda context

    Returns:
        Dict containing the response
    """
    try:
        # Extract action information from the event
        action_group = event.get('actionGroup', '')
        action = event.get('action', '')
        api_path = event.get('apiPath', '')

        # Process create task request
        if action_group == 'TaskManagement' and action == 'createTask' and api_path == '/tasks':
            return create_task(event.get('requestBody', {}))

        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': f'Unsupported action: {action_group}/{action}'
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def create_task(request_body: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Create a new task in DynamoDB.

    Args:
        request_body: The request body containing task details

    Returns:
        Dict containing the created task information
    """
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    current_time = datetime.utcnow().isoformat()

    # Prepare task item
    task_item = {
        'task_id': task_id,
        'description': request_body.get('description'),
        'priority': request_body.get('priority', 'medium'),
        'deadline': request_body.get('deadline'),
        'status': 'created',
        'created_at': current_time
    }

    # Save to DynamoDB
    table.put_item(Item=task_item)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'task_id': task_id,
            'status': 'created',
            'created_at': current_time
        })
    }

def validate_request(request_body: Dict[Any, Any]) -> None:
    """
    Validate the request body for task creation.

    Args:
        request_body: The request body to validate

    Raises:
        ValueError: If validation fails
    """
    if not request_body.get('description'):
        raise ValueError("Task description is required")

    priority = request_body.get('priority', 'medium')
    if priority not in ['low', 'medium', 'high']:
        raise ValueError("Invalid priority value")

    deadline = request_body.get('deadline')
    if deadline:
        try:
            datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid deadline format. Use YYYY-MM-DD")
