from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_le_1_m(self) -> enums.SymbolTimeErrorLe:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy[:LE1M] \n
		Snippet: value: enums.SymbolTimeErrorLe = driver.configure.rfSettings.dtx.sing.stError.lowEnergy.get_le_1_m() \n
		Specifies the symbol timing error of the LE signal.
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
			:return: symbol_time_err: OFF | NEG50 | POS50 No symbol timing error, - 50 ppm or 50 ppm
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LE1M?')
		return Conversions.str_to_scalar_enum(response, enums.SymbolTimeErrorLe)

	def set_le_1_m(self, symbol_time_err: enums.SymbolTimeErrorLe) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy[:LE1M] \n
		Snippet: driver.configure.rfSettings.dtx.sing.stError.lowEnergy.set_le_1_m(symbol_time_err = enums.SymbolTimeErrorLe.NEG50) \n
		Specifies the symbol timing error of the LE signal.
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
			:param symbol_time_err: OFF | NEG50 | POS50 No symbol timing error, - 50 ppm or 50 ppm
		"""
		param = Conversions.enum_scalar_to_str(symbol_time_err, enums.SymbolTimeErrorLe)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LE1M {param}')

	# noinspection PyTypeChecker
	def get_lrange(self) -> enums.SymbolTimeErrorLe:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LRANge \n
		Snippet: value: enums.SymbolTimeErrorLe = driver.configure.rfSettings.dtx.sing.stError.lowEnergy.get_lrange() \n
		Specifies the symbol timing error of the LE signal.
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
			:return: symbol_time_err: OFF | NEG50 | POS50 No symbol timing error, - 50 ppm or 50 ppm
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.SymbolTimeErrorLe)

	def set_lrange(self, symbol_time_err: enums.SymbolTimeErrorLe) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LRANge \n
		Snippet: driver.configure.rfSettings.dtx.sing.stError.lowEnergy.set_lrange(symbol_time_err = enums.SymbolTimeErrorLe.NEG50) \n
		Specifies the symbol timing error of the LE signal.
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
			:param symbol_time_err: OFF | NEG50 | POS50 No symbol timing error, - 50 ppm or 50 ppm
		"""
		param = Conversions.enum_scalar_to_str(symbol_time_err, enums.SymbolTimeErrorLe)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LRANge {param}')

	# noinspection PyTypeChecker
	def get_le_2_m(self) -> enums.SymbolTimeErrorLe:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LE2M \n
		Snippet: value: enums.SymbolTimeErrorLe = driver.configure.rfSettings.dtx.sing.stError.lowEnergy.get_le_2_m() \n
		Specifies the symbol timing error of the LE signal.
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
			:return: symbol_time_err: OFF | NEG50 | POS50 No symbol timing error, - 50 ppm or 50 ppm
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LE2M?')
		return Conversions.str_to_scalar_enum(response, enums.SymbolTimeErrorLe)

	def set_le_2_m(self, symbol_time_err: enums.SymbolTimeErrorLe) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LE2M \n
		Snippet: driver.configure.rfSettings.dtx.sing.stError.lowEnergy.set_le_2_m(symbol_time_err = enums.SymbolTimeErrorLe.NEG50) \n
		Specifies the symbol timing error of the LE signal.
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
			:param symbol_time_err: OFF | NEG50 | POS50 No symbol timing error, - 50 ppm or 50 ppm
		"""
		param = Conversions.enum_scalar_to_str(symbol_time_err, enums.SymbolTimeErrorLe)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:LENergy:LE2M {param}')
