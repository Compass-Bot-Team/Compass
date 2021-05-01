import linux
import windows
import other-operating-systems


operating_system_list = []
for distro in linux.distros:
    operating_system_list.append(distro)
for version in windows.family:
    operating_system_list.append(version)
for os in other-operating-systems.all:
    operating_system_list.append(os)
