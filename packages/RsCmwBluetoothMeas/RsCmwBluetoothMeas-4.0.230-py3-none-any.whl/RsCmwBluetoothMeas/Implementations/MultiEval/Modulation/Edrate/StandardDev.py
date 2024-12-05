from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDevCls:
	"""StandardDev commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standardDev", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tol: float or bool: float Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.MultiEval.Scount#Modulation CMDLINKRESOLVED]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Omega_I: float or bool: float Standard deviation of the initial center frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Omega_Iplus_Omega_0_Max: float or bool: float Standard deviation of the maximum compensated frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Omega_0_Max: float or bool: float Standard deviation of the maximum compensated frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Rms_Devm: float or bool: float Standard deviation of the differential EVM results Range: 0 to 1
			- Peak_Devm: float or bool: float Range: 0 to 1
			- P_99_Devm: float or bool: float Range: 0 to 1
			- Nominal_Power: float or bool: float Standard deviation of the average power during the carrier-on state Range: 0 dB to 79 dB , Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Out_Of_Tol'),
			ArgStruct.scalar_float_ext('Omega_I'),
			ArgStruct.scalar_float_ext('Omega_Iplus_Omega_0_Max'),
			ArgStruct.scalar_float_ext('Omega_0_Max'),
			ArgStruct.scalar_float_ext('Rms_Devm'),
			ArgStruct.scalar_float_ext('Peak_Devm'),
			ArgStruct.scalar_float_ext('P_99_Devm'),
			ArgStruct.scalar_float_ext('Nominal_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float or bool = None
			self.Omega_I: float or bool = None
			self.Omega_Iplus_Omega_0_Max: float or bool = None
			self.Omega_0_Max: float or bool = None
			self.Rms_Devm: float or bool = None
			self.Peak_Devm: float or bool = None
			self.P_99_Devm: float or bool = None
			self.Nominal_Power: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:SDEViation \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.edrate.standardDev.calculate() \n
		Returns the standard deviation of the modulation results for EDR packets. The values described below are returned by
		FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:SDEViation?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.MultiEval.Scount#Modulation CMDLINKRESOLVED]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Omega_I: float: float Standard deviation of the initial center frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Omega_Iplus_Omega_0_Max: float: float Standard deviation of the maximum compensated frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Omega_0_Max: float: float Standard deviation of the maximum compensated frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Rms_Devm: float: float Standard deviation of the differential EVM results Range: 0 to 1
			- Peak_Devm: float: float Range: 0 to 1
			- P_99_Devm: float: float Range: 0 to 1
			- Nominal_Power: float: float Standard deviation of the average power during the carrier-on state Range: 0 dB to 79 dB , Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Omega_I'),
			ArgStruct.scalar_float('Omega_Iplus_Omega_0_Max'),
			ArgStruct.scalar_float('Omega_0_Max'),
			ArgStruct.scalar_float('Rms_Devm'),
			ArgStruct.scalar_float('Peak_Devm'),
			ArgStruct.scalar_float('P_99_Devm'),
			ArgStruct.scalar_float('Nominal_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Omega_I: float = None
			self.Omega_Iplus_Omega_0_Max: float = None
			self.Omega_0_Max: float = None
			self.Rms_Devm: float = None
			self.Peak_Devm: float = None
			self.P_99_Devm: float = None
			self.Nominal_Power: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.modulation.edrate.standardDev.fetch() \n
		Returns the standard deviation of the modulation results for EDR packets. The values described below are returned by
		FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:SDEViation?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.modulation.edrate.standardDev.read() \n
		Returns the standard deviation of the modulation results for EDR packets. The values described below are returned by
		FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:SDEViation?', self.__class__.ResultData())
