from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Nominal_Power: float: float Average power during the frequency step Range: -128 dBm to 50 dBm, Unit: dBm
			- Ffo: float: float FFOk result Range: -200 kHz to 200 kHz
			- Ffo_Rel: float: float FFOk - FFO1 result Range: -50 kHz to 50 kHz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Ffo'),
			ArgStruct.scalar_float('Ffo_Rel')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nominal_Power: float = None
			self.Ffo: float = None
			self.Ffo_Rel: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:CSOunding:SFRequency:AVERage \n
		Snippet: value: ResultData = driver.csounding.sfrequency.average.read() \n
		Returns the step frequency scalar results. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:CSOunding:SFRequency:AVERage?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:CSOunding:SFRequency:AVERage \n
		Snippet: value: ResultData = driver.csounding.sfrequency.average.fetch() \n
		Returns the step frequency scalar results. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:CSOunding:SFRequency:AVERage?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Nominal_Power: float or bool: float Average power during the frequency step Range: -128 dBm to 50 dBm, Unit: dBm
			- Ffo: float or bool: float FFOk result Range: -200 kHz to 200 kHz
			- Ffo_Rel: float or bool: float FFOk - FFO1 result Range: -50 kHz to 50 kHz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Nominal_Power'),
			ArgStruct.scalar_float_ext('Ffo'),
			ArgStruct.scalar_float_ext('Ffo_Rel')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nominal_Power: float or bool = None
			self.Ffo: float or bool = None
			self.Ffo_Rel: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:SFRequency:AVERage \n
		Snippet: value: CalculateStruct = driver.csounding.sfrequency.average.calculate() \n
		Returns the step frequency scalar results. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:SFRequency:AVERage?', self.__class__.CalculateStruct())
