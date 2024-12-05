from enum import Enum


# noinspection SpellCheckingInspection
class AddressType(Enum):
	"""2 Members, PUBLic ... RANDom"""
	PUBLic = 0
	RANDom = 1


# noinspection SpellCheckingInspection
class AddressTypeExt(Enum):
	"""4 Members, PIDentity ... RSIDentity"""
	PIDentity = 0
	PUBLic = 1
	RANDom = 2
	RSIDentity = 3


# noinspection SpellCheckingInspection
class AfHopingMode(Enum):
	"""3 Members, EUT ... USER"""
	EUT = 0
	NORM = 1
	USER = 2


# noinspection SpellCheckingInspection
class AllocMethod(Enum):
	"""2 Members, LOUDness ... SNR"""
	LOUDness = 0
	SNR = 1


# noinspection SpellCheckingInspection
class AudioChannelMode(Enum):
	"""4 Members, DUAL ... STEReo"""
	DUAL = 0
	JSTereo = 1
	MONO = 2
	STEReo = 3


# noinspection SpellCheckingInspection
class AudioChannelModeLe(Enum):
	"""2 Members, MONO ... STEReo"""
	MONO = 0
	STEReo = 1


# noinspection SpellCheckingInspection
class AudioCodec(Enum):
	"""1 Members, SBC ... SBC"""
	SBC = 0


# noinspection SpellCheckingInspection
class BaudRate(Enum):
	"""24 Members, B110 ... B96K"""
	B110 = 0
	B115k = 1
	B12K = 2
	B14K = 3
	B19K = 4
	B1M = 5
	B1M5 = 6
	B234k = 7
	B24K = 8
	B28K = 9
	B2M = 10
	B300 = 11
	B38K = 12
	B3M = 13
	B3M5 = 14
	B460k = 15
	B48K = 16
	B4M = 17
	B500k = 18
	B576k = 19
	B57K = 20
	B600 = 21
	B921k = 22
	B96K = 23


# noinspection SpellCheckingInspection
class BbBoard(Enum):
	"""140 Members, BBR1 ... SUW44"""
	BBR1 = 0
	BBR11 = 1
	BBR12 = 2
	BBR13 = 3
	BBR14 = 4
	BBR2 = 5
	BBR21 = 6
	BBR22 = 7
	BBR23 = 8
	BBR24 = 9
	BBR3 = 10
	BBR31 = 11
	BBR32 = 12
	BBR33 = 13
	BBR34 = 14
	BBR4 = 15
	BBR41 = 16
	BBR42 = 17
	BBR43 = 18
	BBR44 = 19
	BBT1 = 20
	BBT11 = 21
	BBT12 = 22
	BBT13 = 23
	BBT14 = 24
	BBT2 = 25
	BBT21 = 26
	BBT22 = 27
	BBT23 = 28
	BBT24 = 29
	BBT3 = 30
	BBT31 = 31
	BBT32 = 32
	BBT33 = 33
	BBT34 = 34
	BBT4 = 35
	BBT41 = 36
	BBT42 = 37
	BBT43 = 38
	BBT44 = 39
	SUA012 = 40
	SUA034 = 41
	SUA056 = 42
	SUA078 = 43
	SUA1 = 44
	SUA11 = 45
	SUA112 = 46
	SUA12 = 47
	SUA13 = 48
	SUA134 = 49
	SUA14 = 50
	SUA15 = 51
	SUA156 = 52
	SUA16 = 53
	SUA17 = 54
	SUA178 = 55
	SUA18 = 56
	SUA2 = 57
	SUA21 = 58
	SUA212 = 59
	SUA22 = 60
	SUA23 = 61
	SUA234 = 62
	SUA24 = 63
	SUA25 = 64
	SUA256 = 65
	SUA26 = 66
	SUA27 = 67
	SUA278 = 68
	SUA28 = 69
	SUA3 = 70
	SUA31 = 71
	SUA312 = 72
	SUA32 = 73
	SUA33 = 74
	SUA334 = 75
	SUA34 = 76
	SUA35 = 77
	SUA356 = 78
	SUA36 = 79
	SUA37 = 80
	SUA378 = 81
	SUA38 = 82
	SUA4 = 83
	SUA41 = 84
	SUA412 = 85
	SUA42 = 86
	SUA43 = 87
	SUA434 = 88
	SUA44 = 89
	SUA45 = 90
	SUA456 = 91
	SUA46 = 92
	SUA47 = 93
	SUA478 = 94
	SUA48 = 95
	SUA5 = 96
	SUA6 = 97
	SUA7 = 98
	SUA8 = 99
	SUU1 = 100
	SUU11 = 101
	SUU12 = 102
	SUU13 = 103
	SUU14 = 104
	SUU2 = 105
	SUU21 = 106
	SUU22 = 107
	SUU23 = 108
	SUU24 = 109
	SUU3 = 110
	SUU31 = 111
	SUU32 = 112
	SUU33 = 113
	SUU34 = 114
	SUU4 = 115
	SUU41 = 116
	SUU42 = 117
	SUU43 = 118
	SUU44 = 119
	SUW1 = 120
	SUW11 = 121
	SUW12 = 122
	SUW13 = 123
	SUW14 = 124
	SUW2 = 125
	SUW21 = 126
	SUW22 = 127
	SUW23 = 128
	SUW24 = 129
	SUW3 = 130
	SUW31 = 131
	SUW32 = 132
	SUW33 = 133
	SUW34 = 134
	SUW4 = 135
	SUW41 = 136
	SUW42 = 137
	SUW43 = 138
	SUW44 = 139


