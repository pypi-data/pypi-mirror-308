from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxQualityCls:
	"""RxQuality commands group definition. 156 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rxQuality", core, parent)

	@property
	def iqDrange(self):
		"""iqDrange commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_iqDrange'):
			from .IqDrange import IqDrangeCls
			self._iqDrange = IqDrangeCls(self._core, self._cmd_group)
		return self._iqDrange

	@property
	def iqCoherency(self):
		"""iqCoherency commands group. 2 Sub-classes, 4 commands."""
		if not hasattr(self, '_iqCoherency'):
			from .IqCoherency import IqCoherencyCls
			self._iqCoherency = IqCoherencyCls(self._core, self._cmd_group)
		return self._iqCoherency

	@property
	def search(self):
		"""search commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_search'):
			from .Search import SearchCls
			self._search = SearchCls(self._core, self._cmd_group)
		return self._search

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

	@property
	def trace(self):
		"""trace commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import TraceCls
			self._trace = TraceCls(self._core, self._cmd_group)
		return self._trace

	def clone(self) -> 'RxQualityCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxQualityCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
