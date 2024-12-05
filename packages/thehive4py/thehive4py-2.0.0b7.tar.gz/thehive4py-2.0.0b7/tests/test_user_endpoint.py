from typing import List

import pytest

from tests.utils import TestConfig
from thehive4py.client import TheHiveApi
from thehive4py.errors import TheHiveError
from thehive4py.query.filters import Eq
from thehive4py.types.user import InputUpdateUser, InputUserOrganisation, OutputUser


class TestUserEndpoint:
    def test_get_current(self, thehive: TheHiveApi):
        # TODO: implement a better control for user checking
        current_user = thehive.user.get_current()
        assert current_user["login"] == "admin@thehive.local"

    def test_create_and_get(self, thehive: TheHiveApi):
        created_user = thehive.user.create(
            user={"login": "bailando@sin.ti", "name": "Bailando", "profile": "analyst"}
        )
        created_user_2 = thehive.user.create(
            user={"login": "bailando@sin.ti", "name": "Bailando", "profile": "analyst"}
        )

        assert created_user == created_user_2

        fetched_user = thehive.user.get(created_user["_id"])
        assert created_user == fetched_user

    def test_update(
        self, test_config: TestConfig, thehive: TheHiveApi, test_user: OutputUser
    ):
        user_id = test_user["_id"]
        update_fields: InputUpdateUser = {
            "name": "Updated user",
            "profile": "read-only",
            "email": "whatever@example.com",
            "organisation": test_config.main_org,
        }
        thehive.user.update(user_id=user_id, fields=update_fields)
        updated_user = thehive.user.get(user_id=user_id)

        for field in update_fields:
            assert updated_user.get(field) == update_fields.get(field)

    def test_lock_and_unlock(self, thehive: TheHiveApi, test_user: OutputUser):
        user_id = test_user["_id"]

        thehive.user.lock(user_id=user_id)
        locked_user = thehive.user.get(user_id=user_id)
        assert locked_user["locked"] is True

        thehive.user.unlock(user_id=user_id)
        unlocked_user = thehive.user.get(user_id=user_id)
        assert unlocked_user["locked"] is False

    def test_delete(self, thehive: TheHiveApi, test_user: OutputUser):
        user_id = test_user["_id"]
        thehive.user.delete(user_id=user_id, organisation=test_user["organisation"])
        with pytest.raises(TheHiveError):
            thehive.user.get(user_id=user_id)

    @pytest.mark.skip(reason="integrator container only supports a single org ")
    def test_set_organisations(
        self, test_config: TestConfig, thehive: TheHiveApi, test_user: OutputUser
    ):
        organisations: List[InputUserOrganisation] = [
            {
                "default": True,
                "organisation": test_user["organisation"],
                "profile": "analyst",
            },
            {
                "default": False,
                "organisation": test_config.share_org,
                "profile": "read-only",
            },
        ]
        user_organisations = thehive.user.set_organisations(
            user_id=test_user["_id"], organisations=organisations
        )
        assert organisations == user_organisations

    def test_set_password(self, thehive: TheHiveApi, test_user: OutputUser):
        assert test_user["hasPassword"] is False
        user_id = test_user["_id"]

        password = "super-secruht!"
        thehive.user.set_password(user_id=user_id, password=password)

        user_with_password = thehive.user.get(user_id=user_id)
        assert user_with_password["hasPassword"] is True

    def test_renew_get_and_remove_apikey(
        self, thehive: TheHiveApi, test_user: OutputUser
    ):
        assert test_user["hasKey"] is False
        user_id = test_user["_id"]

        thehive.user.renew_apikey(user_id=user_id)
        assert isinstance(thehive.user.get_apikey(user_id=user_id), str)
        user_with_apikey = thehive.user.get(user_id=user_id)
        assert user_with_apikey["hasKey"] is True

        thehive.user.remove_apikey(user_id=user_id)
        user_without_apikey = thehive.user.get(user_id=user_id)
        assert user_without_apikey["hasKey"] is False

    def test_find_and_count(self, thehive: TheHiveApi, test_user: OutputUser):
        user_filters = Eq("login", test_user["login"])
        found_users = thehive.user.find(filters=user_filters)
        user_count = thehive.user.count(filters=user_filters)

        assert [test_user] == found_users
        assert len(found_users) == user_count
