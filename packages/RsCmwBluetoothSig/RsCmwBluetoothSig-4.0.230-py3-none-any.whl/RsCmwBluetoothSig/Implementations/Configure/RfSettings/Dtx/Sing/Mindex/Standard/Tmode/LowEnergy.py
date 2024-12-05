from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_lrange(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LRANge \n
		Snippet: value: float or bool = driver.configure.rfSettings.dtx.sing.mindex.standard.tmode.lowEnergy.get_lrange() \n
		Specifies the modulation corruption of the signal. Modulation index of 0.5 means no corruption.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode:
		Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: mod_index: (float or boolean) numeric | ON | OFF Range: 0.4 to 0.6 Additional ON/OFF enables/disables modulation index.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LRANge?')
		return Conversions.str_to_float_or_bool(response)

	def set_lrange(self, mod_index: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LRANge \n
		Snippet: driver.configure.rfSettings.dtx.sing.mindex.standard.tmode.lowEnergy.set_lrange(mod_index = 1.0) \n
		Specifies the modulation corruption of the signal. Modulation index of 0.5 means no corruption.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode:
		Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:param mod_index: (float or boolean) numeric | ON | OFF Range: 0.4 to 0.6 Additional ON/OFF enables/disables modulation index.
		"""
		param = Conversions.decimal_or_bool_value_to_str(mod_index)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LRANge {param}')

	def get_le_2_m(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LE2M \n
		Snippet: value: float or bool = driver.configure.rfSettings.dtx.sing.mindex.standard.tmode.lowEnergy.get_le_2_m() \n
		Specifies the modulation corruption of the signal. Modulation index of 0.5 means no corruption.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode:
		Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: mod_index: (float or boolean) numeric | ON | OFF Range: 0.4 to 0.6 Additional ON/OFF enables/disables modulation index.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LE2M?')
		return Conversions.str_to_float_or_bool(response)

	def set_le_2_m(self, mod_index: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LE2M \n
		Snippet: driver.configure.rfSettings.dtx.sing.mindex.standard.tmode.lowEnergy.set_le_2_m(mod_index = 1.0) \n
		Specifies the modulation corruption of the signal. Modulation index of 0.5 means no corruption.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode:
		Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:param mod_index: (float or boolean) numeric | ON | OFF Range: 0.4 to 0.6 Additional ON/OFF enables/disables modulation index.
		"""
		param = Conversions.decimal_or_bool_value_to_str(mod_index)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LE2M {param}')

	def get_le_1_m(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LE1M \n
		Snippet: value: float or bool = driver.configure.rfSettings.dtx.sing.mindex.standard.tmode.lowEnergy.get_le_1_m() \n
		Specifies the modulation corruption of the signal. Modulation index of 0.5 means no corruption.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode:
		Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: mod_index: (float or boolean) numeric | ON | OFF Range: 0.4 to 0.6 Additional ON/OFF enables/disables modulation index.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LE1M?')
		return Conversions.str_to_float_or_bool(response)

	def set_le_1_m(self, mod_index: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LE1M \n
		Snippet: driver.configure.rfSettings.dtx.sing.mindex.standard.tmode.lowEnergy.set_le_1_m(mod_index = 1.0) \n
		Specifies the modulation corruption of the signal. Modulation index of 0.5 means no corruption.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode:
		Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:param mod_index: (float or boolean) numeric | ON | OFF Range: 0.4 to 0.6 Additional ON/OFF enables/disables modulation index.
		"""
		param = Conversions.decimal_or_bool_value_to_str(mod_index)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:STANdard:TMODe:LENergy:LE1M {param}')
