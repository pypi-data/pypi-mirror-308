from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaximumCls:
	"""Maximum commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Power_Ant_Path_1: float: float Range: -99.99 dBm to 99.99 dBm
			- Power_Ant_Path_2: float: float Range: -99.99 dBm to 99.99 dBm
			- Power_Ant_Path_3: float: float Range: -99.99 dBm to 99.99 dBm
			- Power_Ant_Path_4: float: float Range: -99.99 dBm to 99.99 dBm
			- Power_Tone_Ext: float: float Range: -99.99 dBm to 99.99 dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Power_Ant_Path_1'),
			ArgStruct.scalar_float('Power_Ant_Path_2'),
			ArgStruct.scalar_float('Power_Ant_Path_3'),
			ArgStruct.scalar_float('Power_Ant_Path_4'),
			ArgStruct.scalar_float('Power_Tone_Ext')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Power_Ant_Path_1: float = None
			self.Power_Ant_Path_2: float = None
			self.Power_Ant_Path_3: float = None
			self.Power_Ant_Path_4: float = None
			self.Power_Tone_Ext: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:CSOunding:PVAPath:MAXimum \n
		Snippet: value: ResultData = driver.csounding.pvaPath.maximum.read() \n
		Returns the power vs antenna path scalar results. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:CSOunding:PVAPath:MAXimum?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:CSOunding:PVAPath:MAXimum \n
		Snippet: value: ResultData = driver.csounding.pvaPath.maximum.fetch() \n
		Returns the power vs antenna path scalar results. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:CSOunding:PVAPath:MAXimum?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Power_Ant_Path_1: float or bool: float Range: -99.99 dBm to 99.99 dBm
			- Power_Ant_Path_2: float or bool: float Range: -99.99 dBm to 99.99 dBm
			- Power_Ant_Path_3: float or bool: float Range: -99.99 dBm to 99.99 dBm
			- Power_Ant_Path_4: float or bool: float Range: -99.99 dBm to 99.99 dBm
			- Power_Tone_Ext: float or bool: float Range: -99.99 dBm to 99.99 dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Power_Ant_Path_1'),
			ArgStruct.scalar_float_ext('Power_Ant_Path_2'),
			ArgStruct.scalar_float_ext('Power_Ant_Path_3'),
			ArgStruct.scalar_float_ext('Power_Ant_Path_4'),
			ArgStruct.scalar_float_ext('Power_Tone_Ext')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Power_Ant_Path_1: float or bool = None
			self.Power_Ant_Path_2: float or bool = None
			self.Power_Ant_Path_3: float or bool = None
			self.Power_Ant_Path_4: float or bool = None
			self.Power_Tone_Ext: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:PVAPath:MAXimum \n
		Snippet: value: CalculateStruct = driver.csounding.pvaPath.maximum.calculate() \n
		Returns the power vs antenna path scalar results. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:PVAPath:MAXimum?', self.__class__.CalculateStruct())
