from riskreport.client import riskreport_on_entity 

eth_address_1 = "0xbb0ea877a85df253ccc312b80c644da31443abfd"

# Single address example
report = riskreport_on_entity(eth_addresses=[eth_address_1])

for reason in report.reasons:
    print()
    print(f"The following contributed to the score by: {reason.offsets.combined_risk_offset}")
    print(reason.explanation)
