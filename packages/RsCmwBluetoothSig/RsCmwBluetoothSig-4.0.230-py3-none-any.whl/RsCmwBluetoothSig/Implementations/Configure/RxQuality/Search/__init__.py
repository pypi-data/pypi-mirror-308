from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SearchCls:
	"""Search commands group definition. 38 total commands, 4 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("search", core, parent)

	@property
	def step(self):
		"""step commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Step import StepCls
			self._step = StepCls(self._core, self._cmd_group)
		return self._step

	@property
	def packets(self):
		"""packets commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_packets'):
			from .Packets import PacketsCls
			self._packets = PacketsCls(self._core, self._cmd_group)
		return self._packets

	@property
	def limit(self):
		"""limit commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	@property
	def rintegrity(self):
		"""rintegrity commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rintegrity'):
			from .Rintegrity import RintegrityCls
			self._rintegrity = RintegrityCls(self._core, self._cmd_group)
		return self._rintegrity

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:TOUT \n
		Snippet: value: float = driver.configure.rxQuality.search.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually. When the measurement has completed the first measurement
		cycle (first single shot) , the statistical depth is reached and the timer is reset. If the first measurement cycle has
		not been completed when the timer expires, the measurement is stopped. The measurement state changes to RDY.
		The reliability indicator is set to 1, indicating that a measurement timeout occurred. Still running READ, FETCh or
		CALCulate commands are completed, returning the available results. At least for some results, there are no values at all
		or the statistical depth has not been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: timeout: numeric Unit: s
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, timeout: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:TOUT \n
		Snippet: driver.configure.rxQuality.search.set_timeout(timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually. When the measurement has completed the first measurement
		cycle (first single shot) , the statistical depth is reached and the timer is reset. If the first measurement cycle has
		not been completed when the timer expires, the measurement is stopped. The measurement state changes to RDY.
		The reliability indicator is set to 1, indicating that a measurement timeout occurred. Still running READ, FETCh or
		CALCulate commands are completed, returning the available results. At least for some results, there are no values at all
		or the statistical depth has not been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param timeout: numeric Unit: s
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:TOUT {param}')

	def clone(self) -> 'SearchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SearchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
