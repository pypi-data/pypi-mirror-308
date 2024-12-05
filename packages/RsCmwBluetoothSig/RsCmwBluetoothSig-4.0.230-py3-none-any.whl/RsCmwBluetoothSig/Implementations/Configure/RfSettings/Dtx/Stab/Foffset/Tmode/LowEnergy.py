from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_lrange(self) -> List[int or bool]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:FOFFset:TMODe:LENergy:LRANge \n
		Snippet: value: List[int or bool] = driver.configure.rfSettings.dtx.stab.foffset.tmode.lowEnergy.get_lrange() \n
		Return the frequency offset under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values for BR and LE, 3 values for EDR) .
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
			:return: freq_offset: (integer or boolean items) decimal | ON | OFF Range: -250 kHz to 250 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:FOFFset:TMODe:LENergy:LRANge?')
		return Conversions.str_to_int_or_bool_list(response)

	def get_le_2_m(self) -> List[int or bool]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:FOFFset:TMODe:LENergy:LE2M \n
		Snippet: value: List[int or bool] = driver.configure.rfSettings.dtx.stab.foffset.tmode.lowEnergy.get_le_2_m() \n
		Return the frequency offset under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values for BR and LE, 3 values for EDR) .
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
			:return: freq_offset: (integer or boolean items) decimal | ON | OFF Range: -250 kHz to 250 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:FOFFset:TMODe:LENergy:LE2M?')
		return Conversions.str_to_int_or_bool_list(response)

	def get_le_1_m(self) -> List[int or bool]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:FOFFset:TMODe:LENergy:LE1M \n
		Snippet: value: List[int or bool] = driver.configure.rfSettings.dtx.stab.foffset.tmode.lowEnergy.get_le_1_m() \n
		Return the frequency offset under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values for BR and LE, 3 values for EDR) .
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
			:return: freq_offset: (integer or boolean items) decimal | ON | OFF Range: -250 kHz to 250 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:FOFFset:TMODe:LENergy:LE1M?')
		return Conversions.str_to_int_or_bool_list(response)
