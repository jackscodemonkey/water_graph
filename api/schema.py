import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required, permission_required
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from collections import namedtuple

from .models import Customer, MeterType, Meter, Account_Asset_Link, Consumption, Rate


def reverse_node_id(NodeId):
    # Reverse the Node encoded ID into a Django ID for pk lookup.
    Rid = namedtuple('Rid', 'name id')
    rid = Rid(*from_global_id(NodeId))
    return rid.id

def print_user_context(info):
    user = info.context.user
    print('User: {}'.format(user))

# region Customers


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filter_fields = {
            'first_name': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )


class CustomerConnection(relay.Connection):
    class Meta:
        node = CustomerType


class CustomerCreate(relay.ClientIDMutation):
    class Input:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    customer = graphene.Field(CustomerType)

    @classmethod
    @permission_required('api.add_customer')
    def mutate_and_get_payload(cls, root, info, **kwargs):
        customer = Customer.objects.create(
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name']
        )

        return CustomerCreate(customer=customer)


class CustomerUpdate(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    customer = graphene.Field(CustomerType)

    @classmethod
    @permission_required('api.change_customer')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        rid = reverse_node_id(NodeId=kwargs['id'])

        customer = Customer.objects.get(pk=rid)
        customer.first_name = kwargs['first_name']
        customer.last_name = kwargs['last_name']
        customer.save()

        return CustomerUpdate(customer=customer)


class CustomerDelete(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    customer = graphene.Field(CustomerType)

    @classmethod
    @permission_required('api.delete_customer')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        rid = reverse_node_id(NodeId=kwargs['id'])
        customer = Customer.objects.get(pk=rid)
        customer.delete()

        return CustomerDelete(customer=customer)

# endregion Customers

# region MeterTypeType


class MeterTypeType(DjangoObjectType):
    class Meta:
        model = MeterType
        description = """ This is the meter type node."""
        filter_fields = {
            'meter_model': ['exact', 'icontains', 'istartswith'],
            'meter_vendor': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class MeterTypeCreate(relay.ClientIDMutation):
    class Input:
        meter_model = graphene.String(required=True)
        meter_vendor = graphene.String(required=True)

    metertype = graphene.Field(MeterTypeType)

    @classmethod
    @permission_required('api.add_metertype')
    def mutate_and_get_payload(cls, root, info, **kwargs):
        metertype = MeterType.objects.create(
            meter_model=kwargs['meter_model'],
            meter_vendor=kwargs['meter_vendor']
        )

        return MeterTypeCreate(metertype=metertype)


class MeterTypeUpdate(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        meter_model = graphene.String(required=True)
        meter_vendor = graphene.String(required=True)

    metertype = graphene.Field(MeterTypeType)

    @classmethod
    @permission_required('api.change_metertype')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        rid = reverse_node_id(NodeId=kwargs['id'])

        metertype = MeterType.objects.get(pk=rid)
        metertype.meter_model = kwargs['meter_model']
        metertype.meter_vendor = kwargs['meter_vendor']
        metertype.save()

        return MeterTypeUpdate(metertype=metertype)


class MeterTypeDelete(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    metertype = graphene.Field(MeterTypeType)

    @classmethod
    @permission_required('api.delete_metertype')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        rid = reverse_node_id(NodeId=kwargs['id'])
        metertype = MeterType.objects.get(pk=rid)
        metertype.delete()

        return MeterTypeDelete(metertype=metertype)


class MeterTypeConnection(relay.Connection):
    """ Meter Type Connection """
    class Meta:
        node = MeterTypeType
# endregion MeterTypeType

# region Meter


class MeterTy(DjangoObjectType):
    class Meta:
        model = Meter
        description = """ This is the meter node."""
        filter_fields = {
            'meter_type': ['exact'],
            'meter_serial': ['exact', 'icontains', 'istartswith'],
            'install_date': ['exact', 'range', 'year', 'month', 'day'],
            'retire_date': ['exact', 'range', 'year', 'month', 'day'],
        }
        interfaces = (relay.Node,)


class MeterCreate(relay.ClientIDMutation):
    class Input:
        meter_type = graphene.String(required=True)
        meter_serial = graphene.String(required=True)
        install_date = graphene.DateTime(required=True)

    meter = graphene.Field(MeterTy)

    @classmethod
    @permission_required('api.add_meter')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        meterTyperid = reverse_node_id(NodeId=kwargs['meter_type'])
        meterType = MeterType.objects.get(pk=meterTyperid)

        meter = Meter.objects.create(
            meter_type=meterType,
            meter_serial=kwargs['meter_serial'],
            install_date=kwargs['install_date'],
        )

        return MeterCreate(meter=meter)


class MeterUpdate(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        meter_type = graphene.String(required=True)
        meter_serial = graphene.String(required=True)
        install_date = graphene.DateTime(required=True)
        retire_date = graphene.DateTime(required=True)

    meter = graphene.Field(MeterTy)

    @classmethod
    @permission_required('api.change_meter')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        rid = reverse_node_id(NodeId=kwargs['id'])

        meterTyperid = reverse_node_id(NodeId=kwargs['meter_type'])
        meterType = MeterType.objects.get(pk=meterTyperid)

        meter = Meter.objects.get(pk=rid)
        meter.meter_type = meterType
        meter.meter_serial = kwargs['meter_serial']
        meter.install_date = kwargs['install_date']
        meter.retire_date = kwargs['retire_date']
        meter.save()

        return MeterUpdate(meter=meter)


class MeterDelete(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    meter = graphene.Field(MeterTy)

    @classmethod
    @permission_required('api.delete_meter')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        rid = reverse_node_id(NodeId=kwargs['id'])
        meter = Meter.objects.get(pk=rid)
        meter.delete()

        return MeterDelete(meter=meter)


class MeterTyConnection(relay.Connection):
    class Meta:
        node = MeterTy


# endregion MeterType

# region Account_Asset_Link
class AccountAssetLinkType(DjangoObjectType):
    class Meta:
        model = Account_Asset_Link
        description = """
        This is the Asset Account Link node. It is an itermediate table
        used to match Customer accounts to Meters
        """
        filter_fields = {
            'customer': ['exact'],
            'meter': ['exact'],
        }
        interfaces = (relay.Node,)


class AssetAccountLinkCreate(relay.ClientIDMutation):
    class Input:
        customer = graphene.Int(required=True)
        meter = graphene.Int(required=True)

    asset = graphene.Field(AccountAssetLinkType)

    @classmethod
    @permission_required('api.add_account_asset_link')
    def mutate_and_get_payload(cls, root, info, **kwargs):
        asset = Account_Asset_Link.objects.create(
            customer=kwargs['customer'],
            meter=kwargs['meter'],
        )

        return AssetAccountLinkCreate(asset=asset)


class AssetAccountLinkUpdate(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        customer = graphene.Int(required=True)
        meter = graphene.Int(required=True)

    asset = graphene.Field(AccountAssetLinkType)

    @classmethod
    @permission_required('api.change_account_asset_link')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        # Fetch the customer model object and update
        rid = reverse_node_id(NodeId=kwargs['id'])

        asset = Account_Asset_Link.objects.get(pk=rid)
        asset.customer = kwargs['customer']
        asset.meter = kwargs['meter']
        asset.save()

        return AssetAccountLinkUpdate(asset=asset)


class AssetAccountLinkDelete(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    asset = graphene.Field(AccountAssetLinkType)

    @classmethod
    @permission_required('api.delete_account_asset_link')
    def mutate_and_get_payload(cls, root, info, **kwargs):
        rid = reverse_node_id(NodeId=kwargs['id'])
        asset = AccountAssetLink.object.get(pk=rid)
        asset.delete()

        return AssetAccountLinkDelete(asset=asset)


class AccountAssetConnection(relay.Connection):
    class Meta:
        node = AccountAssetLinkType

# endregion Account_Asset_Link

# region ConsumptionType


class ConsumptionType(DjangoObjectType):
    class Meta:
        model = Consumption
        description = """
        This is the consumption history node.
        """
        filter_fields = {
            'meter': ['exact'],
            'read_time': ['exact', 'range', 'year', 'month', 'day'],
            'reading': ['exact', 'range'],
            'unit_of_measure': ['exact'],
        }
        interfaces = (relay.Node,)


class ConsumptionCreate(relay.ClientIDMutation):
    class Input:
        meter = graphene.Int(required=True)
        read_time = graphene.DateTime(required=True)
        reading = graphene.Int(required=True)
        unit_of_measure = graphene.String(required=True)

    consumption = graphene.Field(ConsumptionType)

    @classmethod
    @permission_required('api.create_consumption')
    def mutate_and_get_payload(cls, root, info, **kwargs):
        consumption = Consumption.objects.create(
            meter=kwargs['meter'],
            read_time=kwargs['read_time'],
            reading=kwargs['reading'],
            unit_of_measure=kwargs['unit_of_measure'],
        )

        return ConsumptionCreate(consumption=consumption)


class ConsumptionUpdate(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        meter = graphene.Int(required=True)
        read_time = graphene.DateTime(required=True)
        reading = graphene.Int(required=True)
        unit_of_measure = graphene.String(required=True)

    consumption = graphene.Field(ConsumptionType)

    @classmethod
    @permission_required('api.change_consumption')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        rid = reverse_node_id(NodeId=kwargs['id'])

        consumption = Consumption.object.get(pd=rid)
        consumption.meter = kwargs['meter']
        consumption.read_time = kwargs['read_time']
        consumption.reading = kwargs['reading']
        consumption.unit_of_measure = kwargs['unit_of_measure']
        consumption.save()

        return ConsumptionUpdate(consumption=consumption)


class ConsumptionDelete(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    consumption = graphene.Field(ConsumptionType)

    @classmethod
    @permission_required('api.delete_consumption')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        rid = reverse_node_id(NodeId=kwargs['id'])

        consumption = Consumption.object.get(pk=rid)
        consumption.delete()

        return ConsumptionDelete(consumption=consumption)


class ConsumptionTypeConnection(relay.Connection):
    class Meta:
        node = ConsumptionType
# endregion ConsumptionType

# region Rate


class RateType(DjangoObjectType):
    class Meta:
        model = Rate
        description = """
        This is the rate node.
        """
        filter_fields = {
            'rate': ['exact', 'range'],
            'effective_start': ['exact', 'range', 'year', 'month', 'day'],
            'effective_end': ['exact', 'range', 'year', 'month', 'day'],
            'unit_of_measure': ['exact'],
        }
        interfaces = (relay.Node,)


class RateCreate(relay.ClientIDMutation):
    class Input:
        rate = graphene.Float(required=True)
        effective_start = graphene.Date(required=True)
        effective_end = graphene.Date(required=True)
        unit_of_measure = graphene.String(required=True)

    rate = graphene.Field(RateType)

    @classmethod
    @permission_required('api.create_rate')
    def mutate_and_get_payload(cls, root, info, **kwargs):
        rate = Rate.objects.create(
            rate=kwargs['rate'],
            effective_start=kwargs['effective_start'],
            effective_end=kwargs['effective_end'],
            unit_of_measure=kwargs['unit_of_measure'],
        )

        return RateCreate(rate=rate)


class RateUpdate(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        rate = graphene.Float(required=True)
        effective_start = graphene.Date(required=True)
        effective_end = graphene.Date(required=True)
        unit_of_measure = graphene.String(required=True)

    rate = graphene.Field(RateType)

    @classmethod
    @permission_required('api.change_rate')
    def mutate_and_get_payload(cls, root, info, **kwargs):
        rid = reverse_node_id(NodeId=kwargs['id'])

        rate = Rate.objects.get(pk=rid)
        rate.rate = kwargs['rate']
        rate.effective_start = kwargs['effective_start']
        rate.effective_end = kwargs['effective_end']
        rate.unit_of_measure = kwargs['unit_of_measure']
        rate.save()

        return RateUpdate(rate=rate)


class RateDelete(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    rate = graphene.Field(RateType)

    @classmethod
    @permission_required('api.delete_rate')
    def mutate_and_get_payload(cls, root, info, **kwargs):

        rid = reverse_node_id(NodeId=kwargs['id'])

        rate = Rate.objects.get(pd=rid)
        rate.delete()

        return RateDelete(rate=rate)


class RateTypeConnection(relay.Connection):
    class Meta:
        node = RateType
# endregion Rate

# region Query


class Query(graphene.ObjectType):
    """ Graphene Schema Queries """

    """ Customer Queries """
    customer_read = DjangoFilterConnectionField(CustomerType, description="""
    Returns a filtered list of customers, or leave filters blank for all customers.""")

    @permission_required('api.view_customer')
    def resolve_customer_read(self, info, **kwargs):
        print_user_context(info)

    """ Meter Type Queries """
    metertype_read = DjangoFilterConnectionField(MeterTypeType, description="""
    Returns a filtered list of water meter types. ie: model/manufacturer and the meters
    system id. Leave filters blank to return all meters.""")

    @permission_required('api.view_metertype')
    def resolve_metertype_read(self, info, **kwargs):
        print_user_context(info)

    """ Meter Inentory Queries """
    meter_read = DjangoFilterConnectionField(MeterTy, description="""
    Returns a filtered list of customer meters deployed in field. Leave filters blank to return
    all meters in inventory.
    """)

    @permission_required('api.view_meter')
    def resolve_meter(self, info, **kwargs):
        print_user_context(info)

    """ Asset Account Linking Table Queries """
    asset_account_link_read = DjangoFilterConnectionField(AccountAssetLinkType, description="""
    Asset account linking table, contains foreign key relationship between deployed meters
    and customers.
    """)

    @permission_required('api.view_account_asset_link')
    def resolve_asset_account_link(self, info, **kwargs):
        print_user_context(info)

    """ Consumtion Information Queries """
    consumption_read = DjangoFilterConnectionField(ConsumptionType, description="""
    Returns a filtered list of meter consumption records. Leave filters blank to return all
    consumption information.
    """)

    @permission_required('api.view_consumption')
    def resolve_consumption(self, info, **kwargs):
        print_user_context(info)

    """ Rate Queries """
    rate_read = DjangoFilterConnectionField(RateType, description="""
    Returns a filtered list of rates. Leave filters blank to return all rates.
    """)

    @permission_required('api.view_rate')
    def resolve_rate(self, info, **kwargs):
        print_user_context(info)

# endregion Query

# region Mutation


class Mutation(graphene.ObjectType):

    # region GraphqlJWT Mutations
    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    token_auth.description = "GraphQL JSON Webtoken: authentication end point."
    verify_token = graphql_jwt.relay.Verify.Field()
    verify_token.description = "GraphQL JSON Webtoken: validate if a token is valid."
    refresh_token = graphql_jwt.relay.Refresh.Field()
    refresh_token.description = "GraphQL JSON Webtoken: refresh a valid token to extend its useful lifetime."
    delete_token_cookie = graphql_jwt.relay.DeleteJSONWebTokenCookie.Field()
    delete_token_cookie.description = "GraphQL JSON Webtoken: destroy token immediately."

    # Long running refresh tokens
    revoke_token = graphql_jwt.relay.Revoke.Field()
    revoke_token.description = "GraphQL JSON Webtoken: revoke long running refresh tokens."
    delete_refresh_token_cookie = graphql_jwt.refresh_token.relay.DeleteRefreshTokenCookie.Field()
    delete_refresh_token_cookie.description = "GraphQL JSON Webtoken: delete logn running refresh token cookie."
    # endregion GraphqlJWT Mutations

    # region Customer Mutations
    customer_create = CustomerCreate.Field()
    customer_create.description = "Create a new customer account."
    customer_update = CustomerUpdate.Field()
    customer_update.description = "Update a current customer."
    customer_delete = CustomerDelete.Field()
    customer_delete.description = "Delete a current customer (cascading delete of all associated records)."
    # endregion Customer Mutations#region Customer Mutations

    # region MeterType Mutations
    metertype_create = MeterTypeCreate.Field()
    metertype_create.description = "Create a new meter type for the inventory."
    metertype_update = MeterTypeUpdate.Field()
    metertype_update.description = "Update an existing meter type."
    metertype_delete = MeterTypeDelete.Field()
    metertype_delete.description = "Delete a meter type (cascading delete of all associated records)."
    # endregion Meter Type Mutations

    # region Meter Mutations
    meter_create = MeterCreate.Field()
    meter_create.description = "Create Meter installation records."
    meter_update = MeterUpdate.Field()
    meter_update.description = "Update existing Meter installation records."
    meter_delete = MeterDelete.Field()
    meter_delete.description = "Delete a meter installation (cascading delete of all associated records)."
    # endregion Meter Mutations

    # region Assest Account Linking Mutations
    asset_account_link_create = AssetAccountLinkCreate.Field()
    asset_account_link_create.description = "Create a link between customers and a meter asset."
    asset_account_link_update = AssetAccountLinkUpdate.Field()
    asset_account_link_update.description = "Update an existing link between a customer and meter."
    asset_account_link_delete = AssetAccountLinkDelete.Field()
    asset_account_link_delete.description = "Delete a link between a customer and meter (cascading delete of all associated records)."
    # endregion Assest Account Linking Mutations

    # region Consumption Mutations
    consumption_create = ConsumptionCreate.Field()
    consumption_create.description = "Create a consumption record from a meter reading."
    consumption_update = ConsumptionUpdate.Field()
    consumption_update.description = "Update an existing consumption record."
    consumption_delete = ConsumptionDelete.Field()
    consumption_delete.description = "Delete a consumption record (cascading delete of all associated records)."
    # endregion Consumption Mutations

    # region Rate Mutations
    rate_create = RateCreate.Field()
    rate_create.description = "Create a new rate to apply to meter consumption."
    rate_update = RateUpdate.Field()
    rate_update.description = "Update and existing rate for meter conumption records."
    rate_delete = RateDelete.Field()
    rate_delete.description = "Delete a rate record (cascading delete of all associated records)."
    # endregion Rate Mutations

# endregion Mutation