# noinspection SpellCheckingInspection
class BlockLength(Enum):
	"""4 Members, BL12 ... BL8"""
	BL12 = 0
	BL16 = 1
	BL4 = 2
	BL8 = 3


# noinspection SpellCheckingInspection
class BrPacketType(Enum):
	"""3 Members, DH1 ... DH5"""
	DH1 = 0
	DH3 = 1
	DH5 = 2


# noinspection SpellCheckingInspection
class BurstType(Enum):
	"""3 Members, BR ... LE"""
	BR = 0
	EDR = 1
	LE = 2


# noinspection SpellCheckingInspection
class ByteCountB16k(Enum):
	"""1 Members, B40 ... B40"""
	B40 = 0


# noinspection SpellCheckingInspection
class ByteCountB32K(Enum):
	"""1 Members, B80 ... B80"""
	B80 = 0


# noinspection SpellCheckingInspection
class ByteCountB48K(Enum):
	"""3 Members, B100 ... B155"""
	B100 = 0
	B120 = 1
	B155 = 2


# noinspection SpellCheckingInspection
class CodingScheme(Enum):
	"""2 Members, S2 ... S8"""
	S2 = 0
	S8 = 1


# noinspection SpellCheckingInspection
class CommProtocol(Enum):
	"""2 Members, HCI ... TWO"""
	HCI = 0
	TWO = 1


# noinspection SpellCheckingInspection
class ConnectAction(Enum):
	"""21 Members, ADConnect ... TMConnect"""
	ADConnect = 0
	ADENter = 1
	ADEXit = 2
	AGConnect = 3
	AUDConnect = 4
	CONNect = 5
	DETach = 6
	EMConnect = 7
	ENAGate = 8
	ENEMode = 9
	ENHFp = 10
	EXAGate = 11
	EXEMode = 12
	EXHFp = 13
	HFPConnect = 14
	INQuire = 15
	REController = 16
	SCONnecting = 17
	SINQuiry = 18
	STMode = 19
	TMConnect = 20


# noinspection SpellCheckingInspection
class ConnectionActionLe(Enum):
	"""12 Members, AMConnect ... TMConnect"""
	AMConnect = 0
	AMENter = 1
	AMEXit = 2
	CONNect = 3
	DETach = 4
	EMConnect = 5
	EMENter = 6
	EMEXit = 7
	INQuire = 8
	SCONnecting = 9
	SINQuiry = 10
	TMConnect = 11


