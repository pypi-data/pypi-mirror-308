#
# Copyright (C) 2016
#      The Board of Trustees of the Leland Stanford Junior University
# Written by Stephane Thiell <sthiell@stanford.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import warnings

from sasutils.sysfs import SysfsDevice, SysfsObject


# DEVICE TYPES
# https://en.wikipedia.org/wiki/SCSI_Peripheral_Device_Type

TYPE_DISK = 0x00
TYPE_TAPE = 0x01
TYPE_PRINTER = 0x02
TYPE_PROCESSOR = 0x03   # HP scanners use this
TYPE_WORM = 0x04        # Treated as ROM by our system
TYPE_ROM = 0x05
TYPE_SCANNER = 0x06
TYPE_MOD = 0x07         # Magneto-optical disk treated as TYPE_DISK
TYPE_MEDIUM_CHANGER = 0x08
TYPE_COMM = 0x09        # Communications device
TYPE_RAID = 0x0c
TYPE_ENCLOSURE = 0x0d   # Enclosure Services Device
TYPE_RBC = 0x0e
TYPE_OSD = 0x11
TYPE_NO_LUN = 0x7f

# Numeric SCSI type to string mapping

MAP_TYPES = {TYPE_DISK: 'disk',
             TYPE_TAPE: 'tape',
             TYPE_PRINTER: 'printer',
             TYPE_PROCESSOR: 'processor',
             TYPE_WORM: 'worm',
             TYPE_ROM: 'rom',
             TYPE_SCANNER: 'scanner',
             TYPE_MOD: 'mod',
             TYPE_MEDIUM_CHANGER: 'medium_changer',
             TYPE_COMM: 'comm',
             TYPE_RAID: 'raid',
             TYPE_ENCLOSURE: 'enclosure',
             TYPE_RBC: 'rbc',
             TYPE_OSD: 'osd',
             TYPE_NO_LUN: 'no_lun'}


def strtype(scsi_type):
    try:
        return MAP_TYPES[int(scsi_type)]
    except ValueError:
        return "unknown(%s)" % scsi_type

#
# SCSI classes
#


class SCSIHost(SysfsDevice):

    def __init__(self, device, subsys='scsi_host'):
        SysfsDevice.__init__(self, device, subsys)


class SCSIDisk(SysfsDevice):

    def __init__(self, device, subsys='scsi_disk'):
        SysfsDevice.__init__(self, device, subsys)


class SCSIGeneric(SysfsDevice):

    def __init__(self, device, subsys='scsi_generic'):
        SysfsDevice.__init__(self, device, subsys)
        # the basename of self.sysfsnode is the name of the sg device
        self.sg_name = str(self.sysfsnode)


class SCSIDevice(SysfsObject):
    """
    scsi_device

    SCSIDevice -> array_device (ArrayDevice) -> enclosure (EnclosureDevice)
    """

    def __init__(self, device):
        # scsi_device attrs attached to device
        SysfsObject.__init__(self, device)
        self.scsi_generic = SCSIGeneric(self.sysfsnode)
        try:
            self.scsi_disk = SCSIDisk(self.sysfsnode)
        except KeyError:
            self.scsi_disk = None
        try:
            self.block = BlockDevice(self.sysfsnode, scsi_device=self)
        except KeyError:
            self.block = None
        try:
            self.tape = TapeDevice(self.sysfsnode, scsi_device=self)
        except KeyError:
            self.tape = None
        try:
            # define scsi type string as strtype for convenience
            self.strtype = strtype(self.attrs.type)
        except AttributeError:
            self.strtype = None
        self._array_device = None

    @property
    def array_device(self):
        if not self._array_device:
            try:
                array_node = self.sysfsnode.node('enclosure_device:*')
                self._array_device = ArrayDevice(array_node)
            except KeyError:
                # no enclosure_device, this may happen due to sysfs issues
                pass
        return self._array_device


#
# SCSI bus classes
#

class EnclosureDevice(SCSIDevice):
    """Managed enclosure device"""

    def __init__(self, device):
        SCSIDevice.__init__(self, device)


class ArrayDevice(SysfsObject):

    def __init__(self, sysfsnode):
        SysfsObject.__init__(self, sysfsnode)
        self.enclosure = EnclosureDevice(sysfsnode.node('../device'))

#
# Block devices
#

class BlockDevice(SysfsDevice):
    """
    scsi_disk
    """
    def __init__(self, device, subsys='block', scsi_device=None):
        SysfsDevice.__init__(self, device, subsys, sysfsdev_pattern='sd*')
        self._scsi_device = scsi_device
        self.queue = SysfsObject(self.sysfsnode.node('queue'))

    def json_serialize(self):
        data = dict(self.__dict__)
        if self._scsi_device is not None:
            data['_scsi_device'] = repr(self._scsi_device)
        return data

    @property
    def array_device(self):
        # moved to SCSIDevice but kept here for compat
        warnings.warn("use .scsi_device.array_device instead",
                      DeprecationWarning)
        return self.scsi_device.array_device

    @property
    def scsi_device(self):
        if not self._scsi_device:
            self._scsi_device = SCSIDevice(self.device)
        return self._scsi_device

    def sizebytes(self):
        """Return block device size in bytes"""
        blk_size = float(self.attrs.size)
        # Block size is expressed in 512b sectors regardless of
        # underlaying disk structure.
        # See https://goo.gl/L8GZCG for details
        return blk_size * 512

    def dm(self):
        """Return /dev/mapper device name if present"""
        try:
            dm_dev = SysfsDevice(self.sysfsnode, subsys="holders",
                                 sysfsdev_pattern="*[0-9]/dm")
        except KeyError:
            return "[Not mapped]"
        return dm_dev.attrs.name

#
# Tape devices
#

class TapeDevice(SysfsDevice):
    """
    scsi_tape
    """
    def __init__(self, device, subsys='scsi_tape', scsi_device=None):
        SysfsDevice.__init__(self, device, subsys,
                             sysfsdev_pattern=re.compile(r'st[0-9]+'))
        self._scsi_device = scsi_device

    @property
    def scsi_device(self):
        if not self._scsi_device:
            self._scsi_device = SCSIDevice(self.device)
        return self._scsi_device
