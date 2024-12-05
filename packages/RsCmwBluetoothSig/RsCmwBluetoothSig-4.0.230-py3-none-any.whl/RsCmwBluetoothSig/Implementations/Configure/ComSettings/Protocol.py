from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ProtocolCls:
	"""Protocol commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("protocol", core, parent)

	def set(self, protocol: enums.Protocol, commSettings=repcap.CommSettings.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:PROTocol \n
		Snippet: driver.configure.comSettings.protocol.set(protocol = enums.Protocol.CTSRts, commSettings = repcap.CommSettings.Default) \n
		Specifies the transmission parameters of serial connection. \n
			:param protocol: XONXoff | CTSRts | NONE Transmit flow control X-ON/X-OFF, RFR/CTS, or none
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
		"""
		param = Conversions.enum_scalar_to_str(protocol, enums.Protocol)
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:PROTocol {param}')

	# noinspection PyTypeChecker
	def get(self, commSettings=repcap.CommSettings.Default) -> enums.Protocol:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:PROTocol \n
		Snippet: value: enums.Protocol = driver.configure.comSettings.protocol.get(commSettings = repcap.CommSettings.Default) \n
		Specifies the transmission parameters of serial connection. \n
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
			:return: protocol: XONXoff | CTSRts | NONE Transmit flow control X-ON/X-OFF, RFR/CTS, or none"""
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:PROTocol?')
		return Conversions.str_to_scalar_enum(response, enums.Protocol)
