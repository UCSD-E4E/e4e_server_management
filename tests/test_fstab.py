from ServerManagement.fstab import Fstab

def test_load():
    original_fstab = ("# /etc/fstab: static file system information.\n"
        "#\n"
        "# Use 'blkid' to print the universally unique identifier for a\n"
        "# device; this may be used with UUID= as a more robust way to name devices\n"
        "# that works even if disks are added and removed. See fstab(5).\n"
        "#\n"
        "# <file system> <mount point>   <type>  <options>       <dump>  <pass>\n"
        "# / was on /dev/sda2 during installation\n"
        "UUID=a9b76d9f-e652-4f3c-a4d3-5f17ae417405 /               ext4    errors=remount-ro 0       1\n"
        "# /boot/efi was on /dev/sda1 during installation\n"
        "UUID=6357-16C6  /boot/efi       vfat    umask=0077      0       1\n"
        "# swap was on /dev/nvme0n1p1 during installation\n"
        "UUID=6c8c0eb2-63c6-4237-a095-a6f9457d3e0e none            swap    sw              0       0\n"
        "//e4e-nas.ucsd.edu/aye-aye-sleep-monitoring /mnt/aye-aye-sleep-monitoring cifs vers=3.0,credentials=/home/e4eadmin/e4e-nas.creds,file_mode=0777,dir_mode=0777 0 0\n"
        "UUID=1548aaac-99a5-4da6-99f7-ca365788a119 /mnt/data ext4 rw,user 0 0\n")
    with open('/tmp/fstab', 'w') as tmp_tab:
        tmp_tab.write(original_fstab)
    fstab = Fstab(path='/tmp/fstab')
    assert(len(fstab.entries) == 5)
    assert(fstab.entries[0].filesystem == "UUID=a9b76d9f-e652-4f3c-a4d3-5f17ae417405")
    assert(fstab.entries[1].filesystem == "UUID=6357-16C6")
    assert(fstab.entries[2].filesystem == "UUID=6c8c0eb2-63c6-4237-a095-a6f9457d3e0e")
    assert(fstab.entries[3].filesystem == "//e4e-nas.ucsd.edu/aye-aye-sleep-monitoring")
    assert(fstab.entries[4].filesystem == "UUID=1548aaac-99a5-4da6-99f7-ca365788a119")

    assert(fstab.entries[0].mount.exists())
    assert(fstab.entries[1].mount.exists())
    assert(fstab.entries[2].mount == None)
    assert(fstab.entries[3].mount.exists())
    assert(fstab.entries[4].mount.exists())

    assert(fstab.entries[0].mount.is_mount())
    assert(fstab.entries[1].mount.is_mount())
    assert(fstab.entries[3].mount.is_mount())
    assert(fstab.entries[4].mount.is_mount())

    assert(fstab.entries[0].fstype == 'ext4')
    assert(fstab.entries[1].fstype == 'vfat')
    assert(fstab.entries[2].fstype == 'swap')
    assert(fstab.entries[3].fstype == 'cifs')
    assert(fstab.entries[4].fstype == 'ext4')

    assert(fstab.entries[3].options[0] == 'vers=3.0')
    assert(fstab.entries[3].options[1] == 'credentials=/home/e4eadmin/e4e-nas.creds')
    assert(fstab.entries[3].options[2] == 'file_mode=0777')
    assert(fstab.entries[3].options[3] == 'dir_mode=0777')

    assert(fstab.entries[0].dump == 0)
    assert(fstab.entries[1].dump == 0)
    assert(fstab.entries[2].dump == 0)
    assert(fstab.entries[3].dump == 0)
    assert(fstab.entries[4].dump == 0)

    assert(fstab.entries[0].pass_const == 1)
    assert(fstab.entries[1].pass_const == 1)
    assert(fstab.entries[2].pass_const == 0)
    assert(fstab.entries[3].pass_const == 0)
    assert(fstab.entries[4].pass_const == 0)

    fstab.compile(path='/tmp/fstab2')
    with open('/tmp/fstab2', 'r') as f:
        fstab_compiled = f.read()
    
    