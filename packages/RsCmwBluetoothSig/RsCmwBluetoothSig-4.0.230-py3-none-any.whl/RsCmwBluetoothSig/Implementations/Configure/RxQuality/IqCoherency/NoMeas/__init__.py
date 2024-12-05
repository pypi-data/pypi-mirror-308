from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NoMeasCls:
	"""NoMeas commands group definition. 8 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("noMeas", core, parent)

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	def clone(self) -> 'NoMeasCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NoMeasCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
