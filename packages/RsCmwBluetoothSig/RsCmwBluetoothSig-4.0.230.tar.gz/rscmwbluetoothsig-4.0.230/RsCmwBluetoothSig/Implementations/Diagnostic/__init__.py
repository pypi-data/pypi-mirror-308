from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DiagnosticCls:
	"""Diagnostic commands group definition. 22 total commands, 6 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("diagnostic", core, parent)

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def le(self):
		"""le commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_le'):
			from .Le import LeCls
			self._le = LeCls(self._core, self._cmd_group)
		return self._le

	@property
	def ucs(self):
		"""ucs commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_ucs'):
			from .Ucs import UcsCls
			self._ucs = UcsCls(self._core, self._cmd_group)
		return self._ucs

	@property
	def debug(self):
		"""debug commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_debug'):
			from .Debug import DebugCls
			self._debug = DebugCls(self._core, self._cmd_group)
		return self._debug

	@property
	def connection(self):
		"""connection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_connection'):
			from .Connection import ConnectionCls
			self._connection = ConnectionCls(self._core, self._cmd_group)
		return self._connection

	@property
	def rxQuality(self):
		"""rxQuality commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxQuality'):
			from .RxQuality import RxQualityCls
			self._rxQuality = RxQualityCls(self._core, self._cmd_group)
		return self._rxQuality

	def get_wcmap(self) -> int:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:WCMap \n
		Snippet: value: int = driver.diagnostic.get_wcmap() \n
		No command help available \n
			:return: wait_con_intervals: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:WCMap?')
		return Conversions.str_to_int(response)

	def set_wcmap(self, wait_con_intervals: int) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:WCMap \n
		Snippet: driver.diagnostic.set_wcmap(wait_con_intervals = 1) \n
		No command help available \n
			:param wait_con_intervals: No help available
		"""
		param = Conversions.decimal_value_to_str(wait_con_intervals)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:WCMap {param}')

	def clone(self) -> 'DiagnosticCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DiagnosticCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
