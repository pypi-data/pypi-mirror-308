from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BedrCls:
	"""Bedr commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bedr", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Main_State: enums.ResourceState: OFF | RUN | RDY Current state or target state of ongoing state transition OFF: measurement off RUN: measurement running RDY: measurement completed
			- Sync_State: enums.ResourceState: PEND | ADJ PEND: transition to MainState ongoing ADJ: MainState reached
			- Resource_State: enums.ResourceState: QUE | ACT | INV QUE: waiting for resource allocation ACT: resources allocated INV: no resources allocated"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Main_State', enums.ResourceState),
			ArgStruct.scalar_enum('Sync_State', enums.ResourceState),
			ArgStruct.scalar_enum('Resource_State', enums.ResourceState)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Main_State: enums.ResourceState = None
			self.Sync_State: enums.ResourceState = None
			self.Resource_State: enums.ResourceState = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:BER:STATe:ALL[:BEDR] \n
		Snippet: value: FetchStruct = driver.rxQuality.search.ber.state.all.bedr.fetch() \n
		Queries the main measurement state and the measurement substates. A really running measurement returns RUN, ADJ, ACT. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:BER:STATe:ALL:BEDR?', self.__class__.FetchStruct())
