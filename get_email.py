import json, boto3

# vars
db = boto3.resource('dynamodb')
lista = db.Table('ListaNegra')

# aux func
def lambda_handler(event, context):
    stringParameter = event.get('queryStringParameters')
    email = stringParameter.get('email') if stringParameter != None else None
    if email == '' or email == None:
        return {
            'statusCode': 400,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                'msg': 'El email es obligatorio'
            })
        }
    res = lista.get_item(Key={
        'Email': email
    })
    try:
        res['Item']
        return {
            'statusCode': 200,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                'msg': 'true'
            })
        }
    except:
        return {
            'statusCode': 200,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                'msg': 'false'
            })
        }
