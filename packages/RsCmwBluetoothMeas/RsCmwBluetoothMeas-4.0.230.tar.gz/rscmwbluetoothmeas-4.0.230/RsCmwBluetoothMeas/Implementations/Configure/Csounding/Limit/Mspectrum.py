from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MspectrumCls:
	"""Mspectrum commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mspectrum", core, parent)

	def set(self, mod_thresh: float, fh_min_fl_lim_lower: float, fh_min_fl_enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:MSPectrum \n
		Snippet: driver.configure.csounding.limit.mspectrum.set(mod_thresh = 1.0, fh_min_fl_lim_lower = 1.0, fh_min_fl_enable = False) \n
		Sets the limits for | fL - fH | that is calculated from the frequencies at the power Ppeak - <ModThresh> \n
			:param mod_thresh: float Threshold from peak emission Range: -40 dB to 0 dB
			:param fh_min_fl_lim_lower: float Lower limit for | fL - fH | Range: 0 MHz to 3 MHz
			:param fh_min_fl_enable: OFF | ON Disables or enables the limit check.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('mod_thresh', mod_thresh, DataType.Float), ArgSingle('fh_min_fl_lim_lower', fh_min_fl_lim_lower, DataType.Float), ArgSingle('fh_min_fl_enable', fh_min_fl_enable, DataType.Boolean))
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:MSPectrum {param}'.rstrip())

	# noinspection PyTypeChecker
	class MspectrumStruct(StructBase):
		"""Response structure. Fields: \n
			- Mod_Thresh: float: float Threshold from peak emission Range: -40 dB to 0 dB
			- Fh_Min_Fl_Lim_Lower: float: No parameter help available
			- Fh_Min_Fl_Enable: bool: OFF | ON Disables or enables the limit check."""
		__meta_args_list = [
			ArgStruct.scalar_float('Mod_Thresh'),
			ArgStruct.scalar_float('Fh_Min_Fl_Lim_Lower'),
			ArgStruct.scalar_bool('Fh_Min_Fl_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mod_Thresh: float = None
			self.Fh_Min_Fl_Lim_Lower: float = None
			self.Fh_Min_Fl_Enable: bool = None

	def get(self) -> MspectrumStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:MSPectrum \n
		Snippet: value: MspectrumStruct = driver.configure.csounding.limit.mspectrum.get() \n
		Sets the limits for | fL - fH | that is calculated from the frequencies at the power Ppeak - <ModThresh> \n
			:return: structure: for return value, see the help for MspectrumStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:MSPectrum?', self.__class__.MspectrumStruct())
