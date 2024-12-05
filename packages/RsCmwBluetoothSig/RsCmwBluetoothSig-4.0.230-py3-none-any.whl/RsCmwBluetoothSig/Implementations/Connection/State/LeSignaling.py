from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LeSignalingCls:
	"""LeSignaling commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("leSignaling", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.SignalingState:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:CONNection:STATe:LESignaling \n
		Snippet: value: enums.SignalingState = driver.connection.state.leSignaling.fetch() \n
		Returns the signaling state of the R&S CMW for LE. State changes are initiated using the method RsCmwBluetoothSig.Call.
		Connection.Action.leSignaling command. \n
			:return: state: OFF | SBY | INQuiring | CNNecting | CONNected | DETaching | TCONected | TCNNecting | CPOWer | ECNNecting | ECONnected | EEXiting | EENTering | ACNNecting | ACONnected | AEXiting | AENTering | PAIRing OFF: not connected SBY: standby INQuiring: inquiring CNNecting: connecting CONNected: connected DETaching: detaching TCNNecting: LE test mode - connecting TCONected: LE test mode - connected CPOWer: LE power control EENTering: echo mode - entering ECNNecting: echo mode - connecting ECONnected: echo mode - connected EEXiting: echo mode - exiting AENTering: audio - entering ACNNecting: audio - connecting ACONnected: audio - connected AEXiting: audio - exiting PAIRing: pairing"""
		response = self._core.io.query_str(f'FETCh:BLUetooth:SIGNaling<Instance>:CONNection:STATe:LESignaling?')
		return Conversions.str_to_scalar_enum(response, enums.SignalingState)
