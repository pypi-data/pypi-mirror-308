from .exceptions import CredentialsError, ParamsError, InternalScodError
from requests import Response
from typing import Dict

class Validators:
    def __response_validator(self, response: Dict[str, str]) -> Response:
        data = response.json()
        exceptions = {400: ParamsError, 403: CredentialsError, 500: InternalScodError}
        if response.status_code in exceptions:
            if any(key in data for key in ["erro", "error"]):
                raise exceptions[response.status_code](data["mensagem"])

        return data
