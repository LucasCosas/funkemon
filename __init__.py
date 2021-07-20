import logging
from azure.storage.blob import BlobServiceClient
import requests
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    

    file_path = req.headers.get('file_path')
    file_name = req.headers.get('file_name')


    if not file_name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            file_name = req_body.get('file_name')
            file_path = req_body.get('file_path')

    if file_name:
        try:

            STORAGEACCOUNTURL= 'https://tripdemosa.blob.core.windows.net/'
            STORAGEACCOUNTKEY= ''
            #LOCALFILENAME= 'temp_file.json'
            CONTAINERNAME = file_path.split('/')[0]
            BLOBNAME = file_path.split('/')[1] + '/' + file_name
            
            
            
            #download from blob
            blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)
            blob_client_instance = blob_service_client_instance.get_blob_client(CONTAINERNAME, BLOBNAME, snapshot=None)
            #with open(LOCALFILENAME, "wb") as my_blob:
            

            
            logging.info('downloading blob')
            
            blob_data = blob_client_instance.download_blob()
            data_final = blob_data.readall()
            
           

            logging.info('blob downloaded')

            # LOCALFILE is the file path
            dataframe_blobdata = json.loads(data_final)
            pokemon_name = dataframe_blobdata['pokemon']['pokemon_name']
            
            logging.info('creating URL')

            url = "https://pokeapi.co/api/v2/pokemon/" + pokemon_name.lower()
            
            x = requests.get(url)
            js = json.loads(x.content)
            output = js["abilities"][0]

            
            return func.HttpResponse(
                json.dumps(output),
                mimetype="application/json",
                status_code=200
            )
        
            
            
        except Exception as e:
            return func.HttpResponse(
                e.message,
                status_code=200
            )

            
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
