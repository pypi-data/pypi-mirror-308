from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def leSignaling(self):
		"""leSignaling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_leSignaling'):
			from .LeSignaling import LeSignalingCls
			self._leSignaling = LeSignalingCls(self._core, self._cmd_group)
		return self._leSignaling

	# noinspection PyTypeChecker
	def fetch(self) -> enums.ConnectionState:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:CONNection:STATe \n
		Snippet: value: enums.ConnectionState = driver.connection.state.fetch() \n
		Returns the signaling state of the R&S CMW related to BR/EDR. State changes are initiated using the method
		RsCmwBluetoothSig.Call.Connection.Action.value command. \n
			:return: state: OFF | SBY | INQuiring | SINQuiry | CNNecting | SCONnecting | CONNected | DETaching | TCNNecting | TCONected | ECRunning | ECNNecting | ECONected | EXEMode | ENEMode | HFCNnecting | HFConnected | EXHFp | ENHFp | AGCNnecting | AGConnected | EXAGmode | ENAGmode | ENHSmode | EXHSmode | CNASmode | CHASmode | DHASmode | EHASmode | XHASmode | SMIDle | SMCNnecting | SMConnected | SMDetaching | HSCNnecting | HSConnected | HSDetaching | A2CNnecting | A2Connected | A2Detaching | A2SNnecting | A2SCnnected | A2SDetaching | ACNNecting | ACONected | AEXMode | AENMode OFF: not connected SBY: standby INQuiring: inquiring SINQuiry: stopping inquiry CNNecting: connecting SCONnecting: stop connecting CONNected: connected DETaching: detaching TCNNecting: test mode - connecting TCONnected: test mode - connected ECRunning: EUT controller running ECNNecting: echo mode - connecting ECONected: echo mode - connected EXEMode: echo mode - exiting ENEMode: echo mode - entering HFCNnecting: hands-free profile - connecting HFConnected: hands-free profile - connected EXHFp: hands-free profile - exiting ENHFp: hands-free profile - entering AGCNnecting: hands-free audio gateway profile - connecting AGConnected: hands-free audio gateway profile - connected EXAGmode: hands-free audio gateway profile - exiting ENAGmode: hands-free audio gateway profile - entering CNASmode: hands-free audio gateway (slave mode) - connecting CHASmode: hands-free audio gateway (slave mode) - connected DHASmode: hands-free audio gateway (slave mode) - detaching EHASmode: hands-free audio gateway (slave mode) - entering XHASmode: hands-free audio gateway (slave mode) - exiting SMIDle: slave mode - idle SMCNnecting: slave mode - connecting SMConnected: slave mode - connected SMDetaching: slave mode - detaching HSCNnecting: hands-free profile (slave mode) - connecting HSConnected: hands-free profile (slave mode) - connected ENHSmode: hands-free profile (slave mode) - entering EXHSmode: hands-free profile (slave mode) - exiting HSDetaching: hands-free profile (slave mode) - detaching A2CNnecting: A2DP - connecting A2Connected: A2DP - connected A2Detaching: A2DP - detaching A2SNnecting: A2DP (slave mode) - connecting A2SCnnected: A2DP (slave mode) - connected A2SDetaching: A2DP (slave mode) - detaching ACNNecting: audio - connecting ACONected: audio - connected AEXMode: audio - exiting AENMode: audio - entering For a detailed description of the available states and state transitions, see 'Signaling states'."""
		response = self._core.io.query_str(f'FETCh:BLUetooth:SIGNaling<Instance>:CONNection:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.ConnectionState)

	def clone(self) -> 'StateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
