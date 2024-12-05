from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PerCls:
	"""Per commands group definition. 34 total commands, 5 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("per", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def audio(self):
		"""audio commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_audio'):
			from .Audio import AudioCls
			self._audio = AudioCls(self._core, self._cmd_group)
		return self._audio

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	@property
	def nmode(self):
		"""nmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmode'):
			from .Nmode import NmodeCls
			self._nmode = NmodeCls(self._core, self._cmd_group)
		return self._nmode

	@property
	def tmode(self):
		"""tmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmode'):
			from .Tmode import TmodeCls
			self._tmode = TmodeCls(self._core, self._cmd_group)
		return self._tmode

	def abort(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: ABORt:BLUetooth:SIGNaling<Instance>:RXQuality:PER \n
		Snippet: driver.rxQuality.per.abort() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'ABORt:BLUetooth:SIGNaling<Instance>:RXQuality:PER', opc_timeout_ms)

	def initiate(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:BLUetooth:SIGNaling<Instance>:RXQuality:PER \n
		Snippet: driver.rxQuality.per.initiate() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:BLUetooth:SIGNaling<Instance>:RXQuality:PER', opc_timeout_ms)

	def stop(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: STOP:BLUetooth:SIGNaling<Instance>:RXQuality:PER \n
		Snippet: driver.rxQuality.per.stop() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:BLUetooth:SIGNaling<Instance>:RXQuality:PER', opc_timeout_ms)

	def clone(self) -> 'PerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
