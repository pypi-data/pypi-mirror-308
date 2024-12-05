from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqCoherencyCls:
	"""IqCoherency commands group definition. 20 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqCoherency", core, parent)

	@property
	def moException(self):
		"""moException commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_moException'):
			from .MoException import MoExceptionCls
			self._moException = MoExceptionCls(self._core, self._cmd_group)
		return self._moException

	@property
	def noMeas(self):
		"""noMeas commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_noMeas'):
			from .NoMeas import NoMeasCls
			self._noMeas = NoMeasCls(self._core, self._cmd_group)
		return self._noMeas

	@property
	def packets(self):
		"""packets commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_packets'):
			from .Packets import PacketsCls
			self._packets = PacketsCls(self._core, self._cmd_group)
		return self._packets

	@property
	def limit(self):
		"""limit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	def clone(self) -> 'IqCoherencyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqCoherencyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
