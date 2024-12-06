from unittest import TestCase

from kg_core.response import ResponseObjectConstructor, UserWithRoles, User


class TestResponseObjectConstructor(TestCase):
    def test_init_response_object(self):
        response = ResponseObjectConstructor.init_response_object(User, {"name": "Oli"}, "http://test")
        self.fail()
