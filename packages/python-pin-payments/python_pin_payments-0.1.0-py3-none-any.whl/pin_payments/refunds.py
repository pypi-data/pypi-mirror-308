from typing import Optional

import requests

from config import get_api_key
from pin_payments.base import Base


class Refunds(Base):
    """
    The refunds API allows you to refund charges and retrieve the details of previous refunds.
    """

    def __init__(
            self,
            api_key: str,
            mode: str = 'live'
    ):
        super().__init__(api_key=api_key, mode=mode)

    def list(
            self
    ) -> dict:
        """
        Returns a paginated list of all refunds.

        GET /refunds

        Example:
        curl https://test-api.pinpayments.com/1/refunds -u your-secret-api-key:

        :return: None
        """
        url = f"{self._base_url}refunds/"
        response = requests.get(url, auth=self._auth)

        return self._handle_response(
            response=response,
            function_name='Refunds.list',
            required_status_code=200
        )

    def details(
            self,
            refund_token: str
    ) -> dict:
        """
        Returns the details of the specified refund.

        GET /refunds/refund-token

        Example:
        curl https://test-api.pinpayments.com/1/refunds/rf_ERCQy--Ay6o-NKGiUVcKKA -u your-secret-api-key: -X GET

        :param refund_token: Refund Token
        :return: None
        """
        url = f"{self._base_url}refunds/{refund_token}"
        response = requests.get(url, auth=self._auth)

        return self._handle_response(
            response=response,
            function_name='Refunds.details',
            required_status_code=200
        )

    def create_refund(
            self,
            charge_token: str,
            amount: Optional[int] = None
    ) -> dict:
        """
        Creates a new refund and returns its details.

        POST /charges/charge-token/refunds

        Example:
        curl https://test-api.pinpayments.com/1/charges/ch_bZ3RhJnIUZ8HhfvH8CCvfA/refunds
        -u your-secret-api-key: -X POST

        :param charge_token: Charge Token
        :param amount: The amount to refund in the currency’s base unit
        (e.g. cents for AUD, yen for JPY). Default value is the full amount of the charge.
        :return: None
        """
        url = f"{self._base_url}charges/{charge_token}/refunds"
        data = {}

        if amount is not None:
            data['amount'] = amount

        response = requests.post(url, auth=self._auth, data=data)

        return self._handle_response(
            response=response,
            function_name='Refunds.create_refund',
            required_status_code=201
        )

    def list_charge(
            self,
            charge_token: str
    ) -> dict:
        """
        Returns a list of all refunds for the specified charge.

        GET /charges/charge-token/refunds

        Example:
        curl https://test-api.pinpayments.com/1/charges/ch_bZ3RhJnIUZ8HhfvH8CCvfA/refunds -u your-secret-api-key:

        :param charge_token: Charge Token
        :return: None
        """
        url = f"{self._base_url}charges/{charge_token}/refunds"
        response = requests.get(url, auth=self._auth)

        return self._handle_response(
            response=response,
            function_name='Refunds.list_charge',
            required_status_code=200
        )


if __name__ == '__main__':
    refunds_api = Refunds(api_key=get_api_key(), mode="test")

    all_refunds = refunds_api.list()
    print("All Refunds:", all_refunds)

    refund_token = 'refund_token_example'
    refund_details = refunds_api.details(refund_token=refund_token)
    print(f"Details of Refund {refund_token}:", refund_details)

    charge_token_for_refund = "your_charge_token"
    refund_amount = 100

    refund_creation_result = refunds_api.create_refund(charge_token=charge_token_for_refund, amount=refund_amount)
    print("Refund Creation Result:", refund_creation_result)

    refunds_for_charge = refunds_api.list_charge(charge_token=charge_token_for_refund)
    print(f"All Refunds for Charge {charge_token_for_refund}:", refunds_for_charge)
