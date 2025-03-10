# Starlink Emulation scripts

These scripts are meant to simplify extracting the different partitions from a Starlink User Terminal eMMC dump.

## Install dependencies:

We use already existing tools which require some dependencies.
To install all dependencies at once, you can use our install-requirements.sh script.

### Usage:

```bash
cd scripts/
sudo ./install-requirements.sh
```

## Extracting partitions:

The script extract-from-firmware-dump.sh makes it easy and quick to extract all the important data from a raw Starlink User Terminal eMMC dump.
It takes the dumped image as an argument and creates the directories /dish-partitions with all the extracted dish partitions.
Additionally it creates the directory /rootfs with all the files included in the linux-a partition. The runtime scripts from sx-a are already included in /rootfs.

### Usage:

For example:

```bash
cd scripts/
sudo ./extract-from-firmware-dump.sh ../starlink-dish-emmc.img

