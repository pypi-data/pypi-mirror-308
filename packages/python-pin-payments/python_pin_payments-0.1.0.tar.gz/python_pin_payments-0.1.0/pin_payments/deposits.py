import requests

from config import get_api_key
from pin_payments.base import Base


class Deposits(Base):
    """
    The Deposits API allows you to retrieve details of deposits made to your account.
    """

    def __init__(self, api_key: str, mode: str = 'live'):
        super().__init__(api_key=api_key, mode=mode)
        self._base_url += 'deposits/'

    def list(self) -> dict:
        """
        Returns a paginated list of all deposits.

        GET /deposits

        :return: dict
        """
        response = requests.get(self._base_url, auth=self._auth)
        return self._handle_response(
            response,
            'Deposits.list',
            200
        )

    def details(self, deposit_token: str) -> dict:
        """
        Returns the details of a deposit.

        GET /deposits/deposit-token

        :param deposit_token: The token of the deposit.
        :return: dict
        """
        url = f"{self._base_url}{deposit_token}"
        response = requests.get(url, auth=self._auth)
        return self._handle_response(
            response,
            'Deposits.details',
            200
        )


if __name__ == '__main__':
    deposits_api = Deposits(api_key=get_api_key(), mode='test')

    deposits_list_response = deposits_api.list()
    print("List of Deposits Response:", deposits_list_response)

    deposit_token = 'example-deposit-token'

    deposit_details_response = deposits_api.details(deposit_token=deposit_token)
    print("Deposit Details Response:", deposit_details_response)
