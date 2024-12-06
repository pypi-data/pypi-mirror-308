from unittest import TestCase

from kg_core.response import ResponseObjectConstructor, UserWithRoles, User, SpaceInformation


class TestResponseObjectConstructor(TestCase):
    def test_init_response_object(self):
        response = ResponseObjectConstructor.init_response_object(SpaceInformation, {'http://schema.org/identifier': 'collab-an-adaptive-generalized-leaky-integrate', 'http://schema.org/name': 'collab-an-adaptive-generalized-leaky-integrate', 'https://core.kg.ebrains.eu/vocab/meta/space/autorelease': False, 'https://core.kg.ebrains.eu/vocab/meta/space/clientSpace': False, 'https://core.kg.ebrains.eu/vocab/meta/space/deferCache': False}, "https://kg.ebrains.eu/api/instances/")
        self.fail()
