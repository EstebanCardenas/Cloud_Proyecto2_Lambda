import json, boto3, uuid
from datetime import datetime as dt

# vars
db = boto3.resource('dynamodb')
lista = db.Table('ListaNegra')

# aux func
def in_db(email: str) -> bool:
    res = lista.get_item(Key={
        'Email': email
    })
    try:
        res['Item']
        return True
    except:
        return False

# aux func
def lambda_handler(event, context):
    # Validación
    try:  # Tomar body
        body = json.loads(event.get('body'))
        email = body['email']
        app_id = body['app_id']
        motivo = body['motivo']
    except Exception as e:
        return {
            'statusCode': 400,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                'error': 'body incompatible'   
            })
        }
    try:  # Formato uuid
        uuid.UUID(app_id)
    except:
        return {
            'statusCode': 403,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                'error': 'el id de la aplicacion no tiene formato uuid'
            })
        }
    if in_db(email):
        return {
            'statusCode': 403,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                'error': 'el email ya esta en la lista negra'
            })
        }
        
    # Agregar
    res = lista.put_item(
        Item={
            'Email': email,
            'AppId': app_id,
            'Motivo': motivo[:255],
            'IP': event['requestContext']['identity']['sourceIp'],
            "Fecha/Hora": str(dt.now())
        }
    )
    return {
        'statusCode': 201,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(str(res))
    }
