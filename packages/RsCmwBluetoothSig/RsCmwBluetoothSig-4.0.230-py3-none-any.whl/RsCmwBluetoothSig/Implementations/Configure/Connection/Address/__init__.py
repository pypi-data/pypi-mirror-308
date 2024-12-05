from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AddressCls:
	"""Address commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("address", core, parent)

	@property
	def cmw(self):
		"""cmw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmw'):
			from .Cmw import CmwCls
			self._cmw = CmwCls(self._core, self._cmd_group)
		return self._cmw

	@property
	def eut(self):
		"""eut commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eut'):
			from .Eut import EutCls
			self._eut = EutCls(self._core, self._cmd_group)
		return self._eut

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'AddressCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AddressCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
