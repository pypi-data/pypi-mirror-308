from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- P_95_Zmd: float: float Result of 95% of ZMD value. Range: 0 deg to 360 deg
			- Nominal_Power: float: float Average power during the frequency step Range: -128 dBm to 50 dBm , Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('P_95_Zmd'),
			ArgStruct.scalar_float('Nominal_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.P_95_Zmd: float = None
			self.Nominal_Power: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:CSOunding:SPHase:CURRent \n
		Snippet: value: ResultData = driver.csounding.sphase.current.read() \n
		Returns the stable phase scalar results. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:CSOunding:SPHase:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:CSOunding:SPHase:CURRent \n
		Snippet: value: ResultData = driver.csounding.sphase.current.fetch() \n
		Returns the stable phase scalar results. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:CSOunding:SPHase:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- P_95_Zmd: float or bool: float Result of 95% of ZMD value. Range: 0 deg to 360 deg
			- Nominal_Power: float or bool: float Average power during the frequency step Range: -128 dBm to 50 dBm , Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('P_95_Zmd'),
			ArgStruct.scalar_float_ext('Nominal_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.P_95_Zmd: float or bool = None
			self.Nominal_Power: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:SPHase:CURRent \n
		Snippet: value: CalculateStruct = driver.csounding.sphase.current.calculate() \n
		Returns the stable phase scalar results. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:SPHase:CURRent?', self.__class__.CalculateStruct())
