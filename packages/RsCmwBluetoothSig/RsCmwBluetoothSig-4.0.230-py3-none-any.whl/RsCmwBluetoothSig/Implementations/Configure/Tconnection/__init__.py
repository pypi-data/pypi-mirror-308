from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TconnectionCls:
	"""Tconnection commands group definition. 9 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tconnection", core, parent)

	@property
	def interval(self):
		"""interval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interval'):
			from .Interval import IntervalCls
			self._interval = IntervalCls(self._core, self._cmd_group)
		return self._interval

	@property
	def packets(self):
		"""packets commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_packets'):
			from .Packets import PacketsCls
			self._packets = PacketsCls(self._core, self._cmd_group)
		return self._packets

	@property
	def phy(self):
		"""phy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phy'):
			from .Phy import PhyCls
			self._phy = PhyCls(self._core, self._cmd_group)
		return self._phy

	@property
	def fec(self):
		"""fec commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fec'):
			from .Fec import FecCls
			self._fec = FecCls(self._core, self._cmd_group)
		return self._fec

	def clone(self) -> 'TconnectionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TconnectionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
