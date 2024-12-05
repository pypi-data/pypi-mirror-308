from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqDrangeCls:
	"""IqDrange commands group definition. 35 total commands, 3 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqDrange", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	@property
	def antMeanAmp(self):
		"""antMeanAmp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_antMeanAmp'):
			from .AntMeanAmp import AntMeanAmpCls
			self._antMeanAmp = AntMeanAmpCls(self._core, self._cmd_group)
		return self._antMeanAmp

	def initiate(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange \n
		Snippet: driver.rxQuality.iqDrange.initiate() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange', opc_timeout_ms)

	def stop(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: STOP:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange \n
		Snippet: driver.rxQuality.iqDrange.stop() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange', opc_timeout_ms)

	def abort(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: ABORt:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange \n
		Snippet: driver.rxQuality.iqDrange.abort() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'ABORt:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange', opc_timeout_ms)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.ResourceState:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange \n
		Snippet: value: enums.ResourceState = driver.rxQuality.iqDrange.fetch() \n
		No command help available \n
			:return: meas_status: No help available"""
		response = self._core.io.query_str(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange?')
		return Conversions.str_to_scalar_enum(response, enums.ResourceState)

	def clone(self) -> 'IqDrangeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqDrangeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
