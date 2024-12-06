from typing import Union, List, Dict
from .validators import Validators
import requests


class Client(Validators):
    def get_allowed_cities(self) -> Union[List[Dict[str, str]], List[None]]:
        response = requests.get("https://api.scod.com.br/v3/cliente/listar/cidades_contratadas",
                                headers=self._Scod__headers)

        data = self._Validators__response_validator(response)
        if 'erro' in data and data['erro']:
            return data['mensagem']

        return data
