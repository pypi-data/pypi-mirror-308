from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BerCls:
	"""Ber commands group definition. 8 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ber", core, parent)

	@property
	def state(self):
		"""state commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def bedr(self):
		"""bedr commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_bedr'):
			from .Bedr import BedrCls
			self._bedr = BedrCls(self._core, self._cmd_group)
		return self._bedr

	def clone(self) -> 'BerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
