from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ActionCls:
	"""Action commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("action", core, parent)

	def set_le_signaling(self, action: enums.ConnectionActionLe) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling<Instance>:CONNection:ACTion:LESignaling \n
		Snippet: driver.call.connection.action.set_le_signaling(action = enums.ConnectionActionLe.AMConnect) \n
		Requests the R&S CMW to perform certain signaling actions for LE. It has no query form: the current signaling state can
		be retrieved using the method RsCmwBluetoothSig.Connection.State.LeSignaling.fetch command. \n
			:param action: INQuire | SINQuiry | CONNect | SCONnecting | DETach | TMConnect | EMConnect | EMEXit | EMENter | AMConnect | AMEXit | AMENter INQuire: Switch on master signal and start inquiry for Bluetooth devices within range. Inquiry stops after a configurable maximum duration (see method RsCmwBluetoothSig.Configure.Connection.Inquiry.Duration.leSignaling) or after a configurable number of responses (see method RsCmwBluetoothSig.Configure.Connection.Inquiry.NoResponses.leSignaling) . SINQuiry: Stop inquiry, switch off master signal and return to standby state. CONNect: Switch on master signal, start paging the selected Bluetooth device and establish an ACL connection. SCONnecting: Stop an ongoing connection setup, switch off the master signal and return to standby state. DETach: Detach an established connection, switch off the master signal and return to standby state. TMConnect: Connect test mode - switch on master signal, start paging the selected Bluetooth device, establish a LE UTP test mode connection, and transmit test packets EMConnect: Connect echo mode via isochronous channels. EMEXit: Exit echo mode EMENter: Enter echo mode. AMConnect: Connect LE audio via isochronous channels using LC3 codec. AMEXit: Exit LE audio. AMENter: Enter LE audio.
		"""
		param = Conversions.enum_scalar_to_str(action, enums.ConnectionActionLe)
		self._core.io.write_with_opc(f'CALL:BLUetooth:SIGNaling<Instance>:CONNection:ACTion:LESignaling {param}')

	def set_value(self, action: enums.ConnectAction) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling<Instance>:CONNection:ACTion \n
		Snippet: driver.call.connection.action.set_value(action = enums.ConnectAction.ADConnect) \n
		Requests the R&S CMW to perform certain signaling actions for BR/EDR. It has no query form: the current signaling state
		can be retrieved using the method RsCmwBluetoothSig.Connection.State.fetch command. \n
			:param action: INQuire | SINQuiry | SCONnecting | STMode | CONNect | TMConnect | DETach | REController | EMConnect | EXEMode | ENEMode | HFPConnect | EXHFp | ENHFp | AGConnect | ENAGate | EXAGate | ADConnect | AUDConnect | ADEXit | ADENter INQuire: Switch on master signal and start inquiry for Bluetooth devices within range. Inquiry stops after a configurable maximum duration (see method RsCmwBluetoothSig.Configure.Connection.Inquiry.ilength) or after a configurable number of responses (see method RsCmwBluetoothSig.Configure.Connection.Inquiry.NoResponses.value) . SINQuiry: Stop inquiry, switch off master signal and return to standby state. SCONnecting: Stop an ongoing connection setup, switch off the master signal and return to standby state. STMode: Stop a test mode connection, switch off the master signal and return to standby state. CONNect: Switch on master signal, start paging the selected Bluetooth device and establish an ACL connection. TMConnect: Switch on master signal, start paging the selected Bluetooth device and establish a test mode connection. DETach: Detach an established connection, switch off the master signal and return to standby state. REController: Run EUT controller to reset and initialize the EUT via USB connection EMConnect: Connect echo mode. EXEMode: Exit echo mode ENEMode: Enter echo mode. HFPConnect: Connect hands-free profile. EXHFp: Exit hands-free profile ENHFp: Enter hands-free profile. AGConnect: Connect hands-free audio gateway profile. ENAGate: Enter hands-free audio gateway profile. EXAGate: Exit hands-free audio gateway profile ADConnect: Connect A2DP AUDConnect: Connect audio mode. ADEXit: Exit audio mode ADENter: Enter audio mode.
		"""
		param = Conversions.enum_scalar_to_str(action, enums.ConnectAction)
		self._core.io.write_with_opc(f'CALL:BLUetooth:SIGNaling<Instance>:CONNection:ACTion {param}')
