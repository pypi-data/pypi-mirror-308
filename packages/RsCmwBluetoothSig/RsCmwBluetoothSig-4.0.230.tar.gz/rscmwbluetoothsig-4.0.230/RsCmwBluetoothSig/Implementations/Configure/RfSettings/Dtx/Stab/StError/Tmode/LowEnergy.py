from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_lrange(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:TMODe:LENergy:LRANge \n
		Snippet: value: List[int] = driver.configure.rfSettings.dtx.stab.stError.tmode.lowEnergy.get_lrange() \n
		Return the symbol timing error under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values for BR and LE, 3 values for EDR) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless
		technology, see also 'Dirty TX Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: symbol_time_err: decimal Range: - 50 ppm to 50 ppm, for BR/EDR: - 20 ppm to 20 ppm , Unit: ppm
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:TMODe:LENergy:LRANge?')
		return response

	def get_le_2_m(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:TMODe:LENergy:LE2M \n
		Snippet: value: List[int] = driver.configure.rfSettings.dtx.stab.stError.tmode.lowEnergy.get_le_2_m() \n
		Return the symbol timing error under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values for BR and LE, 3 values for EDR) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless
		technology, see also 'Dirty TX Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: symbol_time_err: decimal Range: - 50 ppm to 50 ppm, for BR/EDR: - 20 ppm to 20 ppm , Unit: ppm
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:TMODe:LENergy:LE2M?')
		return response

	def get_le_1_m(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:TMODe:LENergy:LE1M \n
		Snippet: value: List[int] = driver.configure.rfSettings.dtx.stab.stError.tmode.lowEnergy.get_le_1_m() \n
		Return the symbol timing error under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values for BR and LE, 3 values for EDR) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless
		technology, see also 'Dirty TX Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: symbol_time_err: decimal Range: - 50 ppm to 50 ppm, for BR/EDR: - 20 ppm to 20 ppm , Unit: ppm
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:TMODe:LENergy:LE1M?')
		return response
