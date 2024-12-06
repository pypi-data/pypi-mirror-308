from typing import Optional, List, Dict

import requests

from config import get_api_key
from pin_payments.base import Base


class Plans(Base):
    """
    The Plans API allows you to create, modify, and examine recurring billing plans.
    """

    def __init__(
            self,
            api_key: str,
            mode: str = 'live'
    ):
        super().__init__(api_key=api_key, mode=mode)
        self._base_url += 'plans/'

    def create(
            self,
            name: str,
            amount: int,
            interval: int,
            interval_unit: str,
            currency: str = 'AUD',
            intervals: Optional[int] = 0,
            setup_amount: Optional[int] = 0,
            trial_amount: Optional[int] = 0,
            trial_interval: Optional[int] = 0,
            trial_interval_unit: Optional[str] = '',
            customer_permissions: Optional[List[str]] = None
    ) -> Dict:
        """
        Creates a new plan and returns its details.
        """
        if customer_permissions is None:
            customer_permissions = ["cancel"]
        data = {
            'name': name,
            'amount': amount,
            'currency': currency,
            'interval': interval,
            'interval_unit': interval_unit,
            'intervals': intervals,
            'setup_amount': setup_amount,
            'trial_amount': trial_amount,
            'trial_interval': trial_interval,
            'trial_interval_unit': trial_interval_unit,
            'customer_permissions': customer_permissions
        }

        response = requests.post(self._base_url, auth=self._auth, data=data)
        return self._handle_response(
            response,
            'Plans.create',
            201
        )

    def list(self) -> Dict:
        """
        Returns a paginated list of all plans.
        """
        response = requests.get(self._base_url, auth=self._auth)
        return self._handle_response(
            response,
            'Plans.list',
            200
        )

    def details(self, plan_token: str) -> Dict:
        """
        Returns the details of a specified plan.
        """
        url = f"{self._base_url}{plan_token}"
        response = requests.get(url, auth=self._auth)
        return self._handle_response(
            response,
            'Plans.details',
            200
        )

    def update(
            self,
            plan_token: str,
            name: Optional[str] = None,
            customer_permissions: Optional[List[str]] = None
    ) -> Dict:
        """
        Update the specified plan.
        """
        url = f"{self._base_url}{plan_token}"
        data = {}
        if name is not None:
            data['name'] = name
        if customer_permissions is not None:
            data['customer_permissions'] = customer_permissions

        response = requests.put(url, auth=self._auth, data=data)
        return self._handle_response(
            response,
            'Plans.update',
            200
        )

    def delete(self, plan_token: str) -> Dict:
        """
        Deletes a plan and all of its subscriptions.
        """
        url = f"{self._base_url}{plan_token}"
        response = requests.delete(url, auth=self._auth)
        return self._handle_response(
            response,
            'Plans.delete',
            204
        )

    def create_subscription(
            self,
            plan_token: str,
            customer_token: str,
            card_token: Optional[str] = None,
            include_setup_fee: Optional[bool] = True
    ) -> Dict:
        """
        Creates a new subscription to the specified plan.
        """
        url = f"{self._base_url}{plan_token}/subscriptions"
        data = {
            'customer_token': customer_token,
            'include_setup_fee': include_setup_fee
        }
        if card_token is not None:
            data['card_token'] = card_token

        response = requests.post(url, auth=self._auth, data=data)
        return self._handle_response(
            response,
            'Plans.create_subscription',
            200
        )

    def list_subscriptions(self, plan_token: str) -> Dict:
        """
        Returns a paginated list of subscriptions for a plan.
        """
        url = f"{self._base_url}{plan_token}/subscriptions"
        response = requests.get(url, auth=self._auth)
        return self._handle_response(
            response,
            'Plans.list_subscriptions',
            200
        )


if __name__ == '__main__':
    plans_api = Plans(api_key=get_api_key(), mode='test')

    create_response = plans_api.create(
        name='Monthly Subscription',
        amount=1000,
        interval=1,
        interval_unit='month',
        currency='AUD',
        intervals=12,
        setup_amount=500,
        trial_amount=0,
        trial_interval=1,
        trial_interval_unit='month',
        customer_permissions=["update", "cancel"]
    )
    print("Create Plan Response:", create_response)
    plan_token = create_response['response']['token']

    list_response = plans_api.list()
    print("List Plans Response:", list_response)

    details_response = plans_api.details(plan_token=plan_token)
    print("Plan Details Response:", details_response)

    update_response = plans_api.update(
        plan_token=plan_token,
        name='Updated Monthly Subscription',
        customer_permissions=["cancel"]
    )
    print("Update Plan Response:", update_response)

    customer_token = 'example-customer-token'
    card_token = 'example-card-token'
    subscription_response = plans_api.create_subscription(
        plan_token=plan_token,
        customer_token=customer_token,
        card_token=card_token,
        include_setup_fee=True
    )
    print("Create Subscription Response:", subscription_response)

    list_subscriptions_response = plans_api.list_subscriptions(plan_token=plan_token)
    print("List Subscriptions Response:", list_subscriptions_response)

    delete_response = plans_api.delete(plan_token=plan_token)
    print("Delete Plan Response:", delete_response)
