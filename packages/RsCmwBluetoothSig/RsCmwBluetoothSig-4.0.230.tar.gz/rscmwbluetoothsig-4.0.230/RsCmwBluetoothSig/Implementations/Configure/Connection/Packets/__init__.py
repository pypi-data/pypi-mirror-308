from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PacketsCls:
	"""Packets commands group definition. 21 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("packets", core, parent)

	@property
	def ptype(self):
		"""ptype commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_ptype'):
			from .Ptype import PtypeCls
			self._ptype = PtypeCls(self._core, self._cmd_group)
		return self._ptype

	@property
	def packetLength(self):
		"""packetLength commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_packetLength'):
			from .PacketLength import PacketLengthCls
			self._packetLength = PacketLengthCls(self._core, self._cmd_group)
		return self._packetLength

	@property
	def pattern(self):
		"""pattern commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def units(self):
		"""units commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_units'):
			from .Units import UnitsCls
			self._units = UnitsCls(self._core, self._cmd_group)
		return self._units

	@property
	def typePy(self):
		"""typePy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'PacketsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PacketsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
