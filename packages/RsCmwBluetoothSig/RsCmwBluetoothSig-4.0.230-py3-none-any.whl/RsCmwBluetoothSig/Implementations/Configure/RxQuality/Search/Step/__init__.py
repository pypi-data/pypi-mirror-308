from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StepCls:
	"""Step commands group definition. 5 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("step", core, parent)

	@property
	def audio(self):
		"""audio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_audio'):
			from .Audio import AudioCls
			self._audio = AudioCls(self._core, self._cmd_group)
		return self._audio

	@property
	def tmode(self):
		"""tmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmode'):
			from .Tmode import TmodeCls
			self._tmode = TmodeCls(self._core, self._cmd_group)
		return self._tmode

	@property
	def nmode(self):
		"""nmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nmode'):
			from .Nmode import NmodeCls
			self._nmode = NmodeCls(self._core, self._cmd_group)
		return self._nmode

	def get_bredr(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:BREDr \n
		Snippet: value: float or bool = driver.configure.rxQuality.search.step.get_bredr() \n
		Specifies the power step for the BR/EDR search iteration of BER search measurements. \n
			:return: level_step: (float or boolean) numeric Range: 0.01 dBm to 5 dBm, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:BREDr?')
		return Conversions.str_to_float_or_bool(response)

	def set_bredr(self, level_step: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:BREDr \n
		Snippet: driver.configure.rxQuality.search.step.set_bredr(level_step = 1.0) \n
		Specifies the power step for the BR/EDR search iteration of BER search measurements. \n
			:param level_step: (float or boolean) numeric Range: 0.01 dBm to 5 dBm, Unit: dB
		"""
		param = Conversions.decimal_or_bool_value_to_str(level_step)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:BREDr {param}')

	def get_low_energy(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:LENergy \n
		Snippet: value: float or bool = driver.configure.rxQuality.search.step.get_low_energy() \n
		Specifies the power step for the LE search iteration of PER search measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- For LE connection tests (normal mode) , command for LE 1M PHY - uncoded (..:NMODe:LENergy:LE1M..) is available.
			- For LE UTP test mode, command ..:SEARch:STEP:TMODe:LENergy.. is available.
			- For LE RF tests (direct test mode) , command ..:SEARch:STEP:LENergy.. is available.
			- For LE audio, command ..:SEARch:STEP:AUDio:LENergy.. is available. \n
			:return: level_step: (float or boolean) numeric Range: 0.01 dB to 5 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:LENergy?')
		return Conversions.str_to_float_or_bool(response)

	def set_low_energy(self, level_step: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:LENergy \n
		Snippet: driver.configure.rxQuality.search.step.set_low_energy(level_step = 1.0) \n
		Specifies the power step for the LE search iteration of PER search measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- For LE connection tests (normal mode) , command for LE 1M PHY - uncoded (..:NMODe:LENergy:LE1M..) is available.
			- For LE UTP test mode, command ..:SEARch:STEP:TMODe:LENergy.. is available.
			- For LE RF tests (direct test mode) , command ..:SEARch:STEP:LENergy.. is available.
			- For LE audio, command ..:SEARch:STEP:AUDio:LENergy.. is available. \n
			:param level_step: (float or boolean) numeric Range: 0.01 dB to 5 dB, Unit: dB
		"""
		param = Conversions.decimal_or_bool_value_to_str(level_step)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:LENergy {param}')

	def clone(self) -> 'StepCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StepCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
