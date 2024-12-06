from typing import Union, List, Dict
from .validators import Validators
import requests

class Property(Validators):

    def get_denial_license(self, id: str) -> Union[List[Dict[str, str]], List[None]]:
        response = requests.get(f"https://api.scod.com.br/v3/imovel/certidao/{id}",
                                headers=self._Scod__headers)

        data = self._Validators__response_validator(response)
        if 'erro' in data and data['erro']:
            return data['mensagem']

        return data

    def get_properties(self, page: int) -> Union[List[Dict[str, str]], List[None]]:

        response = requests.get("https://api.scod.com.br/v3/imovel/listar/imoveis",
                                headers=self._Scod__headers, params={"pagina": page})

        data = self._Validators__response_validator(response)
        return data

    def get_property_info(self, id: str) -> Union[List[Dict[str, str]], List[None]]:
        response = requests.get(f"https://api.scod.com.br/v3/imovel/iptu/dados/{id}",
                                headers=self._Scod__headers)

        data = self._Validators__response_validator(response)

        if 'error' in data and data['error']:
            return data['mensagem']

        return data

    def get_debt_file(self, property_id: str, debt_id: str, timeout=30) -> Union[List[Dict[str, str]], List[None]]:
        response = requests.post(f"https://api.scod.com.br/v3/imovel/iptu/boleto/{property_id}",
                                headers=self._Scod__headers, json=[debt_id], timeout=timeout)

        data = self._Validators__response_validator(response)

        if 'error' in data and data['error']:
            return data['mensagem']

        return data
