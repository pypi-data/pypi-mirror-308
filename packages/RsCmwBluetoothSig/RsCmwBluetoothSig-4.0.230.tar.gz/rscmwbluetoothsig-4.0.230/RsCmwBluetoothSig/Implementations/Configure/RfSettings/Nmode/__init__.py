from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NmodeCls:
	"""Nmode commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nmode", core, parent)

	@property
	def hmode(self):
		"""hmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hmode'):
			from .Hmode import HmodeCls
			self._hmode = HmodeCls(self._core, self._cmd_group)
		return self._hmode

	@property
	def mchannel(self):
		"""mchannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mchannel'):
			from .Mchannel import MchannelCls
			self._mchannel = MchannelCls(self._core, self._cmd_group)
		return self._mchannel

	def clone(self) -> 'NmodeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NmodeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
