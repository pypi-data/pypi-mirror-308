from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtendedCls:
	"""Extended commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("extended", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Seg_Reliability: int: decimal Reliability indicator for the segment. The meaning of the returned values is the same as for the common reliability indicator, see previous parameter.
			- Out_Of_Tol: float: float Percentage of measured bursts with failed limit check Range: 0 % to 100 % , Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Freq_Acc_Or_Init_Freq_Error: float: float Frequency accuracy (BR, LE) or initial center frequency error omegai (EDR) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Drift: float: float Frequency drift (BR, LE) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Max_Drift_Rate: float: float Maximal drift rate (BR, LE) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz/50 us (LE coded PHY: Hz/48 us)
			- Delta_F_1_Avg: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_1_Min: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_1_Max: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_2_Avg: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_2_Min: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_2_Max: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Omegai_Omega_0: float: No parameter help available
			- Omega_0_Max: float: float Maximum compensated frequency error (EDR) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Rms_Devm: float: float RMS DEVM (EDR) Range: 0.0 to 1.0
			- Peak_Devm: float: float Peak DEVM (EDR) Range: 0.0 to 1.0
			- Freq_Offset: float: float Frequency offset (LE) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Init_Freq_Drift: float: float Initial frequency drift (LE) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Cte_Freq_Drift: float: No parameter help available
			- Cte_Mx_Drift_Rate: float: No parameter help available
			- Cte_Freq_Offset: float: No parameter help available
			- Cte_Int_Frq_Drift: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Freq_Acc_Or_Init_Freq_Error'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift_Rate'),
			ArgStruct.scalar_float('Delta_F_1_Avg'),
			ArgStruct.scalar_float('Delta_F_1_Min'),
			ArgStruct.scalar_float('Delta_F_1_Max'),
			ArgStruct.scalar_float('Delta_F_2_Avg'),
			ArgStruct.scalar_float('Delta_F_2_Min'),
			ArgStruct.scalar_float('Delta_F_2_Max'),
			ArgStruct.scalar_float('Omegai_Omega_0'),
			ArgStruct.scalar_float('Omega_0_Max'),
			ArgStruct.scalar_float('Rms_Devm'),
			ArgStruct.scalar_float('Peak_Devm'),
			ArgStruct.scalar_float('Freq_Offset'),
			ArgStruct.scalar_float('Init_Freq_Drift'),
			ArgStruct.scalar_float('Cte_Freq_Drift'),
			ArgStruct.scalar_float('Cte_Mx_Drift_Rate'),
			ArgStruct.scalar_float('Cte_Freq_Offset'),
			ArgStruct.scalar_float('Cte_Int_Frq_Drift')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.Freq_Acc_Or_Init_Freq_Error: float = None
			self.Freq_Drift: float = None
			self.Max_Drift_Rate: float = None
			self.Delta_F_1_Avg: float = None
			self.Delta_F_1_Min: float = None
			self.Delta_F_1_Max: float = None
			self.Delta_F_2_Avg: float = None
			self.Delta_F_2_Min: float = None
			self.Delta_F_2_Max: float = None
			self.Omegai_Omega_0: float = None
			self.Omega_0_Max: float = None
			self.Rms_Devm: float = None
			self.Peak_Devm: float = None
			self.Freq_Offset: float = None
			self.Init_Freq_Drift: float = None
			self.Cte_Freq_Drift: float = None
			self.Cte_Mx_Drift_Rate: float = None
			self.Cte_Freq_Offset: float = None
			self.Cte_Int_Frq_Drift: float = None

	def fetch(self, segment=repcap.Segment.Default) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:MODulation:MAXimum:EXTended \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.modulation.maximum.extended.fetch(segment = repcap.Segment.Default) \n
		Returns single maximum modulation results for segment<no> in list mode including Bluetooth version 5.0 and higher.
		The command returns all parameters listed below, independent of the selected list mode setup. However, only for some of
		the parameters measured values are available. For the other parameters, only an indicator is returned (e.g. NAV) . \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		segment_cmd_val = self._cmd_group.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:MODulation:MAXimum:EXTended?', self.__class__.FetchStruct())
