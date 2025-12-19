from django.conf import settings
from main.src.httperro.http_erro import HttpErrors
import requests




class Evolution():

    def __init__(self):
        self.__base_url = settings.EVOLUTION_API_URL
        self.__evolutionmasterkey = settings.EVOLUTIONMASTERKEY
    
    def instance_create(self, name):
        
        headers = {
            "apikey": f"{self.__evolutionmasterkey}"
        }

        json = {
            "instanceName": name,
            "integration": "WHATSAPP-BAILEYS" ,
            "groupsIgnore": False
        }
        
        response = requests.post(
            url=f"{self.__base_url}/instance/create",
            headers=headers,
            json=json
        )
        status_code = response.status_code
        if ((status_code >= 200) and (status_code <= 299)):
            data = {
                "status_code": response.status_code,
                "response": response.json()
            }
            return data
        else: 
            raise HttpErrors(
                message=response.json(), status_code=status_code
            )
            
    
    def instance_status(self, name, key):
        
        headers = {
            "apikey": f"{key}"
        }

        response = requests.get(
            url=f"{self.__base_url}/instance/connectionState/{name}",
            headers=headers,
        )
        data = {
            "status_code": response.status_code,
            "response": response.json()
        }
        return data
    

    def instance_connect(self, name, key):
        
        headers = {
            "apikey": f"{key}"
        }

        response = requests.get(
            url=f"{self.__base_url}/instance/connect/{name}",
            headers=headers,
        )

        data = {
            "status_code": response.status_code,
            "response": response.json()
        }
        return data
    
    def instance_desconect(self, name, key):
        
        headers = {
            "apikey": f"{key}"
        }

        response = requests.delete(
            url=f"{self.__base_url}/instance/logout/{name}",
            headers=headers,
        )

        data = {
            "status_code": response.status_code,
            "response": response.json()
        }
        return data
    
    def instance_delete(self, name, key):
        
        headers = {
            "apikey": f"{key}"
        }

        response = requests.delete(
            url=f"{self.__base_url}/instance/delete/{name}",
            headers=headers,
        )

        data = {
            "status_code": response.status_code,
            "response": response.json()
        }
        return data
    
    def instance_send_text(self, name, key, number, text):
        headers = {
            "apikey": f"{key}"
        }

        json =  {
            "number": f'{number}',
            "text": f"{text}"
        }
        

        response = requests.post(
            url=f"{self.__base_url}/message/sendText/{name}",
            headers=headers,
            json=json
        )
        status_code = response.status_code
        if ((status_code >= 200) and (status_code <= 299)):
            data = {
                "status_code": response.status_code,
                "response": response.json()
            }
            return data
        else: 
            raise HttpErrors(
                message=response.json(), status_code=status_code
            )
    
    def instance_send_media(self, name, key, number, text, media_url, tipo):
        try:
            headers = {
                "apikey": f"{key}"
            }

            json = {
                        "number": f"{number}",
                        "mediatype": f"{tipo}",
                        "caption": f"{text}",
                        "media": f"{media_url}"
            
                    }
                    
                    
            response = requests.post(
                url=f"{self.__base_url}/message/sendMedia/{name}",
                headers=headers,
                json=json,
                timeout=15
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
    
    def instance_create_group(self, name, key, nomedogrupo, participantes):
        try:
            headers = {
                "apikey": f"{key}"
            }
            json = {
                "subject": f"{nomedogrupo}",  
                "description": "optional",
                "participants": participantes
            }

            response = requests.post(
                    url=f"{self.__base_url}/group/create/{name}",
                    headers=headers,
                    json=json
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
    
    def instance_update_image_group(self, name, key,groupid,imageurl):

       
        try:
            signed_url = f"{imageurl}"
          
            headers = {
                "apikey": f"{key}"
            }
            json = {
                "image": f'{signed_url}'
            }

            response = requests.post(
                    url=f"{self.__base_url}/group/updateGroupPicture/{name}?groupJid={groupid}",
                    headers=headers,
                    json=json
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
    
    def instance_update_subject_group(self, name, key,groupid,groupname):

        try:
            
            headers = {
                "apikey": f"{key}"
            }
            json = {
                "subject": f"{groupname}"
                }

            response = requests.post(
                    url=f"{self.__base_url}/group/updateGroupSubject/{name}?groupJid={groupid}",
                    headers=headers,
                    json=json
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
    
    def instance_update_description_group(self, name, key,groupid,description):

        try:
            
          
            headers = {
                "apikey": f"{key}"
            }

            json = {
            "description": f"{description}"
            }

            response = requests.post(
                    url=f"{self.__base_url}/group/updateGroupDescription/{name}?groupJid={groupid}",
                    headers=headers,
                    json=json
                )
            print (response.text)
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
    
    def instance_get_invite_group(self, name, key, groupid):
        try:
            headers = {
                "apikey": f"{key}"
            }

            response = requests.get(
                    url=f"{self.__base_url}/group/inviteCode/{name}?groupJid={groupid}",
                    headers=headers,
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
        
    
    def instance_send_invite_group(self, name, key, groupid):
        try:
            headers = {
                "apikey": f"{key}"
            }

            json = {
                "subject": f"{groupid}",  
                "description": "Acesse esse link para participar do grupo",
                "numbers": [f'{groupid}']
            }

            response = requests.post(
                    url=f"{self.__base_url}/group/sendInvite/{name}?groupJid={groupid}",
                    headers=headers,
                    json=json
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
        
    def instance_get_group(self, name, key):
        try:
            headers = {
                "apikey": f"{key}"
            }

            response = requests.get(
                    url=f"{self.__base_url}/group/fetchAllGroups/{name}?getParticipants=false",
                    headers=headers,
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
    
