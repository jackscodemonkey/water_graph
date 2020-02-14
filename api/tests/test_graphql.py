import pytest
from water_graph.schema import schema
import graphene
import graphql_jwt.testcases
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, AnonymousUser

@pytest.mark.django_db(transaction=True)
class TestCustomer(graphql_jwt.testcases.JSONWebTokenTestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(username='test')

        permission_view = Permission.objects.get(name='Can view customer')
        permission_add = Permission.objects.get(name='Can add customer')
        permission_update = Permission.objects.get(name='Can change customer')
        permission_delete = Permission.objects.get(name='Can delete customer')
        self.user.user_permissions.add(permission_add)
        self.user.user_permissions.add(permission_view)
        self.user.user_permissions.add(permission_update)
        self.user.user_permissions.add(permission_delete)

        self.client = graphql_jwt.testcases.JSONWebTokenClient()
        self.client.authenticate(self.user)

    #region Authenticated Customer Tests
    def test_createCustomer(self):
        query = """
            mutation {
            customerCreate(input: {firstName: "Dave", lastName: "Backster"}) {
                customer {
                id
                firstName
                lastName
                }
            }
            }
        """
        result = self.client.execute(query)
        assert result.errors is None

    def test_readCustomer(self):

        query = """
            query{
            customerRead(firstName:"Joe"){
                edges{
                node{
                    id,
                    firstName,
                    lastName
                }
                }
            }
            }
            """

        result = self.client.execute(query)
        assert result.errors is None
        assert result.data['customerRead']['edges'][0]['node']['firstName'] == 'Joe'

    def test_updateCustomer(self):
        query_read = """
            query{
            customerRead(firstName:"Joe"){
                edges{
                node{
                    id,
                    firstName,
                    lastName
                }
                }
            }
            }
            """
        read_result = self.client.execute(query_read)
        if read_result.errors is None:
            id = read_result.data['customerRead']['edges'][0]['node']['id']
            firstname = read_result.data['customerRead']['edges'][0]['node']['firstName']

        variables={"input":{
                        'id': id,
                        'firstName': firstname,
                        'lastName':"Smiths"
                        }
        }

        if variables['input']['id'] is not None:
            query_update = """
                mutation CustomerUpdate($input: CustomerUpdateInput!){
                    customerUpdate(input: $input) {
                        customer {
                        id
                        firstName
                        lastName
                        }
                    }
                }
            """
        update_result = self.client.execute(query_update, variables)
        assert update_result.errors is None
        assert update_result.data['customerUpdate']['customer']['lastName'] == "Smiths"

    def test_deleteCustomer(self):
        query_read = """
            query{
            customerRead(firstName:"Joe"){
                edges{
                node{
                    id,
                    firstName,
                    lastName
                }
                }
            }
            }
            """
        read_result = self.client.execute(query_read)
        if read_result.errors is None:
            id = read_result.data['customerRead']['edges'][0]['node']['id']

        variables={"input":{
                        'id': id,
                        }
        }

        assert variables['input']['id'] is not None

        if variables['input']['id'] is not None:
            query_update = """
                mutation CustomerDelete($input: CustomerDeleteInput!){
                customerDelete(input: $input) {
                    customer {
                    id
                    }
                }
                }
            """
        update_result = self.client.execute(query_update, variables)
        assert update_result.errors is None
    #endregion Authenticated Customer Tests

class TestMeterType(graphql_jwt.testcases.JSONWebTokenTestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(username='test')

        permission_view = Permission.objects.get(name='Can view meter type')
        permission_add = Permission.objects.get(name='Can add meter type')
        permission_update = Permission.objects.get(name='Can change meter type')
        permission_delete = Permission.objects.get(name='Can delete meter type')
        self.user.user_permissions.add(permission_add)
        self.user.user_permissions.add(permission_view)
        self.user.user_permissions.add(permission_update)
        self.user.user_permissions.add(permission_delete)

        self.client = graphql_jwt.testcases.JSONWebTokenClient()
        self.client.authenticate(self.user)

    #region Authenticated Meter Type Tests
    def test_createMeterType(self):
        query = """
            mutation($input:MeterTypeCreateInput!){
            metertypeCreate(input:$input){
                clientMutationId
            }
            }
        """

        variables ={
        "input": {
            "meterModel":"WET1000",
            "meterVendor": "Ztron"
            }
        }
        result = self.client.execute(query, variables=variables)
        assert result.errors is None

    def test_readMeterType(self):
            query = """
                query MeterTypeRead($meterModel: String!){
                    metertypeRead(meterModel: $meterModel){
                        edges{
                        node{
                            id
                            meterModel
                            meterVendor
                        }
                        }
                    }
                }
                """

            variables = {
                "meterModel": "C234KI"
            }

            result = self.client.execute(query, variables)
            assert result.errors is None
            assert result.data['metertypeRead']['edges'][0]['node']['meterVendor'] == 'WaterFlow'

    def test_updateMeterType(self):
        query_read = """
            query MeterTypeRead($meterModel: String!){
                metertypeRead(meterModel: $meterModel){
                    edges{
                    node{
                        id
                        meterModel
                        meterVendor
                    }
                    }
                }
            }
            """
        variables = {
            "meterModel": "C234KI"
        }

        result = self.client.execute(query_read, variables)
        id = result.data['metertypeRead']['edges'][0]['node']['id']

        query = """
            mutation($input:MeterTypeUpdateInput!){
            metertypeUpdate(input:$input){
                clientMutationId
                metertype{
                    id
                    meterModel
                    meterVendor
                    }
                }
            }
        """

        variables ={
        "input": {
            "id": id,
            "meterModel":"C234KI",
            "meterVendor": "Ztron"
            }
        }
        result = self.client.execute(query, variables=variables)
        assert result.errors is None

    def test_deleteMeterType(self):
        query_read = """
            query MeterTypeRead($meterModel: String!){
                metertypeRead(meterModel: $meterModel){
                    edges{
                    node{
                        id
                        meterModel
                        meterVendor
                    }
                    }
                }
            }
            """
        variables = {
            "meterModel": "C234KI"
        }

        result = self.client.execute(query_read, variables)
        id = result.data['metertypeRead']['edges'][0]['node']['id']

        variables={"input":
            {
            'id': id,
            }
        }

        assert variables['input']['id'] is not None

        if variables['input']['id'] is not None:
            query_delete = """
                mutation MeterTypeDelete($input: MeterTypeDeleteInput!){
                metertypeDelete(input: $input) {
                    metertype {
                    id
                    }
                }
                }
            """
        delete_result = self.client.execute(query_delete, variables)
        assert delete_result.errors is None

    #endregion Authenticated Meter Type Tests