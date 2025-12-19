from django.conf import settings
import requests
from main.src.httperro.http_erro import HttpErrors



class IXC():

    def __init__(self):
        self.__base_url = settings.IXC_API_URL
        self.__ixckey = settings.IXCKEY
    
    def get_contratos(self, contratoid):
        try:
            headers = {
                'ixcsoft': 'listar',
                'Content-Type': 'application/json',
                'Authorization': F'Basic {self.__ixckey}',
            }

            json_data = {
                'qtype': 'cliente_contrato.id',
                'query': f'{contratoid}',
                'oper': '=',
                'page': '1',
                'rp': '1',
                'sortname': 'cliente_contrato.id',
                'sortorder': 'asc',
            }


            response = requests.get(
                url=f'{self.__base_url}/webservice/v1/cliente_contrato',
                headers=headers,
                json=json_data
            )
    
            response.raise_for_status() 
                        
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
               
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)

      