from . import _convlog

__all__ = (
    "__version__",
    "TenhouLogParsingError",
    "TenhouToMjaiError",
    "JsonSerializationError",
    "JsonParsingError",
    "tenhou_file_to_mjai",
)

# VERSION is set in Cargo.toml
VERSION = _convlog.__version__
__version__ = _convlog.__version__
TenhouLogParsingError = _convlog.TenhouLogParsingError
TenhouToMjaiError = _convlog.TenhouToMjaiError
JsonSerializationError = _convlog.JsonSerializationError
JsonParsingError = _convlog.JsonParsingError

tenhou_file_to_mjai = _convlog.tenhou_file_to_mjai
tenhou_to_mjai = _convlog.tenhou_to_mjai
