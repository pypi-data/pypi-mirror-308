from typing import Union, List, Dict
from .validators import Validators
import requests

class Profile(Validators):
    def get_access_profile(self, id: str = '') -> Union[List[Dict[str, str]], List[None]]:
        response = requests.get(f"https://api.scod.com.br/v3/perfil/{id}",
                                headers=self._Scod__headers)
        data = self._Validators__response_validator(response)
        if 'erro' in data and data['erro']:
            return data['mensagem']

        return data
