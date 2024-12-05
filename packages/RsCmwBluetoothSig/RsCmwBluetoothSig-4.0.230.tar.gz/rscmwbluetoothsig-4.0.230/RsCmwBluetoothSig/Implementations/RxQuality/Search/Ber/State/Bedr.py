from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BedrCls:
	"""Bedr commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bedr", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.ResourceState:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:BER:STATe[:BEDR] \n
		Snippet: value: enums.ResourceState = driver.rxQuality.search.ber.state.bedr.fetch() \n
		Queries the main measurement state. Use FETCh:...:STATe:ALL? to query the measurement state including the substates. The
		substates tell you, for example, whether a state transition is ongoing. \n
			:return: meas_status: OFF | RUN | RDY Current state or target state of ongoing state transition OFF: measurement off RUN: measurement running RDY: measurement completed"""
		response = self._core.io.query_str(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:BER:STATe:BEDR?')
		return Conversions.str_to_scalar_enum(response, enums.ResourceState)
