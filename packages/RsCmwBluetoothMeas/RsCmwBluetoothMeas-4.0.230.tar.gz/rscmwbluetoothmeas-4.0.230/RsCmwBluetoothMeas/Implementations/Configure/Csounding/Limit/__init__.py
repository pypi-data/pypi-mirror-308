from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LimitCls:
	"""Limit commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("limit", core, parent)

	@property
	def mspectrum(self):
		"""mspectrum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mspectrum'):
			from .Mspectrum import MspectrumCls
			self._mspectrum = MspectrumCls(self._core, self._cmd_group)
		return self._mspectrum

	# noinspection PyTypeChecker
	class SphaseStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Fields: \n
			- P_95_Zmd_Lim_Upper_1: float: numeric Fizmd measured at antenna 1 Range: 0 deg to 180 deg
			- P_95_Zmd_Lim_Upper_2: float: numeric Fizmd measured at antenna 2 Range: 0 deg to 180 deg
			- P_95_Zmd_Lim_Upper_3: float: numeric Fizmd measured at antenna 3 Range: 0 deg to 180 deg
			- P_95_Zmd_Lim_Upper_4: float: numeric Fizmd measured at antenna 4 Range: 0 deg to 180 deg
			- P_95_Zmd_Enable_1: bool: OFF | ON Enables or disables the limit check for antenna 1.
			- P_95_Zmd_Enable_2: bool: OFF | ON Enables or disables the limit check for antenna 2.
			- P_95_Zmd_Enable_3: bool: OFF | ON Enables or disables the limit check for antenna 3.
			- P_95_Zmd_Enable_4: bool: OFF | ON Enables or disables the limit check for antenna 4."""
		__meta_args_list = [
			ArgStruct.scalar_float('P_95_Zmd_Lim_Upper_1'),
			ArgStruct.scalar_float('P_95_Zmd_Lim_Upper_2'),
			ArgStruct.scalar_float('P_95_Zmd_Lim_Upper_3'),
			ArgStruct.scalar_float('P_95_Zmd_Lim_Upper_4'),
			ArgStruct.scalar_bool('P_95_Zmd_Enable_1'),
			ArgStruct.scalar_bool('P_95_Zmd_Enable_2'),
			ArgStruct.scalar_bool('P_95_Zmd_Enable_3'),
			ArgStruct.scalar_bool('P_95_Zmd_Enable_4')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.P_95_Zmd_Lim_Upper_1: float = None
			self.P_95_Zmd_Lim_Upper_2: float = None
			self.P_95_Zmd_Lim_Upper_3: float = None
			self.P_95_Zmd_Lim_Upper_4: float = None
			self.P_95_Zmd_Enable_1: bool = None
			self.P_95_Zmd_Enable_2: bool = None
			self.P_95_Zmd_Enable_3: bool = None
			self.P_95_Zmd_Enable_4: bool = None

	def get_sphase(self) -> SphaseStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:SPHase \n
		Snippet: value: SphaseStruct = driver.configure.csounding.limit.get_sphase() \n
		Enables or disables and sets the upper limit for the zero mean detrended phase (Fizmd) in the phase of the carrier. Fizmd \n
			:return: structure: for return value, see the help for SphaseStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:SPHase?', self.__class__.SphaseStruct())

	def set_sphase(self, value: SphaseStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:SPHase \n
		Snippet with structure: \n
		structure = driver.configure.csounding.limit.SphaseStruct() \n
		structure.P_95_Zmd_Lim_Upper_1: float = 1.0 \n
		structure.P_95_Zmd_Lim_Upper_2: float = 1.0 \n
		structure.P_95_Zmd_Lim_Upper_3: float = 1.0 \n
		structure.P_95_Zmd_Lim_Upper_4: float = 1.0 \n
		structure.P_95_Zmd_Enable_1: bool = False \n
		structure.P_95_Zmd_Enable_2: bool = False \n
		structure.P_95_Zmd_Enable_3: bool = False \n
		structure.P_95_Zmd_Enable_4: bool = False \n
		driver.configure.csounding.limit.set_sphase(value = structure) \n
		Enables or disables and sets the upper limit for the zero mean detrended phase (Fizmd) in the phase of the carrier. Fizmd \n
			:param value: see the help for SphaseStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:SPHase', value)

	# noinspection PyTypeChecker
	class SfrequencyStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Fields: \n
			- Ffo_Lim_Upper: float: float FFO[k] upper limit Range: 0 ppm to 100 ppm
			- Ffo_Rel_Lim_Upper: float: No parameter help available
			- Ftone_Rel_Cfo: float: float 95% |ftone(k,1) -CFO[k]| upper limit Range: 0 kHz to 50 kHz
			- Fexp_Rel_Cfo: float: float 95% |fE,offset[k]-CFO[k]| upper limit Range: 0 kHz to 50 kHz
			- Fexp_Rel_Ftone_1: float: No parameter help available
			- Fexp_Rel_Ftone_2: float: No parameter help available
			- Fexp_Rel_Ftone_3: float: No parameter help available
			- Fexp_Rel_Ftone_4: float: No parameter help available
			- Ffo_Enable: List[bool]: No parameter help available
			- Ffo_Rel_Enable: List[bool]: No parameter help available
			- Ftone_Rel_Cfo_En: bool: No parameter help available
			- Fexp_Rel_Cfo_En: bool: OFF | ON Disables or enables the limit check of 4_FExpRelCFO.
			- Fexp_Rel_Ftone_En: List[bool]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ffo_Lim_Upper'),
			ArgStruct.scalar_float('Ffo_Rel_Lim_Upper'),
			ArgStruct.scalar_float('Ftone_Rel_Cfo'),
			ArgStruct.scalar_float('Fexp_Rel_Cfo'),
			ArgStruct.scalar_float('Fexp_Rel_Ftone_1'),
			ArgStruct.scalar_float('Fexp_Rel_Ftone_2'),
			ArgStruct.scalar_float('Fexp_Rel_Ftone_3'),
			ArgStruct.scalar_float('Fexp_Rel_Ftone_4'),
			ArgStruct('Ffo_Enable', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Ffo_Rel_Enable', DataType.BooleanList, None, False, False, 3),
			ArgStruct.scalar_bool('Ftone_Rel_Cfo_En'),
			ArgStruct.scalar_bool('Fexp_Rel_Cfo_En'),
			ArgStruct('Fexp_Rel_Ftone_En', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ffo_Lim_Upper: float = None
			self.Ffo_Rel_Lim_Upper: float = None
			self.Ftone_Rel_Cfo: float = None
			self.Fexp_Rel_Cfo: float = None
			self.Fexp_Rel_Ftone_1: float = None
			self.Fexp_Rel_Ftone_2: float = None
			self.Fexp_Rel_Ftone_3: float = None
			self.Fexp_Rel_Ftone_4: float = None
			self.Ffo_Enable: List[bool] = None
			self.Ffo_Rel_Enable: List[bool] = None
			self.Ftone_Rel_Cfo_En: bool = None
			self.Fexp_Rel_Cfo_En: bool = None
			self.Fexp_Rel_Ftone_En: List[bool] = None

	def get_sfrequency(self) -> SfrequencyStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:SFRequency \n
		Snippet: value: SfrequencyStruct = driver.configure.csounding.limit.get_sfrequency() \n
		Configures the step frequency verification limits. \n
			:return: structure: for return value, see the help for SfrequencyStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:SFRequency?', self.__class__.SfrequencyStruct())

	def set_sfrequency(self, value: SfrequencyStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:SFRequency \n
		Snippet with structure: \n
		structure = driver.configure.csounding.limit.SfrequencyStruct() \n
		structure.Ffo_Lim_Upper: float = 1.0 \n
		structure.Ffo_Rel_Lim_Upper: float = 1.0 \n
		structure.Ftone_Rel_Cfo: float = 1.0 \n
		structure.Fexp_Rel_Cfo: float = 1.0 \n
		structure.Fexp_Rel_Ftone_1: float = 1.0 \n
		structure.Fexp_Rel_Ftone_2: float = 1.0 \n
		structure.Fexp_Rel_Ftone_3: float = 1.0 \n
		structure.Fexp_Rel_Ftone_4: float = 1.0 \n
		structure.Ffo_Enable: List[bool] = [True, False, True] \n
		structure.Ffo_Rel_Enable: List[bool] = [True, False, True] \n
		structure.Ftone_Rel_Cfo_En: bool = False \n
		structure.Fexp_Rel_Cfo_En: bool = False \n
		structure.Fexp_Rel_Ftone_En: List[bool] = [True, False, True] \n
		driver.configure.csounding.limit.set_sfrequency(value = structure) \n
		Configures the step frequency verification limits. \n
			:param value: see the help for SfrequencyStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:SFRequency', value)

	# noinspection PyTypeChecker
	class PowerStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Fields: \n
			- Pwr_Up_Ramp_Th: float: float Threshold from the level of the CS burst for the power-up ramp. Range: -60 dB to 0 dB
			- Pwr_Up_Ramp_Lim_Up: float: float Upper limit for power-up ramp duration starting at the CS level - threshold value until reaching the level of CS signal. Range: -60 dB to 0 dB
			- Pwr_Dwn_Ramp_Th: float: float Threshold from the level of the CS burst for the power-down ramp. Range: -60 dB to 0 dB
			- Pwr_Dwn_Ramp_Lim_Up: float: float Upper limit for power-down ramp duration starting at the end of CS burst until reaching the CS level - threshold value. Range: 0 us to 25 us
			- Pwr_Up_Ramp_En: List[bool]: OFF | ON Enables the limit check for power-up ramp duration. Four values: for current, average, maximal, and minimal results.
			- Pwr_Dwn_Ramp_En: List[bool]: OFF | ON Enables the limit check for power-down ramp duration. Four values: for current, average, maximal, and minimal results."""
		__meta_args_list = [
			ArgStruct.scalar_float('Pwr_Up_Ramp_Th'),
			ArgStruct.scalar_float('Pwr_Up_Ramp_Lim_Up'),
			ArgStruct.scalar_float('Pwr_Dwn_Ramp_Th'),
			ArgStruct.scalar_float('Pwr_Dwn_Ramp_Lim_Up'),
			ArgStruct('Pwr_Up_Ramp_En', DataType.BooleanList, None, False, False, 4),
			ArgStruct('Pwr_Dwn_Ramp_En', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pwr_Up_Ramp_Th: float = None
			self.Pwr_Up_Ramp_Lim_Up: float = None
			self.Pwr_Dwn_Ramp_Th: float = None
			self.Pwr_Dwn_Ramp_Lim_Up: float = None
			self.Pwr_Up_Ramp_En: List[bool] = None
			self.Pwr_Dwn_Ramp_En: List[bool] = None

	def get_power(self) -> PowerStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:POWer \n
		Snippet: value: PowerStruct = driver.configure.csounding.limit.get_power() \n
		Enables, disables and sets the power vs time limits. \n
			:return: structure: for return value, see the help for PowerStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:POWer?', self.__class__.PowerStruct())

	def set_power(self, value: PowerStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:POWer \n
		Snippet with structure: \n
		structure = driver.configure.csounding.limit.PowerStruct() \n
		structure.Pwr_Up_Ramp_Th: float = 1.0 \n
		structure.Pwr_Up_Ramp_Lim_Up: float = 1.0 \n
		structure.Pwr_Dwn_Ramp_Th: float = 1.0 \n
		structure.Pwr_Dwn_Ramp_Lim_Up: float = 1.0 \n
		structure.Pwr_Up_Ramp_En: List[bool] = [True, False, True] \n
		structure.Pwr_Dwn_Ramp_En: List[bool] = [True, False, True] \n
		driver.configure.csounding.limit.set_power(value = structure) \n
		Enables, disables and sets the power vs time limits. \n
			:param value: see the help for PowerStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:LIMit:POWer', value)

	def clone(self) -> 'LimitCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LimitCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
