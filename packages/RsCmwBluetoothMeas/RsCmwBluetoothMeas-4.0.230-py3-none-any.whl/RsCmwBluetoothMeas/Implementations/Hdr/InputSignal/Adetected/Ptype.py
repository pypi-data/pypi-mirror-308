from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PtypeCls:
	"""Ptype commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ptype", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.PacketTypeIsignal:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:HDR:ISIGnal:ADETected:PTYPe \n
		Snippet: value: enums.PacketTypeIsignal = driver.hdr.inputSignal.adetected.ptype.fetch() \n
		No command help available \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: packet_type: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:HDR:ISIGnal:ADETected:PTYPe?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.PacketTypeIsignal)
