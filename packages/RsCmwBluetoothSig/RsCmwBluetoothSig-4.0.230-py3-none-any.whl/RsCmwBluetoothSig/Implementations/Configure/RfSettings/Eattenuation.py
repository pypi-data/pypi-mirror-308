from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EattenuationCls:
	"""Eattenuation commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eattenuation", core, parent)

	def get_output(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EATTenuation:OUTPut \n
		Snippet: value: float = driver.configure.rfSettings.eattenuation.get_output() \n
		Defines an external attenuation (or gain, if the value is negative) , to be applied to the output connector. \n
			:return: external_att: numeric Range: -50 dB to 90 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EATTenuation:OUTPut?')
		return Conversions.str_to_float(response)

	def set_output(self, external_att: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EATTenuation:OUTPut \n
		Snippet: driver.configure.rfSettings.eattenuation.set_output(external_att = 1.0) \n
		Defines an external attenuation (or gain, if the value is negative) , to be applied to the output connector. \n
			:param external_att: numeric Range: -50 dB to 90 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(external_att)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EATTenuation:OUTPut {param}')

	def get_input_py(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EATTenuation:INPut \n
		Snippet: value: float = driver.configure.rfSettings.eattenuation.get_input_py() \n
		Defines an external attenuation (or gain, if the value is negative) , to be applied to the input connector. \n
			:return: external_att: numeric Range: -50 dB to 90 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EATTenuation:INPut?')
		return Conversions.str_to_float(response)

	def set_input_py(self, external_att: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EATTenuation:INPut \n
		Snippet: driver.configure.rfSettings.eattenuation.set_input_py(external_att = 1.0) \n
		Defines an external attenuation (or gain, if the value is negative) , to be applied to the input connector. \n
			:param external_att: numeric Range: -50 dB to 90 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(external_att)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EATTenuation:INPut {param}')
