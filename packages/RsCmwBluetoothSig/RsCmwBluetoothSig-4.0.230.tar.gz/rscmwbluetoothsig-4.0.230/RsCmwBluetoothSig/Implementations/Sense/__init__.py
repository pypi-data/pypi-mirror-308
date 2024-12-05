from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SenseCls:
	"""Sense commands group definition. 35 total commands, 4 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sense", core, parent)

	@property
	def usbDevice(self):
		"""usbDevice commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_usbDevice'):
			from .UsbDevice import UsbDeviceCls
			self._usbDevice = UsbDeviceCls(self._core, self._cmd_group)
		return self._usbDevice

	@property
	def eut(self):
		"""eut commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_eut'):
			from .Eut import EutCls
			self._eut = EutCls(self._core, self._cmd_group)
		return self._eut

	@property
	def connection(self):
		"""connection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_connection'):
			from .Connection import ConnectionCls
			self._connection = ConnectionCls(self._core, self._cmd_group)
		return self._connection

	@property
	def elogging(self):
		"""elogging commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_elogging'):
			from .Elogging import EloggingCls
			self._elogging = EloggingCls(self._core, self._cmd_group)
		return self._elogging

	def get_cmap(self) -> List[int]:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:CMAP \n
		Snippet: value: List[int] = driver.sense.get_cmap() \n
		Queries channels used by adaptive frequency hopping (AFH) . \n
			:return: afh_channel_map: decimal 79 comma-separated values, one value per channel: 0: channel is blocked for AFH 1: channel is released for AFH Range: 0 to 1
		"""
		response = self._core.io.query_bin_or_ascii_int_list('SENSe:BLUetooth:SIGNaling<Instance>:CMAP?')
		return response

	def clone(self) -> 'SenseCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SenseCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
