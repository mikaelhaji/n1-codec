Blosc![ref1]

class numcodecs.blosc.Blosc(cname='lz4', clevel=5, shuffle=1, blocksize=0)

Codec providing compression using the Blosc meta-compressor.

Parameters: cname : string, optional

A string  naming  one  of the  compression algorithms available within blosc, e.g., ‘zstd’, ‘blosclz’, ‘lz4’, ‘lz4hc’, ‘zlib’ or ‘snappy’.

clevel : integer, optional

An integer between 0 and 9 specifying the compression level.

shuffle : integer, optional

Either  NOSHUFFLE  (0),  SHUFFLE  (1),  BITSHUFFLE  (2)  or AUTOSHUFFLE (-1). If AUTOSHUFFLE, bit-shuffle will be used for buffers with  itemsize  1,  and  byte-shuffle  will be  used  otherwise.  The  default  is SHUFFLE.

blocksize : int

The  requested size  of the  compressed blocks.  If 0 (default),  an  automatic blocksize will be used.

See also:![](Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.002.png)

[numcodecs.zstd.Zstd, num](https://numcodecs.readthedocs.io/en/stable/zstd.html#numcodecs.zstd.Zstd)c[odecs.lz4.LZ4](https://numcodecs.readthedocs.io/en/stable/lz4.html#numcodecs.lz4.LZ4)

codec\_id = 'blosc'

Codec identifier.

NOSHUFFLE = 0 SHUFFLE = 1 BITSHUFFLE = 2 AUTOSHUFFLE = -1 encode(self, buf) decode(self, buf, out=None) get\_config()

Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encodi-ng    .                    ×

classmethod from\_config(config)

Instantiate codec from a configuration object.           decode\_partial(self, buf, int start, int nitems, out=None)

Experimental

Helper functions![ref1]

numcodecs.blosc.init()

Initialize the Blosc library environment.

numcodecs.blosc.destroy()

Destroy the Blosc library environment.

numcodecs.blosc.compname\_to\_compcode(cname)

Return the compressor code associated with the compressor name. If the compressor name is not recognized, or there is not support for it in this build, -1 is returned instead.

numcodecs.blosc.list\_compressors()

Get a list of compressors supported in the current build.

numcodecs.blosc.get\_nthreads()

Get the number of threads that Blosc uses internally for compression and decompression.

numcodecs.blosc.set\_nthreads(int nthreads)

Set the number of threads that Blosc uses internally for compression and decompression.

numcodecs.blosc.cbuffer\_sizes(source)

Return  information about  a  compressed  buffer,  namely  the  number  of uncompressed  bytes (nbytes) and compressed (cbytes). It also returns the blocksize (which is used internally for do‐ ing the compression by blocks).

Returns: nbytes : int

cbytes : int blocksize : int

numcodecs.blosc.cbuffer\_complib(source)

Return the name of the compression library used to compress source.

numcodecs.blosc.cbuffer\_metainfo(source)

Return  some meta-information about the  compressed buffer in source, including  the  typesize, whether the shuffle or bit-shuffle filters were used, and the whether the buffer was memcpyed.

Returns : typesize -                        ×

shuffle

memcpyed

numcodecs.blosc.compress(source, char \*cname, int clevel, int shuffle=SHUFFLE, int blocksize=AUTOBLOCKS)

Compress data.

Parameters: source : bytes-like

Data to be compressed. Can be any object supporting the buffer protocol. cname : bytes

Name of compression library to use.

clevel : int

Compression level.

shuffle : int

Either  NOSHUFFLE  (0),  SHUFFLE  (1),  BITSHUFFLE  (2)  or AUTOSHUFFLE (-1). If AUTOSHUFFLE, bit-shuffle will be used for buffers with  itemsize  1,  and  byte-shuffle  will be  used  otherwise.  The  default  is SHUFFLE.

blocksize : int

The requested size of the compressed blocks. If 0, an automatic blocksize will be used.

Returns: dest : bytes

Compressed data.

numcodecs.blosc.decompress(source, dest=None)

Decompress data.

Parameters: source : bytes-like

Compressed  data,  including  blosc  header. Can  be  any  object  supporting the buffer protocol.

dest : array-like, optional

Object to decompress into.

Returns: dest : bytes

Object containing decompressed data.

numcodecs.blosc.decompress\_partial(source, start, nitems, dest=None)

Experimental Decompress data of only a part of a buffer.

Parameters: source : bytes-like

Compressed  data,  including  blosc  header. Can  be  any  object  supporting

the buf fer protocol. -                        × start: int,

Offset in item where we want to start decoding

nitems: int

Number of items we want to decode

dest : array-like, optional

Object to decompress into.

Returns: dest : bytes

Object containing decompressed data.

- ×

BZ2![ref1]

class numcodecs.bz2.BZ2(level=1) [source]

Codec providing compression using bzip2 via the Python standard library.

Parameters: level : int

Compression level.

codec\_id = 'bz2'

Codec identifier.

encode(buf) [sou[rce\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/bz2.html#BZ2.encode)

Encode data in buf.

Parameters: buf : buffer-like

Data  to be  encoded. May be  any  object  supporting the  new-style buf‐ fer protocol.

Returns: enc : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

decode(buf, out=None) [source[\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/bz2.html#BZ2.decode)

Decode data in buf.

Parameters: buf : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

out : buffer-like, optional

Writeable  buffer  to  store  decoded  data.  N.B.  if provided,  this  buffer must be exactly the right size to store the decoded data.

Returns: dec : buffer-like

Decoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

get\_config()

Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encoding.

classmethod from\_config(config)

Instantiate codec from a configuration object.

- ×

Codec API![ref1]

This module defines the Codec base class, a common interface for all codec classes.

Codec classes must implement  Codec.encode() and  Codec.decode() methods. Inputs to and outputs from  these  methods  may  be  any  Python  object  exporting  a  contiguous  buffer  via  the  new-style Python protocol.

Codec classes must implement a  Codec.get\_config() method, which must return a dictionary hold‐ ing all configuration  parameters  required  to enable  encoding  and  decoding  of data.  The  expecta‐ tion is that  these configuration  parameters  will be  stored  or communicated  separately from encod‐

ed  data,  and  thus  the  codecs  do  not  need  to  store  all encoding  parameters  within the  encoded data.  For broad  compatibility, the  configuration  object  must  contain  only JSON-serializable values. The configuration object must also contain an ‘id’ field storing the codec identifier (see below).

Codec classes must  implement a  Codec.from\_config() class method, which will return  an  instance of the class initialized from a configuration object.

Finally, codec classes must set a codec\_id class-level attribute. This must be a string. Two different codec classes may set the same value for the codec\_id attribute if and only if they are fully compat‐ ible,  meaning  that  (1) configuration  parameters  are  the  same,  and  (2) given  the  same  configura‐ tion, one class could correctly decode data encoded by the other and vice versa.

class numcodecs.abc.Codec [source]

Codec abstract base class.

codec\_id = None

Codec identifier.

abstract encode(buf) [sou[rce\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/abc.html#Codec.encode)

Encode data in buf.

Parameters: buf : buffer-like

Data  to be  encoded. May be  any  object  supporting the  new-style buf‐ fer protocol.

Returns: enc : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

abstract decode(buf, out=None) [source[\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/abc.html#Codec.decode)

Decode data in buf.

Parameters: buf : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new--st      yl    e       b    u  ff  e×r protocol.

out : buffer-like, optional

Writeable  buffer  to  store  decoded  data.  N.B.  if provided,  this  buffer must be exactly the right size to store the decoded data.

Returns: dec : buffer-like

Decoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

get\_config() [sour[ce\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/abc.html#Codec.get_config)

Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encoding.

classmethod from\_config(config) [source]

Instantiate codec from a configuration object.

- ×

Codec registry![ref1]

The registry module provides some simple convenience functions to enable applications to dynami‐ cally register and look-up codec classes.

numcodecs.registry.get\_codec(config) [source]

Obtain a codec for the given configuration.

Parameters: config : dict-like Configuration object.

Returns: codec : Codec Examples![ref2]

\>>> import numcodecs as codecs

\>>> codec = codecs.get\_codec(dict(id='zlib', level=1)) >>> codec

Zlib(level=1)![ref3]

numcodecs.registry.register\_codec(cls, codec\_id=None) [source]

Register a codec class.

Parameters: cls : Codec class Notes

This  function  maintains  a  mapping  from  codec  identifiers  to  codec  classes.  When  a  codec class is registered, it will replace any class previously registered under the same codec identifi‐ er, if present.

- ×

Delta![ref1]

class numcodecs.delta.Delta(dtype, astype=None) [source]

Codec to encode data as the difference between adjacent values.

Parameters: dtype : dtype

Data type to use for decoded data.

astype : dtype, optional

Data type to use for encoded data.

Notes

If astype is an integer data type, please ensure that it is sufficiently large to store encoded val‐ ues. No checks are made and data may become corrupted due to integer overflow if astype is too  small.  Note  also  that  the  encoded data  for each chunk  includes the  absolute value  of the first element in the  chunk,  and  so  the encoded data  type  in general needs to be  large  enough to store absolute values from the array.

Examples![ref3]

\>>> import numcodecs

\>>> import numpy as np

\>>> x = np.arange(100, 120, 2, dtype='i2')

\>>> codec = numcodecs.Delta(dtype='i2', astype='i1')

\>>> y = codec.encode(x)

\>>> y

array([100,   2,   2,   2,   2,   2,   2,   2,   2,   2], dtype=int8) >>> z = codec.decode(y)

\>>> z

array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118], dtype=int16)![ref2]

codec\_id = 'delta'

Codec identifier.

encode(buf) [sou[rce\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/delta.html#Delta.encode)

Encode data in buf.

Parameters: buf : buffer-like

Data  to be  encoded. May be  any  object  supporting the  new-style buf‐ fer protocol.

Returns: enc : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

- ×

decode(buf, out=None) [source[\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/delta.html#Delta.decode)

Decode data in buf.

Parameters: buf : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

out : buffer-like, optional

Writeable  buffer  to  store  decoded  data.  N.B.  if provided,  this  buffer must be exactly the right size to store the decoded data.

Returns: dec : buffer-like

Decoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

get\_config() [sour[ce\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/delta.html#Delta.get_config)

Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encoding.

classmethod from\_config(config)

Instantiate codec from a configuration object.

- ×

GZip![ref1]

class numcodecs.gzip.GZip(level=1) [source]

Codec providing gzip compression using zlib via the Python standard library.

Parameters: level : int

Compression level.

codec\_id = 'gzip'

Codec identifier.

encode(buf) [sou[rce\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/gzip.html#GZip.encode)

Encode data in buf.

Parameters: buf : buffer-like

Data  to be  encoded. May be  any  object  supporting the  new-style buf‐ fer protocol.

Returns: enc : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

decode(buf, out=None) [source[\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/gzip.html#GZip.decode)

Decode data in buf.

Parameters: buf : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

out : buffer-like, optional

Writeable  buffer  to  store  decoded  data.  N.B.  if provided,  this  buffer must be exactly the right size to store the decoded data.

Returns: dec : buffer-like

Decoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

get\_config()

Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encoding.

classmethod from\_config(config)

Instantiate codec from a configuration object.

- ×

LZ4![ref1]

class numcodecs.lz4.LZ4(acceleration=1)

Codec providing compression using LZ4.

Parameters: acceleration : int

Acceleration  level. The  larger  the  acceleration  value,  the  faster  the  algo‐ rithm, but also the lesser the compression.

See also:![](Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.005.png)

[numcodecs.zstd.Zstd, num](https://numcodecs.readthedocs.io/en/stable/zstd.html#numcodecs.zstd.Zstd)c[odecs.blosc.Blosc](https://numcodecs.readthedocs.io/en/stable/blosc.html#numcodecs.blosc.Blosc)

codec\_id = 'lz4'

Codec identifier.

encode(self, buf) decode(self, buf, out=None) get\_config()

Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encoding.

classmethod from\_config(config)

Instantiate codec from a configuration object.

Helper functions![ref1]

numcodecs.lz4.compress(source, int acceleration=DEFAULT\_ACCELERATION)

Compress data.

Parameters: source : bytes-like

Data to be compressed. Can be any object supporting the buffer protocol.

acceleration : int

Acceleration  level. The  larger  the  acceleration  value,  the  faster  the  algo‐ rithm, but also the lesser the compression.

Returns: dest : bytes

Compressed data.

Notes -                        ×


The compressed output includes a 4-byte header storing the original size of the decompressed data as a little-endian 32-bit integer.

numcodecs.lz4.decompress(source, dest=None)

Decompress data.

Parameters: source : bytes-like

Compressed data. Can be any object supporting the buffer protocol.

dest : array-like, optional

Object to decompress into.

Returns: dest : bytes

Object containing decompressed data.

- ×

LZMA![ref1]

class numcodecs.lzma.LZMA(format=1, check=-1, preset=None, filters=None) [\[source\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/lzma.html#LZMA)

Codec providing compression using lzma via the Python standard library.

Parameters: format : integer, optional

One of the lzma format codes, e.g., lzma.FORMAT\_XZ.

check : integer, optional

One of the lzma check codes, e.g., lzma.CHECK\_NONE.

preset : integer, optional

An integer between 0 and 9 inclusive, specifying the compression level.

filters : list, optional

A list of dictionaries  specifying  compression  filters.  If filters  are  provided, ‘preset’ must be None.

codec\_id = 'lzma'

Codec identifier.

encode(buf) [sou[rce\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/lzma.html#LZMA.encode)

Encode data in buf.

Parameters: buf : buffer-like

Data  to be  encoded. May be  any  object  supporting the  new-style buf‐ fer protocol.

Returns: enc : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

decode(buf, out=None) [source[\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/lzma.html#LZMA.decode)

Decode data in buf.

Parameters: buf : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

out : buffer-like, optional

Writeable  buffer  to  store  decoded  data.  N.B.  if provided,  this  buffer must be exactly the right size to store the decoded data.

Returns: dec : buffer-like

- ×

Decoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.


get\_config()

Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encoding.

classmethod from\_config(config)

Instantiate codec from a configuration object.

- ×

Numcodecs![ref1]

Numcodecs is a Python  package providing  buffer compression and  transformation codecs for use in data storage and communication applications. These include:

- Compression codecs, e.g., Zlib, BZ2, LZMA, ZFPY and Blosc.
- Pre-compression filters, e.g., Delta, Quantize, FixedScaleOffset, PackBits, Categorize.
- Integrity checks, e.g., CRC32, Adler32.

All codecs implement the  same API, allowing codecs to be  organized into pipelines in a variety  of ways.

If you have a question, find a bug, would like to make a suggestion or contribute code, please raise [an issue on GitHub.](https://github.com/alimanfoo/numcodecs/issues)

Installation![ref1]

Numcodecs depends on NumPy. It is generally best  to inst[all NumPy first ](https://numpy.org/install/)using whatever method is most appropriate for you operating system and Python distribution.

Install from PyPI:![ref4]

$ pip install numcodecs![](Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.007.png)

Alternatively, install via conda:![ref4]

$ conda install -c conda-forge numcodecs![ref5]

Numcodecs  includes  a  C extension  providing  integration  with the  [Blosc ](https://www.blosc.org/)library. Wheels  are  avail‐ able for most platforms.

Installing a wheel or via conda will install a pre-compiled binary distribution. However, if you have a newer  CPU that  supports the AVX2 instruction  set  (e.g.,  Intel Haswell,  Broadwell  or Skylake)  then installing  via pip is preferable, because  you can  compile  the  Blosc  library from source with optimi‐ sations for AVX2.:![ref4]

$ pip install -v --no-cache-dir --no-binary numcodecs numcodecs![ref5]

Note that if you compile the C extensions on a machine with AVX2 support you probably then can‐ not use the same binaries on a machine without AVX2.

If you  specifically want  to disable AVX2 or SSE2 when  compiling,  you  can  use  the  following envi‐ ronment variables:![ref5]

$ export DISABLE\_NUMCODECS\_AVX2=1 -                        × $ export DISABLE\_NUMCODECS\_SSE2=1![ref6]

To work with Numcodecs source code  in development, clone  the  repository from GitHub and  then install in editable mode using pip.:![ref5]

$ git clone --recursive https://github.com/zarr-developers/numcodecs.git $ cd numcodecs

$ pip install -e .[test,msgpack,zfpy]![ref4]

Note: if you prefer to use the GitHub CLI gh you will need to append -- --recurse-submodules to the clone command to everything works properly.

To verify that Numcodecs has been fully installed (including the Blosc extension) run the test suite:![ref6]

$ pytest -v![ref5]

Contents![ref1]

- [Codec API](https://numcodecs.readthedocs.io/en/stable/abc.html)
  - [Codec](https://numcodecs.readthedocs.io/en/stable/abc.html#numcodecs.abc.Codec)
- [Codec registry](https://numcodecs.readthedocs.io/en/stable/registry.html)
  - [get_codec()](https://numcodecs.readthedocs.io/en/stable/registry.html#numcodecs.registry.get_codec)
  - [register_codec()](https://numcodecs.readthedocs.io/en/stable/registry.html#numcodecs.registry.register_codec)
- [Blosc](https://numcodecs.readthedocs.io/en/stable/blosc.html)
  - [Blosc](https://numcodecs.readthedocs.io/en/stable/blosc.html#numcodecs.blosc.Blosc)
  - [Helper functions](https://numcodecs.readthedocs.io/en/stable/blosc.html#helper-functions)
- [LZ4](https://numcodecs.readthedocs.io/en/stable/lz4.html)
  - [LZ4](https://numcodecs.readthedocs.io/en/stable/lz4.html#numcodecs.lz4.LZ4)
  - [Helper functions](https://numcodecs.readthedocs.io/en/stable/lz4.html#helper-functions)
- [ZFPY](https://numcodecs.readthedocs.io/en/stable/zfpy.html)
  - [ZFPY](https://numcodecs.readthedocs.io/en/stable/zfpy.html#numcodecs.zfpy.ZFPY)
- [Zstd](https://numcodecs.readthedocs.io/en/stable/zstd.html)
  - [Zstd](https://numcodecs.readthedocs.io/en/stable/zstd.html#numcodecs.zstd.Zstd)
  - [Helper functions](https://numcodecs.readthedocs.io/en/stable/zstd.html#helper-functions)
- [Zlib](https://numcodecs.readthedocs.io/en/stable/zlib.html)
  - [Zlib](https://numcodecs.readthedocs.io/en/stable/zlib.html#numcodecs.zlib.Zlib)
- [GZip](https://numcodecs.readthedocs.io/en/stable/gzip.html)
  - [GZip](https://numcodecs.readthedocs.io/en/stable/gzip.html#numcodecs.gzip.GZip)
- [BZ2](https://numcodecs.readthedocs.io/en/stable/bz2.html)
  - [BZ2](https://numcodecs.readthedocs.io/en/stable/bz2.html#numcodecs.bz2.BZ2)
- [LZMA](https://numcodecs.readthedocs.io/en/stable/lzma.html)
  - [LZMA](https://numcodecs.readthedocs.io/en/stable/lzma.html#numcodecs.lzma.LZMA)
- [Delta](https://numcodecs.readthedocs.io/en/stable/delta.html)
  - [Delta](https://numcodecs.readthedocs.io/en/stable/delta.html#numcodecs.delta.Delta)
- [FixedScaleOffset](https://numcodecs.readthedocs.io/en/stable/fixedscaleoffset.html)
  - [FixedScaleOffset](https://numcodecs.readthedocs.io/en/stable/fixedscaleoffset.html#numcodecs.fixedscaleoffset.FixedScaleOffset) -                        ×
- [Quantize](https://numcodecs.readthedocs.io/en/stable/quantize.html)
  - [Quantize](https://numcodecs.readthedocs.io/en/stable/quantize.html#numcodecs.quantize.Quantize)
- [Bitround](https://numcodecs.readthedocs.io/en/stable/bitround.html)
  - [BitRound](https://numcodecs.readthedocs.io/en/stable/bitround.html#numcodecs.bitround.BitRound)
- [PackBits](https://numcodecs.readthedocs.io/en/stable/packbits.html)
  - [PackBits](https://numcodecs.readthedocs.io/en/stable/packbits.html#numcodecs.packbits.PackBits)
- [Categorize](https://numcodecs.readthedocs.io/en/stable/categorize.html)
  - [Categorize](https://numcodecs.readthedocs.io/en/stable/categorize.html#numcodecs.categorize.Categorize)
- [32-bit checksums](https://numcodecs.readthedocs.io/en/stable/checksum32.html)
  - [CRC32](https://numcodecs.readthedocs.io/en/stable/checksum32.html#crc32)
  - [Adler32](https://numcodecs.readthedocs.io/en/stable/checksum32.html#adler32)
  - [Fletcher32](https://numcodecs.readthedocs.io/en/stable/checksum32.html#fletcher32)
  - [JenkinsLookup3](https://numcodecs.readthedocs.io/en/stable/checksum32.html#jenkinslookup3)
- [AsType](https://numcodecs.readthedocs.io/en/stable/astype.html)
  - [AsType](https://numcodecs.readthedocs.io/en/stable/astype.html#numcodecs.astype.AsType)
- [JSON](https://numcodecs.readthedocs.io/en/stable/json.html)
  - [J SON](https://numcodecs.readthedocs.io/en/stable/json.html#numcodecs.json.JSON)
- [Pickle](https://numcodecs.readthedocs.io/en/stable/pickles.html)
  - [Pickle](https://numcodecs.readthedocs.io/en/stable/pickles.html#numcodecs.pickles.Pickle)
- [MsgPack](https://numcodecs.readthedocs.io/en/stable/msgpacks.html)
  - [MsgPack](https://numcodecs.readthedocs.io/en/stable/msgpacks.html#numcodecs.msgpacks.MsgPack)
- [Codecs for variable-length objects](https://numcodecs.readthedocs.io/en/stable/vlen.html)
  - [VLenUTF8](https://numcodecs.readthedocs.io/en/stable/vlen.html#vlenutf8)
  - [VLenBytes](https://numcodecs.readthedocs.io/en/stable/vlen.html#vlenbytes)
  - [VLenArray](https://numcodecs.readthedocs.io/en/stable/vlen.html#vlenarray)
- [Shuffle](https://numcodecs.readthedocs.io/en/stable/shuffle.html)
  - [Shuffle](https://numcodecs.readthedocs.io/en/stable/shuffle.html#numcodecs.shuffle.Shuffle)
- [Release notes](https://numcodecs.readthedocs.io/en/stable/release.html)
  - [0.12.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-12-1)
  - [0.12.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-12-0)
  - [0.11.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-11-0)
  - [0.10.2](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-10-2)
  - [0.10.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-10-1)
  - [0.10.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-10-0)
  - [0.9.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-9-1)
  - [0.9.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-9-0)
  - [0.8.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-8-1)
  - [0.8.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-8-0)
  - [0.7.3](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-7-3)
  - [0.7.2](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-7-2)
  - [0.7.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-7-1)
  - [0.7.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-7-0)
  - [0.6.4](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-6-4)
  - [0.6.3](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-6-3)
  - [0.6.2](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-6-2)
  - [0.6.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-6-1) -                        ×
  - [0.6.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-6-0)
  - [0.5.5](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-5-5)
  - [0.5.4](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-5-4)
  - [0.5.3](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-5-3)
  - [0.5.2](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-5-2)
  - [0.5.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-5-1)
  - [0.5.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-5-0)
  - [0.4.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-4-1)
  - [0.4.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-4-0)
  - [0.3.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-3-1)
  - [0.3.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-3-0)
  - [0.2.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-2-1)
  - [0.2.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-2-0)
  - [0.1.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-1-1)
  - [0.1.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-1-0)
  - [0.0.1](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-0-1)
  - [0.0.0](https://numcodecs.readthedocs.io/en/stable/release.html#release-0-0-0)
- [Contributing to NumCodecs](https://numcodecs.readthedocs.io/en/stable/contributing.html)
  - [Asking for help](https://numcodecs.readthedocs.io/en/stable/contributing.html#asking-for-help)
  - [Bug reports](https://numcodecs.readthedocs.io/en/stable/contributing.html#bug-reports)
  - [Enhancement proposals](https://numcodecs.readthedocs.io/en/stable/contributing.html#enhancement-proposals)
  - [Contributing code and/or documentation](https://numcodecs.readthedocs.io/en/stable/contributing.html#contributing-code-and-or-documentation)
  - [Development best practices, policies and procedures](https://numcodecs.readthedocs.io/en/stable/contributing.html#development-best-practices-policies-and-procedures)

Acknowledgments![](Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.010.png)

The  following people  have  contributed  to  the  development  of NumCodecs  by  contributing  code, documentation, code reviews, comments and/or ideas:

- [Francesc Alted](https://github.com/FrancescAlted)
- [Prakhar Goel](https://github.com/newt0311)
- [Jerome Kelleher](https://github.com/jeromekelleher)
- [John Kirkham](https://github.com/jakirkham)
- [Alistair Miles](https://github.com/alimanfoo)
- [Jeff Reback](https://github.com/jreback)
- [Trevor Manz](https://github.com/manzt)
- [Grzegorz Bokota](https://github.com/Czaki)
- [Josh Moore](https://github.com/joshmoore)
- [Martin Durant](https://github.com/martindurant)
- [Paul Branson](https://github.com/pbranson)

Numcodecs bundles the c-b[losc libra](https://github.com/Blosc/c-blosc)ry.

Development of this package is supported by the MRC[ Centre for Genomics and Global Health.](https://www.sanger.ac.uk/collaboration/mrc-centre-genomics-and-global-health-cggh/)

Indices and tables -                        ×![ref7]

- [Index](https://numcodecs.readthedocs.io/en/stable/genindex.html)

- [Module Index](https://numcodecs.readthedocs.io/en/stable/py-modindex.html)
- [Search Page](https://numcodecs.readthedocs.io/en/stable/search.html)
- ×

ZFPY![ref1]

class numcodecs.zfpy.ZFPY(mode=4, tolerance=-1, rate=-1, precision=-1, compression\_kwargs=None) [sourc[e\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/zfpy.html#ZFPY)

Codec providing compression using zfpy via the Python standard library.

Parameters: mode : integer

One of the zfpy mode choice, e.g., zfpy.mode\_fixed\_accuracy.

tolerance : double, optional

A double-precision number, specifying the compression accuracy needed.

rate : double, optional

A double-precision number, specifying the compression rate needed.

precision : int, optional

A integer number, specifying the compression precision needed.

codec\_id = 'zfpy'

Codec identifier.

encode(buf) [sou[rce\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/zfpy.html#ZFPY.encode)

Encode data in buf.

Parameters: buf : buffer-like

Data  to be  encoded. May be  any  object  supporting the  new-style buf‐ fer protocol.

Returns: enc : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

decode(buf, out=None) [source[\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/zfpy.html#ZFPY.decode)

Decode data in buf.

Parameters: buf : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

out : buffer-like, optional

Writeable  buffer  to  store  decoded  data.  N.B.  if provided,  this  buffer must be exactly the right size to store the decoded data.

Returns: dec : buffer-like

Decoded  data.  May  be  any  object  supporting  the  new--st      yl    e       b    u  ff  e×r protocol.

get\_config()


Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encoding.

classmethod from\_config(config)

Instantiate codec from a configuration object.

- ×

Zlib![ref1]

class numcodecs.zlib.Zlib(level=1) [source]

Codec providing compression using zlib via the Python standard library.

Parameters: level : int

Compression level.

codec\_id = 'zlib'

Codec identifier.

encode(buf) [sou[rce\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/zlib.html#Zlib.encode)

Encode data in buf.

Parameters: buf : buffer-like

Data  to be  encoded. May be  any  object  supporting the  new-style buf‐ fer protocol.

Returns: enc : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

decode(buf, out=None) [source[\]](https://numcodecs.readthedocs.io/en/stable/_modules/numcodecs/zlib.html#Zlib.decode)

Decode data in buf.

Parameters: buf : buffer-like

Encoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

out : buffer-like, optional

Writeable  buffer  to  store  decoded  data.  N.B.  if provided,  this  buffer must be exactly the right size to store the decoded data.

Returns: dec : buffer-like

Decoded  data.  May  be  any  object  supporting  the  new-style  buffer protocol.

get\_config()

Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encoding.

classmethod from\_config(config)

Instantiate codec from a configuration object.

- ×

Zstd![ref1]

class numcodecs.zstd.Zstd(level=1)

Codec providing compression using Zstandard.

Parameters: level : int

Compression level (1-22). See also:![](Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.012.png)

[numcodecs.lz4.LZ4, nu](https://numcodecs.readthedocs.io/en/stable/lz4.html#numcodecs.lz4.LZ4)[mcodecs.blosc.Blosc](https://numcodecs.readthedocs.io/en/stable/blosc.html#numcodecs.blosc.Blosc)

codec\_id = 'zstd'

Codec identifier.

encode(self, buf) decode(self, buf, out=None) get\_config()

Return  a  dictionary holding  configuration  parameters  for this  codec.  Must  include  an  ‘id’ field with the codec identifier. All values must be compatible with JSON encoding.

classmethod from\_config(config)

Instantiate codec from a configuration object.

Helper functions![ref7]

numcodecs.zstd.compress(source, int level=DEFAULT\_CLEVEL)

Compress data.

Parameters: source : bytes-like

Data to be compressed. Can be any object supporting the buffer protocol.

level : int

Compression level (1-22).

Returns: dest : bytes

Compressed data.

numcodecs.zstd.decompress(source, dest=None)

Decompress data.

- ×

Parameters: source : bytes-like

Compressed data. Can be any object supporting the buffer protocol.


dest : array-like, optional

Object to decompress into.

Returns: dest : bytes

Object containing decompressed data.

- ×

[ref1]: Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.001.png
[ref2]: Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.003.png
[ref3]: Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.004.png
[ref4]: Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.006.png
[ref5]: Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.008.png
[ref6]: Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.009.png
[ref7]: Aspose.Words.25aa547b-789b-4ec6-806c-21e65af73ac1.011.png