# noinspection SpellCheckingInspection
class ConnectionState(Enum):
	"""47 Members, A2CNnecting ... XHASmode"""
	A2CNnecting = 0
	A2Connected = 1
	A2Detaching = 2
	A2SCnnected = 3
	A2SDetaching = 4
	A2SNnecting = 5
	ACNNecting = 6
	ACONected = 7
	AENMode = 8
	AEXMode = 9
	AGCNnecting = 10
	AGConnected = 11
	CHASmode = 12
	CNASmode = 13
	CNNecting = 14
	CONNected = 15
	DETaching = 16
	DHASmode = 17
	ECNNecting = 18
	ECONected = 19
	ECRunning = 20
	EHASmode = 21
	ENAGmode = 22
	ENEMode = 23
	ENHFp = 24
	ENHSmode = 25
	EXAGmode = 26
	EXEMode = 27
	EXHFp = 28
	EXHSmode = 29
	HFCNnecting = 30
	HFConnected = 31
	HSCNnecting = 32
	HSConnected = 33
	HSDetaching = 34
	INQuiring = 35
	OFF = 36
	SBY = 37
	SCONnecting = 38
	SINQuiry = 39
	SMCNnecting = 40
	SMConnected = 41
	SMDetaching = 42
	SMIDle = 43
	TCNNecting = 44
	TCONected = 45
	XHASmode = 46


# noinspection SpellCheckingInspection
class ConTestResult(Enum):
	"""4 Members, FAIL ... TOUT"""
	FAIL = 0
	NRUN = 1
	PASS = 2
	TOUT = 3


# noinspection SpellCheckingInspection
class CteType(Enum):
	"""4 Members, AOA1us ... AOD2us"""
	AOA1us = 0
	AOA2us = 1
	AOD1us = 2
	AOD2us = 3


# noinspection SpellCheckingInspection
class DataBits(Enum):
	"""2 Members, D7 ... D8"""
	D7 = 0
	D8 = 1


# noinspection SpellCheckingInspection
class DriftRate(Enum):
	"""2 Members, HDRF ... LDRF"""
	HDRF = 0
	LDRF = 1


# noinspection SpellCheckingInspection
class DtxMode(Enum):
	"""2 Members, SINGle ... SPEC"""
	SINGle = 0
	SPEC = 1


# noinspection SpellCheckingInspection
class EdrPacketType(Enum):
	"""6 Members, E21P ... E35P"""
	E21P = 0
	E23P = 1
	E25P = 2
	E31P = 3
	E33P = 4
	E35P = 5


# noinspection SpellCheckingInspection
class EutState(Enum):
	"""2 Members, FAIL ... OK"""
	FAIL = 0
	OK = 1


# noinspection SpellCheckingInspection
class HwInterface(Enum):
	"""3 Members, NONE ... USB"""
	NONE = 0
	RS232 = 1
	USB = 2


# noinspection SpellCheckingInspection
class IqStopCondition(Enum):
	"""2 Members, NONE ... VALM"""
	NONE = 0
	VALM = 1


# noinspection SpellCheckingInspection
class LeDiagState(Enum):
	"""4 Members, LOADingvec ... VECTorloaded"""
	LOADingvec = 0
	OFF = 1
	ON = 2
	VECTorloaded = 3


# noinspection SpellCheckingInspection
class LeHoppingMode(Enum):
	"""2 Members, ALL ... CH2"""
	ALL = 0
	CH2 = 1


# noinspection SpellCheckingInspection
class LePacketType2(Enum):
	"""2 Members, RFCTe ... RFPHytest"""
	RFCTe = 0
	RFPHytest = 1


# noinspection SpellCheckingInspection
class LePhysicalType(Enum):
	"""3 Members, LE1M ... LELR"""
	LE1M = 0
	LE2M = 1
	LELR = 2


# noinspection SpellCheckingInspection
class LeRangePaternType(Enum):
	"""6 Members, ALL0 ... PRBS9"""
	ALL0 = 0
	ALL1 = 1
	ALT = 2
	P11 = 3
	P44 = 4
	PRBS9 = 5


# noinspection SpellCheckingInspection
class LeSigCodec(Enum):
	"""1 Members, LC3 ... LC3"""
	LC3 = 0


# noinspection SpellCheckingInspection
class LeSigDirection(Enum):
	"""3 Members, DOWNlink ... UPLink"""
	DOWNlink = 0
	DUPLex = 1
	UPLink = 2


# noinspection SpellCheckingInspection
class LeSigFrameDuration(Enum):
	"""2 Members, MS10 ... MS75"""
	MS10 = 0
	MS75 = 1


