from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SearchCls:
	"""Search commands group definition. 42 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("search", core, parent)

	@property
	def per(self):
		"""per commands group. 5 Sub-classes, 3 commands."""
		if not hasattr(self, '_per'):
			from .Per import PerCls
			self._per = PerCls(self._core, self._cmd_group)
		return self._per

	@property
	def ber(self):
		"""ber commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ber'):
			from .Ber import BerCls
			self._ber = BerCls(self._core, self._cmd_group)
		return self._ber

	def clone(self) -> 'SearchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SearchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
