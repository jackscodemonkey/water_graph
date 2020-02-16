import pytest
from water_graph.schema import schema
import graphene
import graphql_jwt.testcases
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, AnonymousUser


@pytest.mark.django_db(transaction=True)
class TestCustomer(graphql_jwt.testcases.JSONWebTokenTestCase):
    """ Customer End Point Tests"""

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

    # region Authenticated Customer Tests
    def test_create_customer(self):
        """ Test createing a customer """

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

    def test_read_customer(self):
        """ Test searching and reading a customer record."""

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

    def test_update_customer(self):
        """ Test updating a customer record. """

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

        variables = {"input": {
            'id': id,
            'firstName': firstname,
            'lastName': "Smiths"
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

    def test_delete_customer(self):
        """ Test deleting a customer record. """

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

        variables = {"input": {
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
    # endregion Authenticated Customer Tests


class TestMeterType(graphql_jwt.testcases.JSONWebTokenTestCase):
    """ Meter Type End Point Tests"""

    def setUp(self):

        self.user = get_user_model().objects.create(username='test')

        permission_view = Permission.objects.get(name='Can view meter type')
        permission_add = Permission.objects.get(name='Can add meter type')
        permission_update = Permission.objects.get(
            name='Can change meter type')
        permission_delete = Permission.objects.get(
            name='Can delete meter type')
        self.user.user_permissions.add(permission_add)
        self.user.user_permissions.add(permission_view)
        self.user.user_permissions.add(permission_update)
        self.user.user_permissions.add(permission_delete)

        self.client = graphql_jwt.testcases.JSONWebTokenClient()
        self.client.authenticate(self.user)

    # region Authenticated Meter Type Tests
    def test_create_meter_type(self):
        """ Test creating a meter type. """

        query = """
            mutation($input:MeterTypeCreateInput!){
            metertypeCreate(input:$input){
                clientMutationId
            }
            }
        """

        variables = {
            "input": {
                "meterModel": "WET1000",
                "meterVendor": "Ztron"
            }
        }
        result = self.client.execute(query, variables=variables)
        assert result.errors is None

    def test_read_meter_type(self):
        """ Test searhing and reading a meter type. """

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

    def test_update_meter_type(self):
        """ Test updating a meter type. """

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

        variables = {
            "input": {
                "id": id,
                "meterModel": "C234KI",
                "meterVendor": "Ztron"
            }
        }
        result = self.client.execute(query, variables=variables)
        assert result.errors is None

    def test_delete_meter_type(self):
        """ Test deleting a meter type. """

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

        variables = {"input":
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

    # endregion Authenticated Meter Type Tests


class TestMeter(graphql_jwt.testcases.JSONWebTokenTestCase):
        """ Meter End Point Tests"""

    def setUp(self):

        self.user = get_user_model().objects.create(username='test')

        permission_view = Permission.objects.get(name='Can view meter')
        permission_add = Permission.objects.get(name='Can add meter')
        permission_update = Permission.objects.get(name='Can change meter')
        permission_delete = Permission.objects.get(name='Can delete meter')
        self.user.user_permissions.add(permission_add)
        self.user.user_permissions.add(permission_view)
        self.user.user_permissions.add(permission_update)
        self.user.user_permissions.add(permission_delete)

        self.client = graphql_jwt.testcases.JSONWebTokenClient()
        self.client.authenticate(self.user)

    # region Authenticated Meter Tests
    def test_createMeter(self):
        query = """
            mutation MeterCreate($input:MeterCreateInput!){
                meterCreate(input:$input){
                    meter{
                    id
                    meterSerial
                    installDate
                    meterType{
                        id
                    }
                    }
                }
            }
        """

        variables = {
            "input": {
                "meterSerial": "asdf1234",
                "installDate": "2020-01-30T01:08:34.028000+00:00",
                "meterType": "TWV0ZXJUeXBlVHlwZToy",
            }
        }

        result = self.client.execute(query, variables=variables)
        assert result.errors is None

    def test_readMeter(self):
        query = """
            query MeterRead($input:String!){
            meterRead(meterSerial_Icontains: $input){
                edges{
                node{
                    id
                    meterSerial
                    installDate
                    retireDate
                }
                }
            }
            }
        """

        variables = {
            "input": "kzx1234sss3778022"
        }

        result = self.client.execute(query, variables=variables)
        assert result.errors is None
        assert result.data['meterRead']['edges'][0]['node']['installDate'] == '2020-01-30T01:08:34.028000+00:00'

    def test_updateMeter(self):
        query_read = """
            query MeterRead($input:String!){
            meterRead(meterSerial_Icontains: $input){
                edges{
                node{
                    id
                    meterSerial
                    installDate
                    retireDate
                    meterType{
                        id
                    }
                }
                }
            }
            }
        """
        variables_read = {
            "input": "kzx1234sss3778022"
        }

        result = self.client.execute(query_read, variables_read)
        id = result.data['meterRead']['edges'][0]['node']['id']
        metertypeid = result.data['meterRead']['edges'][0]['node']['meterType']['id']

        query = """
        mutation($input:MeterUpdateInput!){
            meterUpdate(input:$input){
               clientMutationId
            }
        }
        """

        variables = {
            "input": {
                "id": id,
                "meterSerial": "kzx1234sss3778022",
                "installDate": "2020-01-30T01:08:34.028000+00:00",
                "retireDate": "2020-03-30T01:08:34.028000+00:00",
                "meterType": metertypeid,
            }
        }

        result = self.client.execute(query, variables)
        assert result.errors is None

    def test_deleteMeter(self):
        query_read = """
            query MeterRead($input:String!){
            meterRead(meterSerial_Icontains: $input){
                edges{
                node{
                    id
                    meterSerial
                    installDate
                    retireDate
                    meterType{
                        id
                    }
                }
                }
            }
            }
        """
        variables_read = {
            "input": "kzx1234sss3778022"
        }

        result = self.client.execute(query_read, variables_read)
        id = result.data['meterRead']['edges'][0]['node']['id']

        variables = {
            "input": {
                'id': id,
            }
        }
        assert variables['input']['id'] is not None
        if variables['input']['id'] is not None:
            query_delete = """
                mutation MeterDelete($input: MeterDeleteInput!){
                    meterDelete(input: $input){
                        meter{
                            id
                        }
                    }
                }
            """

        result = self.client.execute(query_delete, variables=variables)
        assert result.errors is None

    # endregion Authenticated Meter Tests


class TestAccountAssetLink(graphql_jwt.testcases.JSONWebTokenTestCase):
    def setUp(self):

        self.user = get_user_model().objects.create(username='test')

        permission_view = Permission.objects.get(
            name='Can view account_ asset_ link')
        permission_add = Permission.objects.get(
            name='Can add account_ asset_ link')
        permission_update = Permission.objects.get(
            name='Can change account_ asset_ link')
        permission_delete = Permission.objects.get(
            name='Can delete account_ asset_ link')
        self.user.user_permissions.add(permission_add)
        self.user.user_permissions.add(permission_view)
        self.user.user_permissions.add(permission_update)
        self.user.user_permissions.add(permission_delete)

        self.client = graphql_jwt.testcases.JSONWebTokenClient()
        self.client.authenticate(self.user)

    def test_read_account_asset_link(self):
        """ Test searching and reading an asset account link."""
        pass

    def test_createAccoutAssetLink(self):
        """ Test creating an asset account link."""
        pass

    def test_updateAccountAssetLink(self):
        """ Test updating an asset account link."""
        pass

    def test_deleteAccountAssetLink(self):
        """ Test deleting an asset account link."""
        pass
