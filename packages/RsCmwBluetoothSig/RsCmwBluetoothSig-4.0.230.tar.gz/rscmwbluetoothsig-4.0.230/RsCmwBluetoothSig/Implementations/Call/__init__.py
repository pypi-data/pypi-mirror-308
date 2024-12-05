from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CallCls:
	"""Call commands group definition. 8 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("call", core, parent)

	@property
	def hciCustom(self):
		"""hciCustom commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hciCustom'):
			from .HciCustom import HciCustomCls
			self._hciCustom = HciCustomCls(self._core, self._cmd_group)
		return self._hciCustom

	@property
	def dtMode(self):
		"""dtMode commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtMode'):
			from .DtMode import DtModeCls
			self._dtMode = DtModeCls(self._core, self._cmd_group)
		return self._dtMode

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	@property
	def connection(self):
		"""connection commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_connection'):
			from .Connection import ConnectionCls
			self._connection = ConnectionCls(self._core, self._cmd_group)
		return self._connection

	def clone(self) -> 'CallCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CallCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
