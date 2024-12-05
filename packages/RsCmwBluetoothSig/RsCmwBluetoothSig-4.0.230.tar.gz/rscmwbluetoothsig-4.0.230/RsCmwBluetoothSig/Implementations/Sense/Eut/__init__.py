from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EutCls:
	"""Eut commands group definition. 23 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eut", core, parent)

	@property
	def capability(self):
		"""capability commands group. 1 Sub-classes, 10 commands."""
		if not hasattr(self, '_capability'):
			from .Capability import CapabilityCls
			self._capability = CapabilityCls(self._core, self._cmd_group)
		return self._capability

	@property
	def information(self):
		"""information commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_information'):
			from .Information import InformationCls
			self._information = InformationCls(self._core, self._cmd_group)
		return self._information

	@property
	def csettings(self):
		"""csettings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csettings'):
			from .Csettings import CsettingsCls
			self._csettings = CsettingsCls(self._core, self._cmd_group)
		return self._csettings

	@property
	def powerControl(self):
		"""powerControl commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_powerControl'):
			from .PowerControl import PowerControlCls
			self._powerControl = PowerControlCls(self._core, self._cmd_group)
		return self._powerControl

	def clone(self) -> 'EutCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EutCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
