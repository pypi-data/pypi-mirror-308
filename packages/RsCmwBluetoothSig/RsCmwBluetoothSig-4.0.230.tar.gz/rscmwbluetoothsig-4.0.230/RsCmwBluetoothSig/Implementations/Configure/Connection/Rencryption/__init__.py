from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RencryptionCls:
	"""Rencryption commands group definition. 2 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rencryption", core, parent)

	@property
	def leSignaling(self):
		"""leSignaling commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_leSignaling'):
			from .LeSignaling import LeSignalingCls
			self._leSignaling = LeSignalingCls(self._core, self._cmd_group)
		return self._leSignaling

	def clone(self) -> 'RencryptionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RencryptionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
