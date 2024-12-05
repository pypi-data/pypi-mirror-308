from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioCls:
	"""Audio commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("audio", core, parent)

	# noinspection PyTypeChecker
	class LinfoStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Speech_Code: enums.SpeechCode: CVSD | ALAW | ULAW | MSBC CVSD (8 kHz) , A-law (8 kHz) , u-law (8 kHz) , or mSBC (16 kHz) codec
			- Link_Type: enums.VoiceLinkType: SCO | ESCO Synchronous connection-oriented (SCO) or enhanced synchronous connection-oriented (eSCO) link
			- Packet_Type: enums.PacketTypeEsco: HV1 | HV2 | HV3 | EV3 | EV4 | EV5 | 2EV3 | 3EV3 | 2EV5 | 3EV5 HV1: SCO packets high-quality voice, 1/3 rate FEC HV2: SCO packets high-quality voice, 2/3 rate FEC HV3: SCO packets high-quality voice, no FEC EV3, EV4, EV5: eSCO packets on the top of BR ACL connection 2EV3, 3EV3, 2EV5, 3EV5: eSCO packets on the top of EDR ACL connection (2-EV3, 3-EV3, 2-EV5, 3-EV5 packets)
			- Sample_Rate: float: float Range: 0 kHz to 999 kHz
			- Data_Rate: int: decimal Range: 0 kbit/s to 9999 kbit/s"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Speech_Code', enums.SpeechCode),
			ArgStruct.scalar_enum('Link_Type', enums.VoiceLinkType),
			ArgStruct.scalar_enum('Packet_Type', enums.PacketTypeEsco),
			ArgStruct.scalar_float('Sample_Rate'),
			ArgStruct.scalar_int('Data_Rate')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Speech_Code: enums.SpeechCode = None
			self.Link_Type: enums.VoiceLinkType = None
			self.Packet_Type: enums.PacketTypeEsco = None
			self.Sample_Rate: float = None
			self.Data_Rate: int = None

	def get_linfo(self) -> LinfoStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:LINFo \n
		Snippet: value: LinfoStruct = driver.sense.connection.audio.get_linfo() \n
		Queries the parameters of active audio connection. \n
			:return: structure: for return value, see the help for LinfoStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:LINFo?', self.__class__.LinfoStruct())
