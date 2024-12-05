from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.LeSignalingState:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:LENergy:STATe \n
		Snippet: value: enums.LeSignalingState = driver.lowEnergy.state.fetch() \n
		Returns the signaling state of the R&S CMW for LE direct test connections. \n
			:return: state: IDLE | OFF | SPCM | STCM | CMR | STTX | TXRunning | SPTX | STRX | RXRunning | SPRX | RCOM IDLE: Connected in direct test mode, no active test running OFF: Not connected in direct test mode SPCM: Stopping communication test STCM: Starting communication test CMR: Communication test running STTX: Starting TX test TXRunning: TX test running SPTX: Stopping TX test STRX: Starting RX test RXRunning: RX test running SPRX: Stopping RX test RCOM: Refreshing COM port list"""
		response = self._core.io.query_str(f'FETCh:BLUetooth:SIGNaling<Instance>:LENergy:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.LeSignalingState)
