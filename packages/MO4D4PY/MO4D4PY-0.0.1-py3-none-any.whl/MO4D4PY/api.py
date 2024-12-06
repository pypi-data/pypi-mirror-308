import requests
import json
from .exceptions import APIError, TimeoutError

class API:

    # Definición de un diccionario constante
    HCTYPE = {         
            'CodeAssist': 'application/json',
            'TechnicalDoc':'multipart/form-data, boundary = ----WebKitFormBoundarybGclqD44Hd3A1Nzr',
            'ExplainCode': 'application/json;charset=UTF-8',          
            'RefactorCode': 'application/json;charset=UTF-8',
            'CommentCode': 'application/json;charset=UTF-8',
            'UnitTest': 'application/json;charset=UTF-8',
            'CodeReview': 'application/json;charset=UTF-8',
            'Creatediagrams': 'multipart/form-data, boundary = ',
            'JmeterTest': 'multipart/form-data, boundary = ',
            'RestAPI': 'multipart/form-data, boundary = ',
            'Custom': 'multipart/form-data, boundary = ',
            'translator': 'multipart/form-data, boundary = ',
            'SEO': 'multipart/form-data, boundary = ',
            'mom': 'multipart/form-data, boundary = ',
            'mindmap': 'multipart/form-data, boundary = ',
            'kassist': 'multipart/form-data, boundary = ',
        }
    
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.endpoints = { 
            'CodeAssist': 'https://machineone4delivery.net/api/v1/codeassist/openai/codegen',
            'ExplainCode': 'https://machineone4delivery.net/api/v2/explain',
            'RefactorCode': 'https://machineone4delivery.net/api/v2/refactor',
            'CommentCode': 'https://machineone4delivery.net/api/v2/comments',
            'UnitTest': 'https://machineone4delivery.net/api/v2/unittest',
            'CodeReview': 'https://machineone4delivery.net/api/v2/codereview',
            'tools': 'https://machineone4delivery.net/api/v2/mo4d/openai/tools'
        }

        self.templates = { 
            'CodeAssist': 'CodeAssist',
            'TechnicalDoc':'tools',
            'ExplainCode': 'ExplainCode',
            'RefactorCode': 'RefactorCode',
            'CommentCode': 'CommentCode',
            'UnitTest': 'UnitTest',
            'CodeReview': 'CodeReview',
            'Creatediagrams': 'tools',
            'JmeterTest': 'tools',
            'RestAPI': 'tools',
            'Custom': 'tools',
            'translator': 'tools',
            'SEO': 'tools',
            'mom': 'tools',
            'mindmap': 'tools',
            'kassist': 'tools'
        }

    def request(self, template_name, payload, files=None, timeout=10):
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' does not exist.")
        
        endpoint = self.endpoints.get(self.templates[template_name])
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": f"{self.HCTYPE.get(template_name)}"
        }

        files=None
                
        payload_ajustado = self.ajustar_payload(template_name, payload)      

        #payload_ajustado

        try:
            response = requests.post( endpoint, headers= headers, json= payload_ajustado,  files=files,  timeout= timeout )
            response.raise_for_status()

        except requests.exceptions.HTTPError as http_err:
            raise APIError(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            raise APIError("Error de conexión")
        except requests.exceptions.Timeout:
            raise TimeoutError("La solicitud ha tardado demasiado")
        except requests.exceptions.RequestException as err:
            raise APIError(f"Error en la solicitud: {err}")
        
        return response.json()


    def ajustar_payload(self,template_name, payload ):
        # Definir los payloads esperados para cada template
        payloads_esperados = {
            'CodeAssist':   {'userPrompt': '', 'token': '', 'systemPrompt': '', 'temperature': 0.7 , 'provider': 'azure', 'message': '' },
            'TechnicalDoc': {'prompt': '', 'token': '','type': 'technical-documentation'},
            #'TechnicalDoc': {'prompt': '', 'token': '', 'language': '', 'type': 'technical-documentation', 'temperature': 0.7, 'provider': 'azure' },
            'ExplainCode':  {'code': '', 'token': '', 'provider': 'azure'},
            'RefactorCode': {'code': '', 'token': '', 'provider': 'azure'},
            'CommentCode':  {'code': '', 'token': '', 'provider': 'azure'},
            'UnitTest':     {'code': '', 'token': '', 'provider': 'azure'},
            'CodeReview':   {'code': '', 'token': '', 'provider': 'azure'},
            'Creatediagrams': {'prompt': '', 'token': '', 'language': '', 'type': 'PlantUML', 'temperature': 0.7, 'provider': 'azure' },
            'JmeterTest':     {'prompt': '', 'token': '', 'language': '', 'type': 'Jmeter', 'temperature': 0.7, 'provider': 'azure' },
            'RestAPI':        {'prompt': '', 'token': '', 'language': '', 'type': 'Rest-API-testing', 'temperature': 0.7, 'provider': 'azure' },
            'Custom':         {'prompt': '', 'token': '', 'language': '', 'type': 'custom', 'temperature': 0.7, 'provider': 'azure', 'message': ''},
            'translator':     {'prompt': '', 'token': '', 'language': '', 'type': 'Language-Translator', 'temperature': 0.7, 'provider': 'azure' },
            'SEO':            {'prompt': '', 'token': '', 'language': '', 'type': 'SEO', 'temperature': 0.7, 'provider': 'azure', 'message': ''},
            'mom':            {'prompt': '', 'token': '', 'language': '', 'type': 'mom', 'temperature': 0.7, 'provider': 'azure' },
            'mindmap':        {'prompt': '', 'token': '', 'language': '', 'type': 'mindmap', 'temperature': 0.7, 'provider': 'azure' },
            'kassist':        {'userPrompt': '', 'nowledgeId': '', 'token': '' }
        }

        msg = []
        msg.append(  {"role": "system", "content": ""}   )    
        msg.append( {"role": "user", "content": payload['prompt'] }  )    

        # Obtener el payload esperado para el template dado
        payload_base     = payloads_esperados.get(template_name)

        # si no hay base Error. Se da cuando no se ha informado correctamente el template
        if payload_base is None:
            raise ValueError(f"Template '{template_name}' no es válido.")
        
        #Poner el prompt y la api key a la base 
        for clave, valor in payload_base.items():
            if clave =='token':
               payload_base[ clave] =  self.api_key
            if clave == 'code' or  clave == 'userPrompt' or clave == 'prompt':
                payload_base[clave] =  payload['prompt']
            if clave == 'message':
                payload_base[clave] = msg
           
        for clave, valor in payload.items():
            if payload[clave] != "" and clave != 'prompt':
                payload_base[clave] = payload[clave]

        return  payload_base

