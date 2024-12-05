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
	def get_lrange(self) -> enums.DtxMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LRANge \n
		Snippet: value: enums.DtxMode = driver.configure.rfSettings.dtx.mode.tmode.lowEnergy.get_lrange() \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.DtxMode)

	def set_lrange(self, dtx_mode: enums.DtxMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LRANge \n
		Snippet: driver.configure.rfSettings.dtx.mode.tmode.lowEnergy.set_lrange(dtx_mode = enums.DtxMode.SINGle) \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:param dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		param = Conversions.enum_scalar_to_str(dtx_mode, enums.DtxMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LRANge {param}')

	# noinspection PyTypeChecker
	def get_le_2_m(self) -> enums.DtxMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LE2M \n
		Snippet: value: enums.DtxMode = driver.configure.rfSettings.dtx.mode.tmode.lowEnergy.get_le_2_m() \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LE2M?')
		return Conversions.str_to_scalar_enum(response, enums.DtxMode)

	def set_le_2_m(self, dtx_mode: enums.DtxMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LE2M \n
		Snippet: driver.configure.rfSettings.dtx.mode.tmode.lowEnergy.set_le_2_m(dtx_mode = enums.DtxMode.SINGle) \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:param dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		param = Conversions.enum_scalar_to_str(dtx_mode, enums.DtxMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LE2M {param}')

	# noinspection PyTypeChecker
	def get_le_1_m(self) -> enums.DtxMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LE1M \n
		Snippet: value: enums.DtxMode = driver.configure.rfSettings.dtx.mode.tmode.lowEnergy.get_le_1_m() \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LE1M?')
		return Conversions.str_to_scalar_enum(response, enums.DtxMode)

	def set_le_1_m(self, dtx_mode: enums.DtxMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LE1M \n
		Snippet: driver.configure.rfSettings.dtx.mode.tmode.lowEnergy.set_le_1_m(dtx_mode = enums.DtxMode.SINGle) \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:param dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		param = Conversions.enum_scalar_to_str(dtx_mode, enums.DtxMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:TMODe:LENergy:LE1M {param}')
