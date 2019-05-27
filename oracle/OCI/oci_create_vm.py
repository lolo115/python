import oci
import os
import sys

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
    cidr_block='10.10.10.0/24'
    availability_domain='EUUz:EU-FRANKFURT-1-AD-1'

    # Compartment ID for premiseo
    compartment_id = "ocid1.compartment.oc1..aaaaaaaawvlb2q64wmiixsvhslhpleydssbq2ihowtdf6ck5glke2hsa3p6q"
    vcn_id='ocid1.vcn.oc1.eu-frankfurt-1.aaaaaaaa6dvwjqzbezpuv47gck4oydljklo6vn4a7e2fyzveasr4ker4vutq'
    subnet_id='ocid1.subnet.oc1.eu-frankfurt-1.aaaaaaaafkbzfwysvvyosx45ujly2ggww5vb44qoihciuxgnnhhrffi3uj5q'
    ig_id='ocid1.internetgateway.oc1.eu-frankfurt-1.aaaaaaaanfdjdbnvwmejllw4syoes5rjinn2c2w7nrv3dpooh5ccx4k7fjqq'

    vm_name='VM_laurent'
    vcn = None
    subnet = None
    internet_gateway = None

    vcn=virtual_network_client.get_vcn(vcn_id=vcn_id)
    print("VCN data =")
    print("\t VCN name = ",vcn.data.display_name)
    print("\t VCN cidr block=", vcn.data.cidr_block)

    subnet=virtual_network_client.get_subnet(subnet_id=subnet_id)
    print("Subnet data =")
    print("\t Subnet name = ", subnet.data.display_name)
    print("\t Subnet cidr block = ", subnet.data.cidr_block)
    print("\t Subnet availability domain =", subnet.data.availability_domain)

    internet_gateway=virtual_network_client.get_internet_gateway(ig_id=ig_id)
    print("IG data =")
    print("\t IG name = ", internet_gateway.data.display_name)
    print("\t IG state = ", internet_gateway.data.lifecycle_state)


    shape_response=compute_client.list_shapes(compartment_id=compartment_id, availability_domain=availability_domain)
    print(">>>>> Shapes available in Compartment and Availability Zone", shape_response.data)
    sys.exit(0)
    # For VM Shapes See https://docs.cloud.oracle.com/iaas/Content/Compute/References/computeshapes.htm#VMShapes
    image = get_image(compute_client, 'Oracle Linux', '7.6', 'VM.Standard2.1')
    print(image)


    with open(ssh_public_key_path, mode='r') as file:
        ssh_key = file.read()

    instance_metadata = {
        'ssh_authorized_keys': ssh_key
    }

    launch_instance_details = oci.core.models.LaunchInstanceDetails(
        display_name=vm_name,
        compartment_id=compartment_id,
        availability_domain=availability_domain,
        shape='VM.Standard2.1',
        metadata=instance_metadata,
        source_details=oci.core.models.InstanceSourceViaImageDetails(image_id=image.id),
        create_vnic_details=oci.core.models.CreateVnicDetails(subnet_id=subnet.id, display_name=vm_name+"VNIC1")
    )

    launch_instance_response = compute_client.launch_instance(launch_instance_details)

    print('\nLaunched instance')
    print('===========================')
    print('{}\n\n'.format(launch_instance_response.data))

    get_instance_response = oci.wait_until(
        compute_client,
        compute_client.get_instance(launch_instance_response.data.id),
        'lifecycle_state',
        'RUNNING'
    )

    print('\nRunning instance')
    print('===========================')
    print('{}\n\n'.format(get_instance_response.data))

    # Affichage des infos d'IP
    list_vnic_attachments_response = oci.pagination.list_call_get_all_results(
        compute_client.list_vnic_attachments,
        compartment_id,
        instance_id=get_instance_response.data.id
    )

    vnic = virtual_network_client.get_vnic(list_vnic_attachments_response.data[0].vnic_id).data
    print('\nInstance IP Addresses')
    print('===========================')
    print('Private IP: {}'.format(vnic.private_ip))
    print('Public IP: {}\n\n'.format(vnic.public_ip))


    #Instance IP Addresses
    #===========================
    #Private IP: 10.10.10.2
    #Public IP: 130.61.93.211

    # mbp:~ leturgezl$ ssh opc@130.61.93.211