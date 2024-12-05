from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SingCls:
	"""Sing commands group definition. 51 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sing", core, parent)

	@property
	def mindex(self):
		"""mindex commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_mindex'):
			from .Mindex import MindexCls
			self._mindex = MindexCls(self._core, self._cmd_group)
		return self._mindex

	@property
	def stError(self):
		"""stError commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_stError'):
			from .StError import StErrorCls
			self._stError = StErrorCls(self._core, self._cmd_group)
		return self._stError

	@property
	def fdrift(self):
		"""fdrift commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_fdrift'):
			from .Fdrift import FdriftCls
			self._fdrift = FdriftCls(self._core, self._cmd_group)
		return self._fdrift

	@property
	def foffset(self):
		"""foffset commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_foffset'):
			from .Foffset import FoffsetCls
			self._foffset = FoffsetCls(self._core, self._cmd_group)
		return self._foffset

	def clone(self) -> 'SingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
