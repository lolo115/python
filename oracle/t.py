import oci

config=oci.config.from_file()
virtual_network_client = oci.core.VirtualNetworkClient(config)

vcn_id="ocid1.vcn.oc1.eu-frankfurt-1.aaaaaaaaylddvu25bbxuvwz5tyf2oenbydcyhrsismcwd6xbc3eh7dly7qua"
vcn=virtual_network_client.get_vcn(vcn_id=vcn_id)

route_table_resp= virtual_network_client.get_route_table(vcn.data.default_route_table_id)
route_rules = route_table_resp.data.route_rules

print("route rules : ",route_rules)

# a bit more complex and encapsulated

route_rules = virtual_network_client.get_route_table(virtual_network_client.get_vcn(vcn_id=vcn_id).data.default_route_table_id).data.route_rules

print("route rules : ",route_rules)
