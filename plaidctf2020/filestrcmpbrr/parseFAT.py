#!/usr/bin/env python
# Parse the initial bytes from a FAT-fs image.
# 2012-04-08
import struct
import sys

# formats of various parts of a FAT boot sector:

# ----
# offsets into boot_sector fields:
jmp_instr = 0
oem_id = 1
bytes_per_sector = 2
sectors_per_cluster = 3
n_reserved_sectors = 4
n_FATs = 5
n_root_entries = 6
n_sectors_small = 7
media_descriptor = 8
sectors_per_FAT = 9
sectors_per_track = 10
n_heads = 11
n_hidden_sectors = 12
n_sectors_large = 13

sectors_per_FAT32 = 14
# ----

bpb_format = {
    # Field                     Offset Length
    # -----                     ------ ------
    "Bytes Per Sector": (0x0B, 2),
    "Sectors Per Cluster": (0x0D, 1),
    "Reserved Sectors": (0x0E, 2),
    "FATs": (0x10, 1),
    "Root Entries": (0x11, 2),
    "Small Sectors": (19, 2),
    "Media Descriptor": (21, 1),
    "Sectors Per FAT": (22, 2)
    # DOS 3.31 ---
    ,
    "Sectors Per Track": (0x18, 2),
    "Heads": (26, 2),
    "Hidden Sectors": (28, 4),
    "Large Sectors": (0x20, 4),
}
bpbfields = "HBHBHHBHHHII"
bpblen = sum([i[1] for i in bpb_format.values()])

media_discription_byte = {
    0xF0: (
        "1.44 MB / 2.88 MB",
        "3.5-inch, 2-sided, 18-sector / 3.5-inch, 2-sided, 36-sector",
    )
    #  , 0xf0 : ('1.44 MB', '3.5-inch, 2-sided, 18-sector')
    #  , 0xf0 : ('2.88 MB', '3.5-inch, 2-sided, 36-sector')
    ,
    0xF9: (
        "720 KB / 1.2 MB",
        "3.5-inch, 2-sided, 9-sector / 5.25-inch, 2-sided, 15-sector",
    )
    #  , 0xf9 : ( '720 KB', '3.5-inch, 2-sided, 9-sector')
    #  , 0xf9 : ( '1.2 MB', '5.25-inch, 2-sided, 15-sector')
    ,
    0xFD: ("360 KB", "5.25-inch, 2-sided, 9-sector"),
    0xFF: ("320 KB", "5.25-inch, 2-sided, 8-sector"),
    0xFC: ("180 KB", "5.25-inch, 1-sided, 9-sector"),
    0xFE: ("160 KB", "5.25-inch, 1-sided, 8-sector"),
    0xF8: ("-----", "Fixed disk"),
}

FAT16ebpb_format = {
    # ...DOS 4.0 ---
    # Field                     Offset Length
    # -----                     ------ ------
    "Physical Drive Number": (0x24, 1),
    "Current Head": (0x25, 1),
    "Signature": (0x26, 1),
    "ID": (0x27, 4),
    "Volume Label": (0x2B, 11),
    "System ID": (0x36, 8),
}
FAT16ebpbfields = "BBBI11s8s"
FAT16ebpblen = sum([i[1] for i in FAT16ebpb_format.values()])

FAT32ebpb_format = {
    # relative offsets
    "sectors per FAT": (0x00B, 4),
    "Mirroring flags": (0x24, 2),
    "Version": (0x02A, 2),
    "root-dir start cluster": (0x02C, 4),  # typically 0
    "FS Information Sector number": (0x025, 2),  # typically 1
    "boot-sector-copy start sector": (0x027, 2),
    "reserved": (0x029, 12)
    # ...same as DOS 3.31/DOS 4.0 ebpb...
    ,
    "physical drive number": (0x035, 1),
    "various": (0x036, 1),
    "Extended boot signature": (0x037, 1),
    "Volume ID": (0x038, 4),
    "Volume Label": (0x03C, 11),
    "file system type": (0x047, 8),
}
FAT32ebpbfields = "IHHIHH12sBBBI11s8s"
FAT32ebpblen = sum([i[1] for i in FAT32ebpb_format.values()])

basic_bpb_format = "<3s8s" + bpbfields

signature = "BB"

# How much space for boot code?

basicbootcodelength = (
    512 - struct.calcsize(basic_bpb_format) - struct.calcsize(signature)
)
FAT16bootcodelength = basicbootcodelength - FAT16ebpblen
FAT32bootcodelength = basicbootcodelength - FAT32ebpblen

# Finally, set up the boot-sector formats

FAT16_middle = FAT16ebpbfields + "%ds" % FAT16bootcodelength
FAT16boot_sector_format = basic_bpb_format + FAT16_middle + signature

FAT32_middle = FAT32ebpbfields + "%ds" % FAT32bootcodelength
FAT32boot_sector_format = basic_bpb_format + FAT32_middle + signature

basicBSstruct = struct.Struct(basic_bpb_format)
FAT16struct = struct.Struct(FAT16boot_sector_format)
FAT32struct = struct.Struct(FAT32boot_sector_format)