# noinspection SpellCheckingInspection
class LeSignalingState(Enum):
	"""12 Members, CMR ... TXRunning"""
	CMR = 0
	IDLE = 1
	OFF = 2
	RCOM = 3
	RXRunning = 4
	SPCM = 5
	SPRX = 6
	SPTX = 7
	STCM = 8
	STRX = 9
	STTX = 10
	TXRunning = 11


# noinspection SpellCheckingInspection
class LogCategory(Enum):
	"""4 Members, CONTinue ... WARNing"""
	CONTinue = 0
	ERRor = 1
	INFO = 2
	WARNing = 3


# noinspection SpellCheckingInspection
class ModIndexType(Enum):
	"""2 Members, STAB ... STAN"""
	STAB = 0
	STAN = 1


# noinspection SpellCheckingInspection
class OperatingMode(Enum):
	"""6 Members, AUDio ... UTPMode"""
	AUDio = 0
	CNTest = 1
	ECMode = 2
	PROFiles = 3
	RFTest = 4
	UTPMode = 5


# noinspection SpellCheckingInspection
class PacketTypeEsco(Enum):
	"""10 Members, _2EV3 ... HV3"""
	_2EV3 = 0
	_2EV5 = 1
	_3EV3 = 2
	_3EV5 = 3
	EV3 = 4
	EV4 = 5
	EV5 = 6
	HV1 = 7
	HV2 = 8
	HV3 = 9


# noinspection SpellCheckingInspection
class PacketTypeSco(Enum):
	"""3 Members, HV1 ... HV3"""
	HV1 = 0
	HV2 = 1
	HV3 = 2


# noinspection SpellCheckingInspection
class PageScanMode(Enum):
	"""4 Members, _0X00 ... _0X03"""
	_0X00 = 0
	_0X01 = 1
	_0X02 = 2
	_0X03 = 3


# noinspection SpellCheckingInspection
class PageScanPeriodMode(Enum):
	"""3 Members, P0 ... P2"""
	P0 = 0
	P1 = 1
	P2 = 2


# noinspection SpellCheckingInspection
class Parity(Enum):
	"""3 Members, EVEN ... ODD"""
	EVEN = 0
	NONE = 1
	ODD = 2


# noinspection SpellCheckingInspection
class PowerChange(Enum):
	"""4 Members, DOWN ... UP"""
	DOWN = 0
	MAX = 1
	NNE = 2
	UP = 3


# noinspection SpellCheckingInspection
class PowerControl(Enum):
	"""3 Members, DOWN ... UP"""
	DOWN = 0
	MAX = 1
	UP = 2


# noinspection SpellCheckingInspection
class PowerControlMode(Enum):
	"""2 Members, AUTO ... OFF"""
	AUTO = 0
	OFF = 1


# noinspection SpellCheckingInspection
class PowerFlag(Enum):
	"""3 Members, MAX ... NONE"""
	MAX = 0
	MIN = 1
	NONE = 2


# noinspection SpellCheckingInspection
class PowerMinMax(Enum):
	"""5 Members, CHANged ... NOTS"""
	CHANged = 0
	MAX = 1
	MIN = 2
	NNM = 3
	NOTS = 4


# noinspection SpellCheckingInspection
class PriorityRole(Enum):
	"""2 Members, MASTer ... SLAVe"""
	MASTer = 0
	SLAVe = 1


# noinspection SpellCheckingInspection
class ProfileRole(Enum):
	"""3 Members, ADGate ... HNDFree"""
	ADGate = 0
	ASINk = 1
	HNDFree = 2


# noinspection SpellCheckingInspection
class Protocol(Enum):
	"""3 Members, CTSRts ... XONXoff"""
	CTSRts = 0
	NONE = 1
	XONXoff = 2


# noinspection SpellCheckingInspection
class PsrMode(Enum):
	"""3 Members, R0 ... R2"""
	R0 = 0
	R1 = 1
	R2 = 2


# noinspection SpellCheckingInspection
class Repeat(Enum):
	"""2 Members, CONTinuous ... SINGleshot"""
	CONTinuous = 0
	SINGleshot = 1


