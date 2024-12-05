from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MindexCls:
	"""Mindex commands group definition. 18 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mindex", core, parent)

	@property
	def nmode(self):
		"""nmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmode'):
			from .Nmode import NmodeCls
			self._nmode = NmodeCls(self._core, self._cmd_group)
		return self._nmode

	@property
	def standard(self):
		"""standard commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_standard'):
			from .Standard import StandardCls
			self._standard = StandardCls(self._core, self._cmd_group)
		return self._standard

	@property
	def stable(self):
		"""stable commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_stable'):
			from .Stable import StableCls
			self._stable = StableCls(self._core, self._cmd_group)
		return self._stable

	@property
	def tmode(self):
		"""tmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmode'):
			from .Tmode import TmodeCls
			self._tmode = TmodeCls(self._core, self._cmd_group)
		return self._tmode

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	def get_brate(self) -> List[float or bool]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:BRATe \n
		Snippet: value: List[float or bool] = driver.configure.rfSettings.dtx.stab.mindex.get_brate() \n
		Return the modulation index under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for BR (..:BRATe..) , LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless tLE
		UTP test mode:echnology, see also 'Dirty TX Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: mod_index: (float or boolean items) float | ON | OFF Range: 0.2 to 0.55
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:BRATe?')
		return Conversions.str_to_float_or_bool_list(response)

	def clone(self) -> 'MindexCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MindexCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