# ----------------


def get_boot_sector_bytes(filename):
    """Open a file, read the boot sector;
    return the file handle and the boot-sector bytes.
    """
    f = open(filename)
    b = f.read(512)
    return (f, b)


# ----


def get_boot_sector(filename):
    """Open a file, read the boot sector, parse it;
    return the file handle, the boot-sector bytes,
    and the boot-sector fields interpreted as both FAT12/16 and FAT32.
    """
    f, b = get_boot_sector_bytes(filename)
    f16fields = struct.unpack(FAT16boot_sector_format, b)
    f32fields = struct.unpack(FAT32boot_sector_format, b)
    return (f, b, f16fields, f32fields)


# ----
f, b, f16, f32 = get_boot_sector(sys.argv[1])


def clustercount(fields):
    """Calculate the number of clusters identified in the boot sector."""
    if fields[sectors_per_FAT] != 0:
        n_FAT_sectors = fields[sectors_per_FAT]
    else:
        n_FAT_sectors = fields[sectors_per_FAT32]

    root_dir_start = (
        fields[n_reserved_sectors] * fields[bytes_per_sector]
        + n_FAT_sectors * fields[n_FATs]
    )

    bytes_in_root_dir = fields[n_root_entries] * 32
    data_start_bytes = root_dir_start + bytes_in_root_dir
    data_start_sectors = data_start_bytes / fields[bytes_per_sector]

    if fields[n_sectors_small] != 0:
        n_sectors = fields[n_sectors_small]
    else:
        n_sectors = fields[n_sectors_large]

    n_clusters = (n_sectors - data_start_sectors) / fields[sectors_per_cluster]
    return n_clusters


print(clustercount(f32))

# ----


def FATtype(fields):
    """Identify the FAT type based on the number of clusters in the fs."""
    if clustercount(fields) < 4087:
        return "FAT12"
    elif clustercount(fields) < 65527:
        return "FAT16"
    elif clustercount(fields) < 268435447:
        return "FAT32"
    else:
        return "FAT"


# ----

# -----------------------------------------------------------
# Which FAT is it?
#
# see
#   homepage.ntlworld.com/jonathan.deboynepollard/FGA/determining-fat-widths.html
# for a detailed algorithm.
#
# see also
#   support.microsoft.com/kb/140418
#
# from
#   averstak.tripod.com/fatdox/bootsec.htm
averstack_doco = """
...
Now it is high time to explain how clusters are mapped to sectors.
First, consider the layout of the FAT disk:
    LBA Location    Length in Sectors 	                Description
    --------------- ----------------------------------- --------------
    0 	            ReservedSectors 	                Boot Sector(s),
                                                        File System Info Sector
    ReservedSectors NumberOfFATs*SectorsPerFAT 	        File Allocation Tables
    RootStart * 	(RootEntries*32)/BytesPerSector 	Root Directory, if any
    ClustersStart 	NumberOfClusters*SectorsPerCluster 	Data Clusters
* Note: RootStart does not make sense for FAT32 partitions.
However, the formulae below are still valid for FAT32.

Some of the values in the table are in the BPB.
Let us calculate the rest of them:
    RootStart=ReservedSectors+NumberOfFATs*SectorsPerFAT
    ClustersStart=RootStart+(RootEntries*32) div BytesPerSector
* Note: if (RootEntries*32) mod BytesPerSector then ClustersStart=ClustersStart+1
    NumberOfClusters=2+(NumberOfSectors-ClustersStart) div SectorsPerCluster

To convert cluster address to LBA address use the formula:
    LBA=ClustersStart+(Cluster-2)*SectorsPerCluster

Now we are ready to detect which file system is used.

    If NumberOfClusters<4087 then FAT12 is used.
    If 4087<=NumberOfClusters<65,527 then FAT16 is used.
    If 65,527<=NumberOfClusters<268,435,457 then FAT32 is used.
    Otherwise, none of the above is used.

I fairly warn you: I have not yet found two sources that agree on these values.
So, be careful if the number of clusters is close to the border value.
One might have noticed that the maximum NumberOfClusters for FAT32 looks odd.
Since only 28 of 32 bits are currently used, the FAT32 partition can have no
more than 268,435,456 clusters.
Looking at NumberOfClusters is the only recommended by Microsoft way of
detecting the FAT entry size.

Since the type of the file system depends on the cluster size, which can be
set arbitrarily by the formatting program, let me introduce the Microsoft
recommendations.
Note that these are only guidelines.
The partition size is not used directly to determine the FAT type.
It is first converted to NumberOfClusters as described above.
 
Partition Size          Type of FAT
10MB or less 	        FAT12
10MB through 512MB (?) 	FAT16
512MB (?) through 2TB 	FAT32
 
The following table contains the ranges for the partition sizes.
They do overlap.
 
Min Partition Size 	Max Partition Size 	Type of FAT
1.5KB 	510.75MB 	FAT12
2.0435MB 	8190.75MB 	FAT16
~32MB 	32TB 	FAT32

Author:  Alex Verstak  3/10/1998 
"""
# -----------------------------------------------------------