# noinspection SpellCheckingInspection
class ResourceState(Enum):
	"""8 Members, ACTive ... RUN"""
	ACTive = 0
	ADJusted = 1
	INValid = 2
	OFF = 3
	PENDing = 4
	QUEued = 5
	RDY = 6
	RUN = 7


# noinspection SpellCheckingInspection
class ResultStatus2(Enum):
	"""10 Members, DC ... ULEU"""
	DC = 0
	INV = 1
	NAV = 2
	NCAP = 3
	OFF = 4
	OFL = 5
	OK = 6
	UFL = 7
	ULEL = 8
	ULEU = 9


# noinspection SpellCheckingInspection
class RxConnector(Enum):
	"""163 Members, I11I ... RH8"""
	I11I = 0
	I13I = 1
	I15I = 2
	I17I = 3
	I21I = 4
	I23I = 5
	I25I = 6
	I27I = 7
	I31I = 8
	I33I = 9
	I35I = 10
	I37I = 11
	I41I = 12
	I43I = 13
	I45I = 14
	I47I = 15
	IFI1 = 16
	IFI2 = 17
	IFI3 = 18
	IFI4 = 19
	IFI5 = 20
	IFI6 = 21
	IQ1I = 22
	IQ3I = 23
	IQ5I = 24
	IQ7I = 25
	R10D = 26
	R11 = 27
	R11C = 28
	R11D = 29
	R12 = 30
	R12C = 31
	R12D = 32
	R12I = 33
	R13 = 34
	R13C = 35
	R14 = 36
	R14C = 37
	R14I = 38
	R15 = 39
	R16 = 40
	R17 = 41
	R18 = 42
	R21 = 43
	R21C = 44
	R22 = 45
	R22C = 46
	R22I = 47
	R23 = 48
	R23C = 49
	R24 = 50
	R24C = 51
	R24I = 52
	R25 = 53
	R26 = 54
	R27 = 55
	R28 = 56
	R31 = 57
	R31C = 58
	R32 = 59
	R32C = 60
	R32I = 61
	R33 = 62
	R33C = 63
	R34 = 64
	R34C = 65
	R34I = 66
	R35 = 67
	R36 = 68
	R37 = 69
	R38 = 70
	R41 = 71
	R41C = 72
	R42 = 73
	R42C = 74
	R42I = 75
	R43 = 76
	R43C = 77
	R44 = 78
	R44C = 79
	R44I = 80
	R45 = 81
	R46 = 82
	R47 = 83
	R48 = 84
	RA1 = 85
	RA2 = 86
	RA3 = 87
	RA4 = 88
	RA5 = 89
	RA6 = 90
	RA7 = 91
	RA8 = 92
	RB1 = 93
	RB2 = 94
	RB3 = 95
	RB4 = 96
	RB5 = 97
	RB6 = 98
	RB7 = 99
	RB8 = 100
	RC1 = 101
	RC2 = 102
	RC3 = 103
	RC4 = 104
	RC5 = 105
	RC6 = 106
	RC7 = 107
	RC8 = 108
	RD1 = 109
	RD2 = 110
	RD3 = 111
	RD4 = 112
	RD5 = 113
	RD6 = 114
	RD7 = 115
	RD8 = 116
	RE1 = 117
	RE2 = 118
	RE3 = 119
	RE4 = 120
	RE5 = 121
	RE6 = 122
	RE7 = 123
	RE8 = 124
	RF1 = 125
	RF1C = 126
	RF2 = 127
	RF2C = 128
	RF2I = 129
	RF3 = 130
	RF3C = 131
	RF4 = 132
	RF4C = 133
	RF4I = 134
	RF5 = 135
	RF5C = 136
	RF6 = 137
	RF6C = 138
	RF7 = 139
	RF7C = 140
	RF8 = 141
	RF8C = 142
	RF9C = 143
	RFAC = 144
	RFBC = 145
	RFBI = 146
	RG1 = 147
	RG2 = 148
	RG3 = 149
	RG4 = 150
	RG5 = 151
	RG6 = 152
	RG7 = 153
	RG8 = 154
	RH1 = 155
	RH2 = 156
	RH3 = 157
	RH4 = 158
	RH5 = 159
	RH6 = 160
	RH7 = 161
	RH8 = 162


