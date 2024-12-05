from collections.abc import Sequence
import types
from typing import overload

import _shortfin_default.lib


class DType:
    @property
    def name(self) -> str: ...

    @property
    def is_boolean(self) -> bool: ...

    @property
    def is_integer(self) -> bool: ...

    @property
    def is_float(self) -> bool: ...

    @property
    def is_complex(self) -> bool: ...

    @property
    def bit_count(self) -> int: ...

    @property
    def is_byte_aligned(self) -> bool: ...

    @property
    def dense_byte_count(self) -> int: ...

    def is_integer_bitwidth(self, arg: int, /) -> bool: ...

    def compute_dense_nd_size(self, arg: Sequence[int], /) -> int: ...

    def __eq__(self, arg: DType, /) -> bool: ...

    def __repr__(self) -> str: ...

class RandomGenerator:
    def __init__(self, seed: int | None = None) -> None:
        """
        Returns an object for generating random numbers.

          Every instance is self contained and does not share state with others.

          Args:
            seed: Optional seed for the generator. Not setting a seed will cause an
              implementation defined value to be used, which may in fact be a completely
              fixed number.
        """

def argmax(input: device_array, axis: int = -1, out: device_array | None = None, *, keepdims: bool = False, device_visible: bool = False) -> device_array:
    """
    Returns the indices of the maximum values along an axis.

    Implemented for dtypes: float16, float32.

    Args:
      input: An input array.
      axis: Axis along which to sort. Defaults to the last axis (note that the
        numpy default is into the flattened array, which we do not support).
      keepdims: Whether to preserve the sort axis. If true, this will become a unit
        dim. If false, it will be removed.
      out: Array to write into. If specified, it must have an expected shape and
        int64 dtype.
      device_visible: Whether to make the result array visible to devices. Defaults to
        False.

    Returns:
      A device_array of dtype=int64, allocated on the host and not visible to the device.
    """

class base_array:
    @property
    def dtype(self) -> DType: ...

    @property
    def shape(self) -> list[int]: ...

bfloat16: DType = ...

bool8: DType = ...

complex128: DType = ...

complex64: DType = ...

class device_array(base_array):
    def __init__(*args, **kwargs) -> None: ...

    def __sfinv_marshal__(self, arg0: types.CapsuleType, arg1: int, /) -> None: ...

    @staticmethod
    def for_device(arg0: _shortfin_default.lib.local.ScopedDevice, arg1: Sequence[int], arg2: DType, /) -> object: ...

    @staticmethod
    def for_host(arg0: _shortfin_default.lib.local.ScopedDevice, arg1: Sequence[int], arg2: DType, /) -> object: ...

    def for_transfer(self) -> object: ...

    @property
    def device(self) -> _shortfin_default.lib.local.ScopedDevice: ...

    @property
    def storage(self) -> storage: ...

    def fill(self, pattern: object) -> None:
        """
        Fill an array with a value.

        Note that `fill` is asynchronous and may not be visible immediately. For immediate
        manipulation of host visible arrays, assign to the `items` property or use the
        `map(discard=True)` to get a mapping object which can be used to directly
        update the contents.

        Equivalent to `array.storage.fill(pattern)`.
        """

    def copy_from(self, source_array: device_array) -> None:
        """
        Copy contents from a source array to this array.

        Equivalent to `dest_array.storage.copy_from(source_array.storage)`.
        """

    def copy_to(self, dest_array: device_array) -> None:
        """
        Copy contents this array to a destination array.

        Equivalent to `dest_array.storage.copy_from(source_array.storage)`.
        """

    def view(self, *args) -> device_array:
        """
        Create a view of an array.

        Either integer indices or slices can be passed to the view() method to create
        an aliased device_array that shares a subset of the storage. Only view()
        organizations that result in a row-major, dense array are currently supported.
        """

    def map(self, *, read: bool = False, write: bool = False, discard: bool = False) -> object:
        """
        Create a typed mapping of the buffer contents in host memory.

        Support kwargs of:

        | read: Enables read access to the mapped memory.
        | write: Enables write access to the mapped memory and will flush upon close
          (for non-unified memory systems).
        | discard: Indicates that the entire memory map should be treated as if it will
          be overwritten. Initial contents will be undefined. Implies `write=True`.

        Mapping memory for access from the host requires a compatible buffer that has
        been created with host visibility (which includes host buffers).

        The returned mapping object is a context manager that will close/flush on
        exit. Alternatively, the `close()` method can be invoked explicitly.

        See also `storage.map()` which functions similarly but does not allow access
        to dtype specific functionality.
        """

    @property
    def items(self) -> object:
        """Convenience shorthand for map(...).items"""

    @items.setter
    def items(self, arg: object, /) -> None: ...

    @property
    def __array_interface__(self) -> dict: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

