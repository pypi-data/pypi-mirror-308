from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EdrateCls:
	"""Edrate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("edrate", core, parent)

	def fetch(self) -> int:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:ISIGnal:ADETected:PLENgth:EDRate \n
		Snippet: value: int = driver.inputSignal.adetected.plength.edrate.fetch() \n
		Returns the detected EDR payload length. A result is available after the R&S CMW has auto-detected a packet (method
		RsCmwBluetoothMeas.Configure.InputSignal.dmode AUTO) . \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: payload_length: decimal Range: 0 Byte(s) to 1021 Byte(s)"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:ISIGnal:ADETected:PLENgth:EDRate?', suppressed)
		return Conversions.str_to_int(response)