# noinspection SpellCheckingInspection
class RxConverter(Enum):
	"""40 Members, IRX1 ... RX44"""
	IRX1 = 0
	IRX11 = 1
	IRX12 = 2
	IRX13 = 3
	IRX14 = 4
	IRX2 = 5
	IRX21 = 6
	IRX22 = 7
	IRX23 = 8
	IRX24 = 9
	IRX3 = 10
	IRX31 = 11
	IRX32 = 12
	IRX33 = 13
	IRX34 = 14
	IRX4 = 15
	IRX41 = 16
	IRX42 = 17
	IRX43 = 18
	IRX44 = 19
	RX1 = 20
	RX11 = 21
	RX12 = 22
	RX13 = 23
	RX14 = 24
	RX2 = 25
	RX21 = 26
	RX22 = 27
	RX23 = 28
	RX24 = 29
	RX3 = 30
	RX31 = 31
	RX32 = 32
	RX33 = 33
	RX34 = 34
	RX4 = 35
	RX41 = 36
	RX42 = 37
	RX43 = 38
	RX44 = 39


# noinspection SpellCheckingInspection
class SamplingFrequency(Enum):
	"""4 Members, SF16 ... SF48"""
	SF16 = 0
	SF32 = 1
	SF441 = 2
	SF48 = 3


# noinspection SpellCheckingInspection
class SamplingFrequencyLe(Enum):
	"""6 Members, S16F ... SF441"""
	S16F = 0
	S24F = 1
	S32F = 2
	S48F = 3
	S8F = 4
	SF441 = 5


# noinspection SpellCheckingInspection
class SecurityMode(Enum):
	"""2 Members, SEC2 ... SEC3"""
	SEC2 = 0
	SEC3 = 1


# noinspection SpellCheckingInspection
class SequenceNumbering(Enum):
	"""2 Members, NORM ... TEST"""
	NORM = 0
	TEST = 1


# noinspection SpellCheckingInspection
class SignalingCmwRole(Enum):
	"""2 Members, CENTral ... PERipheral"""
	CENTral = 0
	PERipheral = 1


# noinspection SpellCheckingInspection
class SignalingStandard(Enum):
	"""2 Members, CLASsic ... LESignaling"""
	CLASsic = 0
	LESignaling = 1


# noinspection SpellCheckingInspection
class SignalingState(Enum):
	"""18 Members, ACNNecting ... TCONected"""
	ACNNecting = 0
	ACONnected = 1
	AENTering = 2
	AEXiting = 3
	CNNecting = 4
	CONNected = 5
	CPOWer = 6
	DETaching = 7
	ECNNecting = 8
	ECONnected = 9
	EENTering = 10
	EEXiting = 11
	INQuiring = 12
	OFF = 13
	PAIRing = 14
	SBY = 15
	TCNNecting = 16
	TCONected = 17


# noinspection SpellCheckingInspection
class SpeechCode(Enum):
	"""4 Members, ALAW ... ULAW"""
	ALAW = 0
	CVSD = 1
	MSBC = 2
	ULAW = 3


# noinspection SpellCheckingInspection
class StopBits(Enum):
	"""2 Members, S1 ... S2"""
	S1 = 0
	S2 = 1


# noinspection SpellCheckingInspection
class SubBands(Enum):
	"""2 Members, SB4 ... SB8"""
	SB4 = 0
	SB8 = 1


# noinspection SpellCheckingInspection
class SymbolTimeError(Enum):
	"""3 Members, NEG20 ... POS20"""
	NEG20 = 0
	OFF = 1
	POS20 = 2


# noinspection SpellCheckingInspection
class SymbolTimeErrorLe(Enum):
	"""3 Members, NEG50 ... POS50"""
	NEG50 = 0
	OFF = 1
	POS50 = 2


# noinspection SpellCheckingInspection
class TestMode(Enum):
	"""2 Members, LOOPback ... TXTest"""
	LOOPback = 0
	TXTest = 1


