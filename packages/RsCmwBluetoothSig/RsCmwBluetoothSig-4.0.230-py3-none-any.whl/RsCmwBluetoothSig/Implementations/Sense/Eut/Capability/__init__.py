from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CapabilityCls:
	"""Capability commands group definition. 11 total commands, 1 Subgroups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("capability", core, parent)

	@property
	def adp(self):
		"""adp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adp'):
			from .Adp import AdpCls
			self._adp = AdpCls(self._core, self._cmd_group)
		return self._adp

	# noinspection PyTypeChecker
	class EscoStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Ev_3_Packets: bool: OFF | ON EV3 packets
			- Ev_4_Packets: bool: OFF | ON EV4 packets
			- Ev_5_Packets: bool: OFF | ON EV5 packets
			- Three_Slot_Edr_Pck: bool: OFF | ON 2-EV5 / 3-EV5 packets over three slots
			- Edr_2_Mbps_Mode: bool: OFF | ON 2-EV3 / 2-EV5 packets
			- Edr_3_Mbps_Mode: bool: OFF | ON 3-EV3 / 3-EV5 packets"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Ev_3_Packets'),
			ArgStruct.scalar_bool('Ev_4_Packets'),
			ArgStruct.scalar_bool('Ev_5_Packets'),
			ArgStruct.scalar_bool('Three_Slot_Edr_Pck'),
			ArgStruct.scalar_bool('Edr_2_Mbps_Mode'),
			ArgStruct.scalar_bool('Edr_3_Mbps_Mode')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ev_3_Packets: bool = None
			self.Ev_4_Packets: bool = None
			self.Ev_5_Packets: bool = None
			self.Three_Slot_Edr_Pck: bool = None
			self.Edr_2_Mbps_Mode: bool = None
			self.Edr_3_Mbps_Mode: bool = None

	def get_esco(self) -> EscoStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:ESCO \n
		Snippet: value: EscoStruct = driver.sense.eut.capability.get_esco() \n
		Gets the e-SCO-related capabilities of the connected EUT. For each capability, either OFF or ON is returned \n
			:return: structure: for return value, see the help for EscoStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:ESCO?', self.__class__.EscoStruct())

	def get_sclass(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:SCLass \n
		Snippet: value: str = driver.sense.eut.capability.get_sclass() \n
		Gets the (major) service class of the connected EUT as specified in . \n
			:return: service_class: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:SCLass?')
		return trim_str_response(response)

	def get_encryption(self) -> bool:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:ENCRyption \n
		Snippet: value: bool = driver.sense.eut.capability.get_encryption() \n
		Queries whether the connected EUT supports encryption (OFF|ON) \n
			:return: encryption: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:ENCRyption?')
		return Conversions.str_to_bool(response)

	def get_power_control(self) -> bool:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:PCONtrol \n
		Snippet: value: bool = driver.sense.eut.capability.get_power_control() \n
		Queries whether the connected EUT supports legacy power control (OFF|ON) \n
			:return: power_control: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:PCONtrol?')
		return Conversions.str_to_bool(response)

	def get_ep_control(self) -> bool:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:EPControl \n
		Snippet: value: bool = driver.sense.eut.capability.get_ep_control() \n
		Queries whether the connected EUT supports enhanced power control (OFF|ON) \n
			:return: epower_control: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:EPControl?')
		return Conversions.str_to_bool(response)

	# noinspection PyTypeChecker
	class PsavingStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Hold: bool: OFF | ON Hold mode
			- Sniff: bool: OFF | ON Sniff mode
			- Park: bool: OFF | ON Park mode"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Hold'),
			ArgStruct.scalar_bool('Sniff'),
			ArgStruct.scalar_bool('Park')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hold: bool = None
			self.Sniff: bool = None
			self.Park: bool = None

	def get_psaving(self) -> PsavingStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:PSAVing \n
		Snippet: value: PsavingStruct = driver.sense.eut.capability.get_psaving() \n
		Gets the power saving-related capabilities of the connected EUT. For each capability, either OFF or ON is returned \n
			:return: structure: for return value, see the help for PsavingStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:PSAVing?', self.__class__.PsavingStruct())

	# noinspection PyTypeChecker
	class ConnectionStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Page_Scan_Mode: enums.PageScanMode: 0X00 | 0X01 | 0X02 | 0X03 The page scan mode that is used for default page scan: 0X00: mandatory page scan mode 0X01: optional page scan mode I 0X02: optional page scan mode II 0X03: optional page scan mode III
			- Pg_Scan_Prd_Mode: enums.PageScanPeriodMode: P0 | P1 | P2 Page scan period mode
			- Pg_Scan_Rep_Mode: enums.PsrMode: R0 | R1 | R2 Page scan repetition mode
			- Pscheme: bool: OFF | ON 'Optional paging scheme' support
			- Slot_Offset: bool: OFF | ON 'Slot offset' support
			- Timing_Acc: bool: OFF | ON 'Timing accuracy' support
			- Switch: bool: OFF | ON 'Switching between master and slave' support
			- Rssi: bool: OFF | ON 'Received signal strength indication' support"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Page_Scan_Mode', enums.PageScanMode),
			ArgStruct.scalar_enum('Pg_Scan_Prd_Mode', enums.PageScanPeriodMode),
			ArgStruct.scalar_enum('Pg_Scan_Rep_Mode', enums.PsrMode),
			ArgStruct.scalar_bool('Pscheme'),
			ArgStruct.scalar_bool('Slot_Offset'),
			ArgStruct.scalar_bool('Timing_Acc'),
			ArgStruct.scalar_bool('Switch'),
			ArgStruct.scalar_bool('Rssi')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Page_Scan_Mode: enums.PageScanMode = None
			self.Pg_Scan_Prd_Mode: enums.PageScanPeriodMode = None
			self.Pg_Scan_Rep_Mode: enums.PsrMode = None
			self.Pscheme: bool = None
			self.Slot_Offset: bool = None
			self.Timing_Acc: bool = None
			self.Switch: bool = None
			self.Rssi: bool = None

	def get_connection(self) -> ConnectionStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:CONNection \n
		Snippet: value: ConnectionStruct = driver.sense.eut.capability.get_connection() \n
		Gets the connection-related properties and capabilities of the connected EUT. \n
			:return: structure: for return value, see the help for ConnectionStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:CONNection?', self.__class__.ConnectionStruct())

	# noinspection PyTypeChecker
	class ScoStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Cqdd: bool: OFF | ON Channel quality driven data rate
			- Link: bool: OFF | ON SCO link
			- Ts_Data: bool: OFF | ON Transparent SCO data
			- Hv_2_P: bool: OFF | ON HV2 packets
			- Hv_3_P: bool: OFF | ON HV3 packets
			- Ulaw: bool: OFF | ON u-law log
			- Alaw: bool: OFF | ON A-law log
			- Cvsd: bool: OFF | ON Continuous variable slope delta modulation"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Cqdd'),
			ArgStruct.scalar_bool('Link'),
			ArgStruct.scalar_bool('Ts_Data'),
			ArgStruct.scalar_bool('Hv_2_P'),
			ArgStruct.scalar_bool('Hv_3_P'),
			ArgStruct.scalar_bool('Ulaw'),
			ArgStruct.scalar_bool('Alaw'),
			ArgStruct.scalar_bool('Cvsd')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cqdd: bool = None
			self.Link: bool = None
			self.Ts_Data: bool = None
			self.Hv_2_P: bool = None
			self.Hv_3_P: bool = None
			self.Ulaw: bool = None
			self.Alaw: bool = None
			self.Cvsd: bool = None

	def get_sco(self) -> ScoStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:SCO \n
		Snippet: value: ScoStruct = driver.sense.eut.capability.get_sco() \n
		Gets the SCO-related capabilities of the connected EUT. For each capability, either OFF or ON is returned \n
			:return: structure: for return value, see the help for ScoStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:SCO?', self.__class__.ScoStruct())

	# noinspection PyTypeChecker
	class AclStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Fc_Lag: int: decimal Flow control lag Range: 0 to 7 , Unit: 256 bytes
			- Dh_3_Dm_3: bool: OFF | ON Three-slot packets
			- Dh_5_Dm_5: bool: OFF | ON Five-slot packets
			- Edr_3_Slot: bool: OFF | ON Three-slot EDR ACL packets
			- Edr_5_Slot: bool: OFF | ON Five-slot EDR ACL packets
			- Edr_2_Mbps: bool: OFF | ON EDR ACL 2 Mbit/s
			- Edr_3_Mbps: bool: OFF | ON EDR ACL 3 Mbit/s"""
		__meta_args_list = [
			ArgStruct.scalar_int('Fc_Lag'),
			ArgStruct.scalar_bool('Dh_3_Dm_3'),
			ArgStruct.scalar_bool('Dh_5_Dm_5'),
			ArgStruct.scalar_bool('Edr_3_Slot'),
			ArgStruct.scalar_bool('Edr_5_Slot'),
			ArgStruct.scalar_bool('Edr_2_Mbps'),
			ArgStruct.scalar_bool('Edr_3_Mbps')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Fc_Lag: int = None
			self.Dh_3_Dm_3: bool = None
			self.Dh_5_Dm_5: bool = None
			self.Edr_3_Slot: bool = None
			self.Edr_5_Slot: bool = None
			self.Edr_2_Mbps: bool = None
			self.Edr_3_Mbps: bool = None

	def get_acl(self) -> AclStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:ACL \n
		Snippet: value: AclStruct = driver.sense.eut.capability.get_acl() \n
		Gets the ACL-related capabilities of the connected EUT. Except for the flow control lag, for each capability either OFF
		or ON is returned. \n
			:return: structure: for return value, see the help for AclStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:ACL?', self.__class__.AclStruct())

	# noinspection PyTypeChecker
	class LeSignalingStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Device_Name: str: string LE device name
			- Le_Encryption: bool: OFF | ON Support of LE encryption
			- Conn_Param_Req: bool: OFF | ON Support of connection parameter request procedure
			- Ext_Rejection_Ind: bool: OFF | ON Support of extended rejection indication
			- Slave_Init_Feat_Ex: bool: OFF | ON Support of slave-initiated features exchange
			- Le_Ping: bool: OFF | ON Support of LE ping
			- Le_Data_Pk_Lex: bool: No parameter help available
			- Ll_Privacy: bool: OFF | ON Support of LL privacy
			- Ex_Scan_Filt_Pol: bool: OFF | ON Support of extended scanner filter policies
			- Le_2_Mphy: bool: OFF | ON Support of LE 2 Mbps PHY
			- Stab_Mod_Trans: bool: OFF | ON Support of stable modulation index for transmitter
			- Stab_Mod_Rec: bool: OFF | ON Support of stable modulation index for receiver
			- Le_Coded_Phy: bool: No parameter help available
			- Le_Ext_Adv: bool: OFF | ON Support of extended advertising
			- Le_Periodic_Adv: bool: No parameter help available
			- Chan_Sel_Alg_2: bool: OFF | ON Support of channel selection algorithm No. 2
			- Le_Power_Class_1: bool: No parameter help available
			- Min_Number_Used_Ch: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Device_Name'),
			ArgStruct.scalar_bool('Le_Encryption'),
			ArgStruct.scalar_bool('Conn_Param_Req'),
			ArgStruct.scalar_bool('Ext_Rejection_Ind'),
			ArgStruct.scalar_bool('Slave_Init_Feat_Ex'),
			ArgStruct.scalar_bool('Le_Ping'),
			ArgStruct.scalar_bool('Le_Data_Pk_Lex'),
			ArgStruct.scalar_bool('Ll_Privacy'),
			ArgStruct.scalar_bool('Ex_Scan_Filt_Pol'),
			ArgStruct.scalar_bool('Le_2_Mphy'),
			ArgStruct.scalar_bool('Stab_Mod_Trans'),
			ArgStruct.scalar_bool('Stab_Mod_Rec'),
			ArgStruct.scalar_bool('Le_Coded_Phy'),
			ArgStruct.scalar_bool('Le_Ext_Adv'),
			ArgStruct.scalar_bool('Le_Periodic_Adv'),
			ArgStruct.scalar_bool('Chan_Sel_Alg_2'),
			ArgStruct.scalar_bool('Le_Power_Class_1'),
			ArgStruct.scalar_bool('Min_Number_Used_Ch')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Device_Name: str = None
			self.Le_Encryption: bool = None
			self.Conn_Param_Req: bool = None
			self.Ext_Rejection_Ind: bool = None
			self.Slave_Init_Feat_Ex: bool = None
			self.Le_Ping: bool = None
			self.Le_Data_Pk_Lex: bool = None
			self.Ll_Privacy: bool = None
			self.Ex_Scan_Filt_Pol: bool = None
			self.Le_2_Mphy: bool = None
			self.Stab_Mod_Trans: bool = None
			self.Stab_Mod_Rec: bool = None
			self.Le_Coded_Phy: bool = None
			self.Le_Ext_Adv: bool = None
			self.Le_Periodic_Adv: bool = None
			self.Chan_Sel_Alg_2: bool = None
			self.Le_Power_Class_1: bool = None
			self.Min_Number_Used_Ch: bool = None

	def get_le_signaling(self) -> LeSignalingStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:LESignaling \n
		Snippet: value: LeSignalingStruct = driver.sense.eut.capability.get_le_signaling() \n
		Queries capabilities retrieved from the EUT. \n
			:return: structure: for return value, see the help for LeSignalingStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:LESignaling?', self.__class__.LeSignalingStruct())

	def clone(self) -> 'CapabilityCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CapabilityCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
