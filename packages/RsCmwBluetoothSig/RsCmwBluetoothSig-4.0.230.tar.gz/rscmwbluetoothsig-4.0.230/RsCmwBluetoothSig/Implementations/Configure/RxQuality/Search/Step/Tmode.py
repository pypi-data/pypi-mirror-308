from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TmodeCls:
	"""Tmode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tmode", core, parent)

	def get_low_energy(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:TMODe:LENergy \n
		Snippet: value: float or bool = driver.configure.rxQuality.search.step.tmode.get_low_energy() \n
		Specifies the power step for the LE search iteration of PER search measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- For LE connection tests (normal mode) , command for LE 1M PHY - uncoded (..:NMODe:LENergy:LE1M..) is available.
			- For LE UTP test mode, command ..:SEARch:STEP:TMODe:LENergy.. is available.
			- For LE RF tests (direct test mode) , command ..:SEARch:STEP:LENergy.. is available.
			- For LE audio, command ..:SEARch:STEP:AUDio:LENergy.. is available. \n
			:return: level_step: (float or boolean) numeric Range: 0.01 dB to 5 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:TMODe:LENergy?')
		return Conversions.str_to_float_or_bool(response)

	def set_low_energy(self, level_step: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:TMODe:LENergy \n
		Snippet: driver.configure.rxQuality.search.step.tmode.set_low_energy(level_step = 1.0) \n
		Specifies the power step for the LE search iteration of PER search measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- For LE connection tests (normal mode) , command for LE 1M PHY - uncoded (..:NMODe:LENergy:LE1M..) is available.
			- For LE UTP test mode, command ..:SEARch:STEP:TMODe:LENergy.. is available.
			- For LE RF tests (direct test mode) , command ..:SEARch:STEP:LENergy.. is available.
			- For LE audio, command ..:SEARch:STEP:AUDio:LENergy.. is available. \n
			:param level_step: (float or boolean) numeric Range: 0.01 dB to 5 dB, Unit: dB
		"""
		param = Conversions.decimal_or_bool_value_to_str(level_step)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:TMODe:LENergy {param}')
