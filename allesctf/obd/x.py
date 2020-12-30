from scapy.all import *
from scapy.utils import PcapReader
from scapy.contrib.isotp import ISOTPSession
from scapy.contrib.automotive.uds import UDS
from scapy.contrib.automotive.ecu import ECU
from IPython import embed
# from scapy import ISOTPSession, UDS, ECU

with PcapReader("./t2.pcap") as sock:
    udsmsgs = sniff(session=ISOTPSession, session_kwargs={"use_ext_addr":False, "basecls":UDS}, count=100, opened_socket=sock)

# embed()
ecu = ECU()
ecu.update(udsmsgs)
embed()
print(ecu.log)
print(ecu.supported_responses)
assert len(ecu.log["TransferData"]) == 2

