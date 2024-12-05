from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le1MCls:
	"""Le1M commands group definition. 12 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le1M", core, parent)

	@property
	def a0Reference(self):
		"""a0Reference commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_a0Reference'):
			from .A0Reference import A0ReferenceCls
			self._a0Reference = A0ReferenceCls(self._core, self._cmd_group)
		return self._a0Reference

	@property
	def a1Nreference(self):
		"""a1Nreference commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_a1Nreference'):
			from .A1Nreference import A1NreferenceCls
			self._a1Nreference = A1NreferenceCls(self._core, self._cmd_group)
		return self._a1Nreference

	@property
	def a2Nreference(self):
		"""a2Nreference commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_a2Nreference'):
			from .A2Nreference import A2NreferenceCls
			self._a2Nreference = A2NreferenceCls(self._core, self._cmd_group)
		return self._a2Nreference

	@property
	def a3Nreference(self):
		"""a3Nreference commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_a3Nreference'):
			from .A3Nreference import A3NreferenceCls
			self._a3Nreference = A3NreferenceCls(self._core, self._cmd_group)
		return self._a3Nreference

	def clone(self) -> 'Le1MCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Le1MCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
