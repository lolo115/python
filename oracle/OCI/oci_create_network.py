import oci
import os
import sys

def create_vcn(virtual_network, vcn_name, compartment_id, cidr_block):
    result = virtual_network.create_vcn(
        oci.core.models.CreateVcnDetails(
            cidr_block=cidr_block,
            display_name=vcn_name,
            compartment_id=compartment_id
        )
    )
    get_vcn_response = oci.wait_until(
        virtual_network,
        virtual_network.get_vcn(result.data.id),
        'lifecycle_state',
        'AVAILABLE'
    )
    print('Created VCN: {}'.format(get_vcn_response.data.id))

    return get_vcn_response.data

def create_subnet(virtual_network, vcn, subnet_name, availability_domain):
    result = virtual_network.create_subnet(
        oci.core.models.CreateSubnetDetails(
            compartment_id=vcn.compartment_id,
            availability_domain=availability_domain,
            display_name=subnet_name,
            vcn_id=vcn.id,
            cidr_block=vcn.cidr_block
        )
    )
    get_subnet_response = oci.wait_until(
        virtual_network,
        virtual_network.get_subnet(result.data.id),
        'lifecycle_state',
        'AVAILABLE'
    )
    print('Created Subnet: {}'.format(get_subnet_response.data.id))

    return get_subnet_response.data

def create_internet_gateway(virtual_network, vcn, internet_gateway_name):
    result = virtual_network.create_internet_gateway(
        oci.core.models.CreateInternetGatewayDetails(
            display_name=internet_gateway_name,
            compartment_id=vcn.compartment_id,
            is_enabled=True,
            vcn_id=vcn.id
        )
    )
    get_internet_gateway_response = oci.wait_until(
        virtual_network,
        virtual_network.get_internet_gateway(result.data.id),
        'lifecycle_state',
        'AVAILABLE'
    )
    print('Created internet gateway: {}'.format(get_internet_gateway_response.data.id))

    add_route_rule_to_default_route_table_for_internet_gateway(
        virtual_network,
        vcn,
        get_internet_gateway_response.data
    )

    return get_internet_gateway_response.data

def add_route_rule_to_default_route_table_for_internet_gateway(virtual_network, vcn, internet_gateway):
    get_route_table_response = virtual_network.get_route_table(vcn.default_route_table_id)
    route_rules = get_route_table_response.data.route_rules

    print('\nCurrent Route Rules For VCN')
    print('===========================')
    print('{}\n\n'.format(route_rules))

    # Updating route rules will totally replace any current route rules with what we send through.
    # If we wish to preserve any existing route rules, we need to read them out first and then send
    # them back to the service as part of any update
    route_rules.append(
        oci.core.models.RouteRule(
            cidr_block='0.0.0.0/0',
            network_entity_id=internet_gateway.id
        )
    )

    virtual_network.update_route_table(
        vcn.default_route_table_id,
        oci.core.models.UpdateRouteTableDetails(route_rules=route_rules)
    )

    get_route_table_response = oci.wait_until(
        virtual_network,
        virtual_network.get_route_table(vcn.default_route_table_id),
        'lifecycle_state',
        'AVAILABLE'
    )

    print('\nUpdated Route Rules For VCN')
    print('===========================')
    print('{}\n\n'.format(get_route_table_response.data.route_rules))

    return get_route_table_response.data

def get_image(compute, operating_system, operating_system_version, shape):
    # Listing images is a paginated call, so we can use the oci.pagination module to get all results
    # without having to manually handle page tokens
    #
    # In this case, we want to find the image for the OS and version we want to run, and which can
    # be used for the shape of instance we want to launch
    list_images_response = oci.pagination.list_call_get_all_results(
        compute.list_images,
        compartment_id,
        operating_system=operating_system,
        operating_system_version=operating_system_version,
        shape=shape
    )

    # For demonstration, we just return the first image but for Production code you should have a better
    # way of determining what is needed
    return list_images_response.data[0]

# main
if __name__ == '__main__':
    # Default config file and profile
    config = oci.config.from_file()
    compute_client = oci.core.ComputeClient(config)
    virtual_network_client = oci.core.VirtualNetworkClient(config)

    vcn = None
    subnet = None
    internet_gateway = None
    ssh_public_key_path='/Users/leturgezl/.ssh/id_rsa.pub'

    vcn_name = 'PREMISEO-VCN'
    subnet_name = vcn_name+'-subnet1'
    internet_gateway_name='premiseo_GW'
    cidr_block='10.10.10.0/24'
    availability_domain='EUUz:EU-FRANKFURT-1-AD-1'
    subnet = None
    internet_gateway = None

    # Compartment ID for premiseo
    compartment_id="ocid1.compartment.oc1..aaaaaaaawvlb2q64wmiixsvhslhpleydssbq2ihowtdf6ck5glke2hsa3p6q"

    vcn = create_vcn(virtual_network_client, vcn_name, compartment_id, cidr_block)
    subnet = create_subnet(virtual_network_client, vcn, subnet_name, availability_domain)
    internet_gateway = create_internet_gateway(virtual_network_client, vcn, internet_gateway_name)