def fill_randn(out: device_array, generator: RandomGenerator | None = None) -> None:
    """
    Fills an array with numbers sampled from the standard ormal distribution.

    Values are samples with a mean of 0 and standard deviation of 1.

    This operates like torch.randn but only supports in place fills to an existing
    array, deriving shape and dtype from the output array.

    Args:
      out: Output array to fill.
      generator: Uses an explicit generator. If not specified, uses a global
        default.
    """

float16: DType = ...

float32: DType = ...

float64: DType = ...

int16: DType = ...

int32: DType = ...

int4: DType = ...

int64: DType = ...

int8: DType = ...

class mapping:
    def close(self) -> None: ...

    @property
    def valid(self) -> bool: ...

    def __enter__(self) -> object: ...

    def __exit__(self, exc_type: object | None, exc_value: object | None, exc_tb: object | None) -> None: ...

    @overload
    def fill(self, value: int) -> None:
        """
        Fill the host mapping with a pattern.

        The pattern can either be an object implementing the buffer protocol or a Python
        int/float if the mapping has a dtype. In this case, the numeric value will be
        converted to the appropriate typed pattern. Only dtypes supported by the
        array.array class are supported in this fashion.

        The pattern must evenly divide the mapping.

        Note that like all methods on a mapping, any changes are immediately visible
        (whereas the `fill` method on the array and storage are async operations).
        """

    @overload
    def fill(self, value: float) -> None: ...

    @overload
    def fill(self, buffer: object) -> None: ...

    @property
    def items(self) -> object:
        """
        Access contents as a Python array.

        When reading this attribute, an array.array will be constructed with the
        contents of the mapping. This supports a subset of element types (byte aligned
        integers, floats and doubles) corresponding to Python types.

        On write, the mapping will be written with arbitrary Python types marshaled
        via array.array into its contents.
        """

    @items.setter
    def items(self, arg: object, /) -> None: ...

opaque16: DType = ...

opaque32: DType = ...

opaque64: DType = ...

opaque8: DType = ...

sint16: DType = ...

sint32: DType = ...

sint4: DType = ...

sint64: DType = ...

sint8: DType = ...

class storage:
    def __sfinv_marshal__(self, arg0: types.CapsuleType, arg1: int, /) -> None: ...

    @staticmethod
    def allocate_host(device: _shortfin_default.lib.local.ScopedDevice, allocation_size: int) -> storage: ...

    @staticmethod
    def allocate_device(device: _shortfin_default.lib.local.ScopedDevice, allocation_size: int) -> storage: ...

    def fill(self, pattern: object) -> None:
        """
        Fill a storage with a value.

        Takes as argument any value that can be interpreted as a buffer with the Python
        buffer protocol of size 1, 2, or 4 bytes. The storage will be filled uniformly
        with the pattern.

        This operation executes asynchronously and the effect will only be visible
        once the execution fiber has been synced to the point of mutation.
        """

    def copy_from(self, source_storage: storage) -> None:
        """
        Copy contents from a source storage to this array.

        This operation executes asynchronously and the effect will only be visible
        once the execution fiber has been synced to the point of mutation.
        """

    def map(self, *, read: bool = False, write: bool = False, discard: bool = False) -> object:
        """
        Create a mapping of the buffer contents in host memory.

        Support kwargs of:

        | read: Enables read access to the mapped memory.
        | write: Enables write access to the mapped memory and will flush upon close
          (for non-unified memory systems).
        | discard: Indicates that the entire memory map should be treated as if it will
          be overwritten. Initial contents will be undefined. Implies `write=True`.

        Mapping memory for access from the host requires a compatible buffer that has
        been created with host visibility (which includes host buffers).

        The returned mapping object is a context manager that will close/flush on
        exit. Alternatively, the `close()` method can be invoked explicitly.

        See also `device_array.map()` which functions similarly but allows some
        additional dtype specific accessors.
        """

    def __eq__(self, arg: storage, /) -> bool: ...

    def __len__(self) -> int: ...

    def __repr__(self) -> str: ...

uint16: DType = ...

uint32: DType = ...

uint4: DType = ...

uint64: DType = ...

uint8: DType = ...
