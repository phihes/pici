from pici.communities.discourse import DiscourseCommunity, DiscourseCommunityFactory


class OEMCommunity(DiscourseCommunity):
    
    name = "OpenEnergyMonitor"
    

class OEMCommunityFactory(DiscourseCommunityFactory):
    
    name = "oem"
    base_url = "https://community.openenergymonitor.org/"
    