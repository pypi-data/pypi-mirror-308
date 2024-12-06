from typing import Union, List, Dict
import requests


class Group:
    def get_groups(self) -> Union[List[Dict[str, str]], List[None]]:
        response = requests.get("https://api.scod.com.br/v3/imovel/listar/grupos",
                                headers=self.__headers)

        data = self.__response_validator(response)
        if 'erro' in data and data['erro']:
            return data['mensagem']

        return data
