from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllCls:
	"""All commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("all", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Main_State: bool: OFF | ON OFF: Generator switched off ON: Generator has been turned on
			- Sub_State: enums.ConnectionState: OFF | SBY | INQuiring | SINQuiry | CNNecting | SCONnecting | CONNected | DETaching | TCNNecting | TCONected | ECRunning | ECNNecting | ECONected | EXEMode | ENEMode | HFCNnecting | HFConnected | EXHFp | ENHFp | AGCNnecting | AGConnected | EXAGmode | ENAGmode | ENHSmode | EXHSmode | CNASmode | CHASmode | DHASmode | EHASmode | XHASmode | SMIDle | SMCNnecting | SMConnected | SMDetaching | HSCNnecting | HSConnected | HSDetaching | A2CNnecting | A2Connected | A2Detaching | A2SNnecting | A2SCnnected | A2SDetaching | ACNNecting | ACONected | AEXMode | AENMode Signaling states of the R&S CMW for BR/EDR: OFF: not connected SBY: standby INQuiring: inquiring SINQuiry: stopping inquiry CNNecting: connecting SCONnecting: stop connecting CONNected: connected DETaching: detaching TCNNecting: test mode - connecting TCONnected: test mode - connected ECRunning: EUT controller running ECNNecting: echo mode - connecting ECONected: echo mode - connected EXEMode: echo mode - exiting ENEMode: echo mode - entering HFCNnecting: hands-free profile - connecting HFConnected: hands-free profile - connected EXHFp: hands-free profile - exiting ENHFp: hands-free profile - entering AGCNnecting: hands-free audio gateway profile - connecting AGConnected: hands-free audio gateway profile - connected EXAGmode: hands-free audio gateway profile - exiting ENAGmode: hands-free audio gateway profile - entering CNASmode: hands-free audio gateway (slave mode) - connecting CHASmode: hands-free audio gateway (slave mode) - connected DHASmode: hands-free audio gateway (slave mode) - detaching EHASmode: hands-free audio gateway (slave mode) - entering XHASmode: hands-free audio gateway (slave mode) - exiting SMIDle: slave mode - idle SMCNnecting: slave mode - connecting SMConnected: slave mode - connected SMDetaching: slave mode - detaching HSCNnecting: hands-free profile (slave mode) - connecting HSConnected: hands-free profile (slave mode) - connected ENHSmode: hands-free profile (slave mode) - entering EXHSmode: hands-free profile (slave mode) - exiting HSDetaching: hands-free profile (slave mode) - detaching A2CNnecting: A2DP - connecting A2Connected: A2DP - connected A2Detaching: A2DP - detaching A2SNnecting: A2DP (slave mode) - connecting A2SCnnected: A2DP (slave mode) - connected A2SDetaching: A2DP (slave mode) - detaching ACNNecting: audio - connecting ACONected: audio - connected AEXMode: audio - exiting AENMode: audio - entering For a detailed description of the available states and state transitions, see 'Signaling states'."""
		__meta_args_list = [
			ArgStruct.scalar_bool('Main_State'),
			ArgStruct.scalar_enum('Sub_State', enums.ConnectionState)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Main_State: bool = None
			self.Sub_State: enums.ConnectionState = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:CONNection:STATe:ALL \n
		Snippet: value: FetchStruct = driver.connection.state.all.fetch() \n
		Returns detailed information about the 'Bluetooth Signaling' generator state related to BR/EDR. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:CONNection:STATe:ALL?', self.__class__.FetchStruct())