# noinspection SpellCheckingInspection
class TestVector(Enum):
	"""47 Members, INITstack ... TV9"""
	INITstack = 0
	RELoadstack = 1
	TV0 = 2
	TV1 = 3
	TV10 = 4
	TV11 = 5
	TV12 = 6
	TV13 = 7
	TV14 = 8
	TV15 = 9
	TV16 = 10
	TV17 = 11
	TV18 = 12
	TV19 = 13
	TV2 = 14
	TV20 = 15
	TV21 = 16
	TV22 = 17
	TV23 = 18
	TV24 = 19
	TV25 = 20
	TV26 = 21
	TV27 = 22
	TV28 = 23
	TV29 = 24
	TV3 = 25
	TV30 = 26
	TV31 = 27
	TV32 = 28
	TV33 = 29
	TV34 = 30
	TV35 = 31
	TV36 = 32
	TV37 = 33
	TV38 = 34
	TV39 = 35
	TV4 = 36
	TV40 = 37
	TV41 = 38
	TV42 = 39
	TV43 = 40
	TV44 = 41
	TV5 = 42
	TV6 = 43
	TV7 = 44
	TV8 = 45
	TV9 = 46


# noinspection SpellCheckingInspection
class TxConnector(Enum):
	"""86 Members, I12O ... RH18"""
	I12O = 0
	I14O = 1
	I16O = 2
	I18O = 3
	I22O = 4
	I24O = 5
	I26O = 6
	I28O = 7
	I32O = 8
	I34O = 9
	I36O = 10
	I38O = 11
	I42O = 12
	I44O = 13
	I46O = 14
	I48O = 15
	IFO1 = 16
	IFO2 = 17
	IFO3 = 18
	IFO4 = 19
	IFO5 = 20
	IFO6 = 21
	IQ2O = 22
	IQ4O = 23
	IQ6O = 24
	IQ8O = 25
	R10D = 26
	R118 = 27
	R1183 = 28
	R1184 = 29
	R11C = 30
	R11D = 31
	R11O = 32
	R11O3 = 33
	R11O4 = 34
	R12C = 35
	R12D = 36
	R13C = 37
	R13O = 38
	R14C = 39
	R214 = 40
	R218 = 41
	R21C = 42
	R21O = 43
	R22C = 44
	R23C = 45
	R23O = 46
	R24C = 47
	R258 = 48
	R318 = 49
	R31C = 50
	R31O = 51
	R32C = 52
	R33C = 53
	R33O = 54
	R34C = 55
	R418 = 56
	R41C = 57
	R41O = 58
	R42C = 59
	R43C = 60
	R43O = 61
	R44C = 62
	RA18 = 63
	RB14 = 64
	RB18 = 65
	RC18 = 66
	RD18 = 67
	RE18 = 68
	RF18 = 69
	RF1C = 70
	RF1O = 71
	RF2C = 72
	RF3C = 73
	RF3O = 74
	RF4C = 75
	RF5C = 76
	RF6C = 77
	RF7C = 78
	RF8C = 79
	RF9C = 80
	RFAC = 81
	RFAO = 82
	RFBC = 83
	RG18 = 84
	RH18 = 85


# noinspection SpellCheckingInspection
class TxConverter(Enum):
	"""40 Members, ITX1 ... TX44"""
	ITX1 = 0
	ITX11 = 1
	ITX12 = 2
	ITX13 = 3
	ITX14 = 4
	ITX2 = 5
	ITX21 = 6
	ITX22 = 7
	ITX23 = 8
	ITX24 = 9
	ITX3 = 10
	ITX31 = 11
	ITX32 = 12
	ITX33 = 13
	ITX34 = 14
	ITX4 = 15
	ITX41 = 16
	ITX42 = 17
	ITX43 = 18
	ITX44 = 19
	TX1 = 20
	TX11 = 21
	TX12 = 22
	TX13 = 23
	TX14 = 24
	TX2 = 25
	TX21 = 26
	TX22 = 27
	TX23 = 28
	TX24 = 29
	TX3 = 30
	TX31 = 31
	TX32 = 32
	TX33 = 33
	TX34 = 34
	TX4 = 35
	TX41 = 36
	TX42 = 37
	TX43 = 38
	TX44 = 39


# noinspection SpellCheckingInspection
class VoiceLinkType(Enum):
	"""2 Members, ESCO ... SCO"""
	ESCO = 0
	SCO = 1
