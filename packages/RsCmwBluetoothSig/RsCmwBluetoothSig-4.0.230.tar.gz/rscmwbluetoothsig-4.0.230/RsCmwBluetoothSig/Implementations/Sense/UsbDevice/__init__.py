from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UsbDeviceCls:
	"""UsbDevice commands group definition. 8 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("usbDevice", core, parent)

	@property
	def information(self):
		"""information commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_information'):
			from .Information import InformationCls
			self._information = InformationCls(self._core, self._cmd_group)
		return self._information

	def clone(self) -> 'UsbDeviceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UsbDeviceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
