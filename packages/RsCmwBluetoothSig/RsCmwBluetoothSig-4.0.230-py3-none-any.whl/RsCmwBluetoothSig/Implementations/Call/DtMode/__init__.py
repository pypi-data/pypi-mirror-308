from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DtModeCls:
	"""DtMode commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dtMode", core, parent)

	@property
	def endTx(self):
		"""endTx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_endTx'):
			from .EndTx import EndTxCls
			self._endTx = EndTxCls(self._core, self._cmd_group)
		return self._endTx

	@property
	def startTx(self):
		"""startTx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_startTx'):
			from .StartTx import StartTxCls
			self._startTx = StartTxCls(self._core, self._cmd_group)
		return self._startTx

	def clone(self) -> 'DtModeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DtModeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
