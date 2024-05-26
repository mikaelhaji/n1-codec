**zstd 1.5.1 Manual![ref1]**

**Contents**

1. [Introduction](#_page0_x32.00_y316.00)
1. [Version](#_page0_x32.00_y570.00)
1. [Simple API](#_page0_x32.00_y677.50)
1. [Explicit context](#_page1_x32.00_y600.00)
1. [Advanced compression API (Requires v1.4.0+)](#_page2_x32.00_y340.50)
1. [Advanced decompression API (Requires v1.4.0+)](#_page5_x32.00_y310.50)
1. [Streaming](#_page6_x32.00_y58.50)
1. [Streaming compression - HowTo](#_page6_x32.00_y204.50)
1. [Streaming decompression - HowTo](#_page7_x32.00_y584.50)
1. [Simple dictionary API](#_page8_x32.00_y252.50)
1. [Bulk processing dictionary API](#_page8_x32.00_y487.00)
1. [Dictionary helper functions](#_page9_x32.00_y234.00)
1. [Advanced dictionary and prefix API (Requires v1.4.0+)](#_page9_x32.00_y540.00)
1. [experimental API (static linking only)](#_page11_x32.00_y125.50)
1. [Frame size functions](#_page12_x32.00_y753.50)
1. [Memory management](#_page14_x32.00_y526.50)
1. [Advanced compression functions](#_page15_x32.00_y741.50)
1. [Advanced decompression functions](#_page17_x32.00_y699.50)
1. [Advanced streaming functions](#_page18_x32.00_y631.50)
1. [Buffer-less and synchronous inner streaming functions](#_page20_x32.00_y675.50)
1. [Buffer-less streaming compression (synchronous mode)](#_page20_x32.00_y753.50)
1. [Buffer-less streaming decompression (synchronous mode)](#_page21_x32.00_y351.50)
1. [Block level API](#_page22_x32.00_y423.50)![ref1]

<a name="_page0_x32.00_y316.00"></a>**Introduction**

`  `zstd, short for Zstandard, is a fast lossless compression algorithm, targeting   real-time compression scenarios at zlib-level and better compression ratios.

`  `The zstd compression library provides in-memory compression and decompression   functions.

`  `The library supports regular compression levels from 1 up to ZSTD\_maxCLevel(),   which is currently 22. Levels >= 20, labeled `--ultra`, should be used with

`  `caution, as they require more memory. The library also offers negative

`  `compression levels, which extend the range of speed vs. ratio preferences.

`  `The lower the level, the faster the speed (at the cost of compression).

`  `Compression can be done in:

- a single step (described as Simple API)
- a single step, reusing a context (described as Explicit context)
- unbounded multiple steps (described as Streaming compression)

`  `The compression ratio achievable on small data can be highly improved using   a dictionary. Dictionary compression can be performed in:

- a single step (described as Simple dictionary API)
- a single step, reusing a dictionary (described as Bulk-processing

`      `dictionary API)

`  `Advanced experimental functions can be accessed using

`  ``#define ZSTD\_STATIC\_LINKING\_ONLY` before including zstd.h.

`  `Advanced experimental APIs should never be used with a dynamically-linked

`  `library. They are not "stable"; their definitions or signatures may change in   the future. Only static linking is allowed.

<a name="_page0_x32.00_y570.00"></a>**Version**

**unsigned ZSTD\_versionNumber(void);**

`  `Return runtime library version, the value is (MAJOR\*100\*100 + MINOR\*100 + RELEASE). 

**const char\* ZSTD\_versionString(void);**

`  `Return runtime library version, like "1.4.5". Requires v1.3.0+. 

<a name="_page0_x32.00_y677.50"></a>**Simple API**

**size\_t ZSTD\_compress( void\* dst, size\_t dstCapacity,                 const void\* src, size\_t srcSize,**

`                      `**int compressionLevel);**

`  `Compresses `src` content as a single zstd compressed frame into already allocated `dst`.   Hint : compression runs faster if `dstCapacity` >=  `ZSTD\_compressBound(srcSize)`.

`  `@return : compressed size written into `dst` (<= `dstCapacity),

`            `or an error code if it fails (which can be tested using ZSTD\_isError()). 

**size\_t ZSTD\_decompress( void\* dst, size\_t dstCapacity,**

`                  `**const void\* src, size\_t compressedSize);**

`  ``compressedSize` : must be the \_exact\_ size of some number of compressed and/or skippable frames.   `dstCapacity` is an upper bound of originalSize to regenerate.

`  `If user cannot imply a maximum upper bound, it's better to use streaming mode to decompress data.   @return : the number of bytes decompressed into `dst` (<= `dstCapacity`),

`            `or an errorCode if it fails (which can be tested using ZSTD\_isError()). 

**#define ZSTD\_CONTENTSIZE\_UNKNOWN (0ULL - 1)**

**#define ZSTD\_CONTENTSIZE\_ERROR   (0ULL - 2)**

**unsigned long long ZSTD\_getFrameContentSize(const void \*src, size\_t srcSize);**

`  ``src` should point to the start of a ZSTD encoded frame.

`  ``srcSize` must be at least as large as the frame header.

`            `hint : any size >= `ZSTD\_frameHeaderSize\_max` is large enough.

`  `@return : - decompressed size of `src` frame content, if known

- ZSTD\_CONTENTSIZE\_UNKNOWN if the size cannot be determined
- ZSTD\_CONTENTSIZE\_ERROR if an error occurred (e.g. invalid magic number, srcSize too small)

`   `note 1 : a 0 return value means the frame is valid but "empty".

`   `note 2 : decompressed size is an optional field, it may not be present, typically in streaming mode.

`            `When `return==ZSTD\_CONTENTSIZE\_UNKNOWN`, data to decompress could be any size.

`            `In which case, it's necessary to use streaming mode to decompress data.

`            `Optionally, application can rely on some implicit limit,

`            `as ZSTD\_decompress() only needs an upper bound of decompressed size.

`            `(For example, data could be necessarily cut into blocks <= 16 KB).

`   `note 3 : decompressed size is always present when compression is completed using single-pass functions,

`            `such as ZSTD\_compress(), ZSTD\_compressCCtx() ZSTD\_compress\_usingDict() or ZSTD\_compress\_usingCDict().    note 4 : decompressed size can be very large (64-bits value),

`            `potentially larger than what local system can handle as a single memory segment.

`            `In which case, it's necessary to use streaming mode to decompress data.

`   `note 5 : If source is untrusted, decompressed size could be wrong or intentionally modified.

`            `Always ensure return value fits within application's authorized limits.

`            `Each application can set its own limits.

`   `note 6 : This function replaces ZSTD\_getDecompressedSize() 

**unsigned long long ZSTD\_getDecompressedSize(const void\* src, size\_t srcSize);**

`  `NOTE: This function is now obsolete, in favor of ZSTD\_getFrameContentSize().

`  `Both functions work the same way, but ZSTD\_getDecompressedSize() blends

`  `"empty", "unknown" and "error" results to the same return value (0),

`  `while ZSTD\_getFrameContentSize() gives them separate return values.

` `@return : decompressed size of `src` frame content \_if known and not empty\_, 0 otherwise. 

**size\_t ZSTD\_findFrameCompressedSize(const void\* src, size\_t srcSize);**

` ``src` should point to the start of a ZSTD frame or skippable frame.

` ``srcSize` must be >= first frame size

` `@return : the compressed size of the first frame starting at `src`,

`           `suitable to pass as `srcSize` to `ZSTD\_decompress` or similar,         or an error code if input is invalid 

**Helper functions**

**#define ZSTD\_COMPRESSBOUND(srcSize)   ((srcSize) + ((srcSize)>>8) + (((srcSize) < (128<<10)) ? (((128<<10) - (srcSize)) >> 11)** /\* margin, fro **size\_t      ZSTD\_compressBound(size\_t srcSize);** /\*!< maximum compressed size in worst case single-pass scenario \*/ **unsigned    ZSTD\_isError(size\_t code);**          /\*!< tells if a `size\_t` function result is an error code \*/ **const char\* ZSTD\_getErrorName(size\_t code);**     /\*!< provides readable string from an error code \*/ **int         ZSTD\_minCLevel(void);**               /\*!< minimum negative compression level allowed, requires v1.4.0+ \*/ **int         ZSTD\_maxCLevel(void);**               /\*!< maximum compression level available \*/

**int         ZSTD\_defaultCLevel(void);**           /\*!< default compression level, specified by ZSTD\_CLEVEL\_DEFAULT, requires v1.5.0+ \*/

<a name="_page1_x32.00_y600.00"></a>**Explicit context**

**Compression context**

`  `When compressing many times,

`  `it is recommended to allocate a context just once,

`  `and re-use it for each successive compression operation.

`  `This will make workload friendlier for system's memory.

`  `Note : re-using context is just a speed / resource optimization.

`         `It doesn't change the compression ratio, which remains identical.   Note 2 : In multi-threaded environments,

`         `use one different context per thread for parallel execution.

**typedef struct ZSTD\_CCtx\_s ZSTD\_CCtx;**

**ZSTD\_CCtx\* ZSTD\_createCCtx(void); size\_t     ZSTD\_freeCCtx(ZSTD\_CCtx\* cctx);**  /\* accept NULL pointer \*/

**size\_t ZSTD\_compressCCtx(ZSTD\_CCtx\* cctx,**

`                         `**void\* dst, size\_t dstCapacity,                    const void\* src, size\_t srcSize,**

`                         `**int compressionLevel);**

`  `Same as ZSTD\_compress(), using an explicit ZSTD\_CCtx.

`  `Important : in order to behave similarly to `ZSTD\_compress()`,   this function compresses at requested compression level,

`  `\_\_ignoring any other parameter\_\_ .

`  `If any advanced parameter was set using the advanced API,

`  `they will all be reset. Only `compressionLevel` remains.

**Decompression context**

`  `When decompressing many times,

`  `it is recommended to allocate a context only once,

`  `and re-use it for each successive compression operation.   This will make workload friendlier for system's memory.   Use one context per thread for parallel execution. 

**typedef struct ZSTD\_DCtx\_s ZSTD\_DCtx;**

**ZSTD\_DCtx\* ZSTD\_createDCtx(void); size\_t     ZSTD\_freeDCtx(ZSTD\_DCtx\* dctx);**  /\* accept NULL pointer \*/

**size\_t ZSTD\_decompressDCtx(ZSTD\_DCtx\* dctx,**

`                           `**void\* dst, size\_t dstCapacity,                      const void\* src, size\_t srcSize);**

`  `Same as ZSTD\_decompress(),

`  `requires an allocated ZSTD\_DCtx.

`  `Compatible with sticky parameters.

<a name="_page2_x32.00_y340.50"></a>**Advanced compression API (Requires v1.4.0+)**

**typedef enum { ZSTD\_fast=1,**

`               `**ZSTD\_dfast=2,**

`               `**ZSTD\_greedy=3,**

`               `**ZSTD\_lazy=4,**

`               `**ZSTD\_lazy2=5,**

`               `**ZSTD\_btlazy2=6,**

`               `**ZSTD\_btopt=7,**

`               `**ZSTD\_btultra=8,**

`               `**ZSTD\_btultra2=9**

/\* note : new strategies \_might\_ be added in the future.

`                         `**Only the order (from fast to strong) is guaranteed \*/ } ZSTD\_strategy;**

**typedef enum {**

/\* compression parameters

* **Note: When compressing with a ZSTD\_CDict these parameters are superseded**
* **by the parameters used to construct the ZSTD\_CDict.**
* **See ZSTD\_CCtx\_refCDict() for more info (superseded-by-cdict). \*/**

`    `**ZSTD\_c\_compressionLevel=100,** /\* Set compression parameters according to pre-defined cLevel table.

* **Note that exact compression parameters are dynamically determined,**
* **depending on both compression level and srcSize (when known).**
* **Default level is ZSTD\_CLEVEL\_DEFAULT==3.**
* **Special: value 0 means default, which is controlled by ZSTD\_CLEVEL\_DEFAULT.**
* **Note 1 : it's possible to pass a negative compression level.**
* **Note 2 : setting a level does not automatically set all other compression parameters**
* **to default. Setting this will however eventually dynamically impact the compression**
* **parameters which have not been manually set. The manually set**
* **ones will 'stick'. \*/**

/\* Advanced compression parameters :

* **It's possible to pin down compression parameters to some specific values.**
* **In which case, these values are no longer dynamically selected by the compressor \*/**

`    `**ZSTD\_c\_windowLog=101,**    /\* Maximum allowed back-reference distance, expressed as power of 2.

* **This will set a memory budget for streaming decompression,**
* **with larger values requiring more memory**
* **and typically compressing more.**
* **Must be clamped between ZSTD\_WINDOWLOG\_MIN and ZSTD\_WINDOWLOG\_MAX.**
* **Special: value 0 means "use default windowLog".**
* **Note: Using a windowLog greater than ZSTD\_WINDOWLOG\_LIMIT\_DEFAULT**
* **requires explicitly allowing such size at streaming decompression stage. \*/**

`    `**ZSTD\_c\_hashLog=102,**      /\* Size of the initial probe table, as a power of 2.

* **Resulting memory usage is (1 << (hashLog+2)).**
* **Must be clamped between ZSTD\_HASHLOG\_MIN and ZSTD\_HASHLOG\_MAX.**
* **Larger tables improve compression ratio of strategies <= dFast,**
* **and improve speed of strategies > dFast.**
* **Special: value 0 means "use default hashLog". \*/**

`    `**ZSTD\_c\_chainLog=103,**     /\* Size of the multi-probe search table, as a power of 2.

* **Resulting memory usage is (1 << (chainLog+2)).**
* **Must be clamped between ZSTD\_CHAINLOG\_MIN and ZSTD\_CHAINLOG\_MAX.**
* **Larger tables result in better and slower compression.**
* **This parameter is useless for "fast" strategy.**
* **It's still useful when using "dfast" strategy,**
* **in which case it defines a secondary probe table.**
* **Special: value 0 means "use default chainLog". \*/**

`    `**ZSTD\_c\_searchLog=104,**    /\* Number of search attempts, as a power of 2.

* **More attempts result in better and slower compression.**
* **This parameter is useless for "fast" and "dFast" strategies.**
* **Special: value 0 means "use default searchLog". \*/**

`    `**ZSTD\_c\_minMatch=105,**     /\* Minimum size of searched matches.

* **Note that Zstandard can still find matches of smaller size,**
* **it just tweaks its search algorithm to look for this size and larger.**
* **Larger values increase compression and decompression speed, but decrease ratio.**
* **Must be clamped between ZSTD\_MINMATCH\_MIN and ZSTD\_MINMATCH\_MAX.**
* **Note that currently, for all strategies < btopt, effective minimum is 4.**
* **, for all strategies > fast, effective maximum is 6.**
* **Special: value 0 means "use default minMatchLength". \*/**

`    `**ZSTD\_c\_targetLength=106,** /\* Impact of this field depends on strategy.

* **For strategies btopt, btultra & btultra2:**
* **Length of Match considered "good enough" to stop search.**
* **Larger values make compression stronger, and slower.**
* **For strategy fast:**
* **Distance between match sampling.**
* **Larger values make compression faster, and weaker.**
* **Special: value 0 means "use default targetLength". \*/**

`    `**ZSTD\_c\_strategy=107,**     /\* See ZSTD\_strategy enum definition.

* **The higher the value of selected strategy, the more complex it is,**
* **resulting in stronger and slower compression.**
* **Special: value 0 means "use default strategy". \*/**

/\* LDM mode parameters \*/

`    `**ZSTD\_c\_enableLongDistanceMatching=160,** /\* Enable long distance matching.

* **This parameter is designed to improve compression ratio**
* **for large inputs, by finding large matches at long distance.**
* **It increases memory usage and window size.**
* **Note: enabling this parameter increases default ZSTD\_c\_windowLog to 128 MB**
* **except when expressly set to a different value.**
* **Note: will be enabled by default if ZSTD\_c\_windowLog >= 128 MB and**
* **compression strategy >= ZSTD\_btopt (== compression level 16+) \*/**

`    `**ZSTD\_c\_ldmHashLog=161,**   /\* Size of the table for long distance matching, as a power of 2.

* **Larger values increase memory usage and compression ratio,**
* **but decrease compression speed.**
* **Must be clamped between ZSTD\_HASHLOG\_MIN and ZSTD\_HASHLOG\_MAX**
* **default: windowlog - 7.**
* **Special: value 0 means "automatically determine hashlog". \*/**

`    `**ZSTD\_c\_ldmMinMatch=162,**  /\* Minimum match size for long distance matcher.

* **Larger/too small values usually decrease compression ratio.**
* **Must be clamped between ZSTD\_LDM\_MINMATCH\_MIN and ZSTD\_LDM\_MINMATCH\_MAX.**
* **Special: value 0 means "use default value" (default: 64). \*/**

`    `**ZSTD\_c\_ldmBucketSizeLog=163,** /\* Log size of each bucket in the LDM hash table for collision resolution.

* **Larger values improve collision resolution but decrease compression speed.**
* **The maximum value is ZSTD\_LDM\_BUCKETSIZELOG\_MAX.**
* **Special: value 0 means "use default value" (default: 3). \*/**

`    `**ZSTD\_c\_ldmHashRateLog=164,** /\* Frequency of inserting/looking up entries into the LDM hash table.

* **Must be clamped between 0 and (ZSTD\_WINDOWLOG\_MAX - ZSTD\_HASHLOG\_MIN).**
* **Default is MAX(0, (windowLog - ldmHashLog)), optimizing hash table usage.**
* **Larger values improve compression speed.**
* **Deviating far from default value will likely result in a compression ratio decrease.**
* **Special: value 0 means "automatically determine hashRateLog". \*/**

/\* frame parameters \*/

`    `**ZSTD\_c\_contentSizeFlag=200,** /\* Content size will be written into frame header \_whenever known\_ (default:1)

* **Content size must be known at the beginning of compression.**
* **This is automatically the case when using ZSTD\_compress2(),**
* **For streaming scenarios, content size must be provided with ZSTD\_CCtx\_setPledgedSrcSize() \*/**

`    `**ZSTD\_c\_checksumFlag=201,** /\* A 32-bits checksum of content is written at end of frame (default:0) \*/     **ZSTD\_c\_dictIDFlag=202,**   /\* When applicable, dictionary's ID is written into frame header (default:1) \*/

/\* multi-threading parameters \*/

/\* These parameters are only active if multi-threading is enabled (compiled with build macro ZSTD\_MULTITHREAD).

* **Otherwise, trying to set any other value than default (0) will be a no-op and return an error.**
* **In a situation where it's unknown if the linked library supports multi-threading or not,**
* **setting ZSTD\_c\_nbWorkers to any value >= 1 and consulting the return value provides a quick way to check this property.**

`     `**\*/**

`    `**ZSTD\_c\_nbWorkers=400,**    /\* Select how many threads will be spawned to compress in parallel.

* **When nbWorkers >= 1, triggers asynchronous mode when invoking ZSTD\_compressStream\*() :**
* **ZSTD\_compressStream\*() consumes input and flush output if possible, but immediately gives back control to cal**
* **while compression is performed in parallel, within worker thread(s).**
* **(note : a strong exception to this rule is when first invocation of ZSTD\_compressStream2() sets ZSTD\_e\_end :**
* **in which case, ZSTD\_compressStream2() delegates to ZSTD\_compress2(), which is always a blocking call).**
* **More workers improve speed, but also increase memory usage.**
* **Default value is `0`, aka "single-threaded mode" : no worker is spawned,**
* **compression is performed inside Caller's thread, and all invocations are blocking \*/**

`    `**ZSTD\_c\_jobSize=401,**      /\* Size of a compression job. This value is enforced only when nbWorkers >= 1.

* **Each compression job is completed in parallel, so this value can indirectly impact the nb of active threads.**
* **0 means default, which is dynamically determined based on compression parameters.**
* **Job size must be a minimum of overlap size, or ZSTDMT\_JOBSIZE\_MIN (= 512 KB), whichever is largest.**
* **The minimum size is automatically and transparently enforced. \*/**

`    `**ZSTD\_c\_overlapLog=402,**   /\* Control the overlap size, as a fraction of window size.

* **The overlap size is an amount of data reloaded from previous job at the beginning of a new job.**
* **It helps preserve compression ratio, while each job is compressed in parallel.**
* **This value is enforced only when nbWorkers >= 1.**
* **Larger values increase compression ratio, but decrease speed.**
* **Possible values range from 0 to 9 :**
* **- 0 means "default" : value will be determined by the library, depending on strategy**
* **- 1 means "no overlap"**
* **- 9 means "full overlap", using a full window size.**
* **Each intermediate rank increases/decreases load size by a factor 2 :**
* **9: full window;  8: w/2;  7: w/4;  6: w/8;  5:w/16;  4: w/32;  3:w/64;  2:w/128;  1:no overlap;  0:default**
* **default value varies between 6 and 9, depending on strategy \*/**

/\* note : additional experimental parameters are also available

* **within the experimental section of the API.**
* **At the time of this writing, they include :**
* **ZSTD\_c\_rsyncable**
* **ZSTD\_c\_format**
* **ZSTD\_c\_forceMaxWindow**
* **ZSTD\_c\_forceAttachDict**
* **ZSTD\_c\_literalCompressionMode**
* **ZSTD\_c\_targetCBlockSize**
* **ZSTD\_c\_srcSizeHint**
* **ZSTD\_c\_enableDedicatedDictSearch**
* **ZSTD\_c\_stableInBuffer**
* **ZSTD\_c\_stableOutBuffer**
* **ZSTD\_c\_blockDelimiters**
* **ZSTD\_c\_validateSequences**
* **ZSTD\_c\_useBlockSplitter**
* **ZSTD\_c\_useRowMatchFinder**
* **Because they are not stable, it's necessary to define ZSTD\_STATIC\_LINKING\_ONLY to access them.**
* **note : never ever use experimentalParam? names directly;**
* **also, the enums values themselves are unstable and can still change.**

`     `**\*/**

`     `**ZSTD\_c\_experimentalParam1=500,**

`     `**ZSTD\_c\_experimentalParam2=10,**

`     `**ZSTD\_c\_experimentalParam3=1000,**

`     `**ZSTD\_c\_experimentalParam4=1001,**

`     `**ZSTD\_c\_experimentalParam5=1002,**

`     `**ZSTD\_c\_experimentalParam6=1003,**

`     `**ZSTD\_c\_experimentalParam7=1004,**

`     `**ZSTD\_c\_experimentalParam8=1005,**

`     `**ZSTD\_c\_experimentalParam9=1006,**

`     `**ZSTD\_c\_experimentalParam10=1007,**

`     `**ZSTD\_c\_experimentalParam11=1008,**

`     `**ZSTD\_c\_experimentalParam12=1009,**

`     `**ZSTD\_c\_experimentalParam13=1010,**

`     `**ZSTD\_c\_experimentalParam14=1011,**

`     `**ZSTD\_c\_experimentalParam15=1012**

**} ZSTD\_cParameter;**

**typedef struct {**

`    `**size\_t error;**

`    `**int lowerBound;     int upperBound; } ZSTD\_bounds;**

**ZSTD\_bounds ZSTD\_cParam\_getBounds(ZSTD\_cParameter cParam);**

`  `All parameters must belong to an interval with lower and upper bounds,

`  `otherwise they will either trigger an error or be automatically clamped.  @return : a structure, ZSTD\_bounds, which contains

- an error status field, which must be tested using ZSTD\_isError()
- lower and upper bounds, both inclusive

**size\_t ZSTD\_CCtx\_setParameter(ZSTD\_CCtx\* cctx, ZSTD\_cParameter param, int value);**

`  `Set one compression parameter, selected by enum ZSTD\_cParameter.

`  `All parameters have valid bounds. Bounds can be queried using ZSTD\_cParam\_getBounds().

`  `Providing a value beyond bound will either clamp it, or trigger an error (depending on parameter).

`  `Setting a parameter is generally only possible during frame initialization (before starting compression).   Exception : when using multi-threading mode (nbWorkers >= 1),

`              `the following parameters can be updated \_during\_ compression (within same frame):

`              `=> compressionLevel, hashLog, chainLog, searchLog, minMatch, targetLength and strategy.

`              `new parameters will be active for next job only (after a flush()).

` `@return : an error code (which can be tested using ZSTD\_isError()).

**size\_t ZSTD\_CCtx\_setPledgedSrcSize(ZSTD\_CCtx\* cctx, unsigned long long pledgedSrcSize);**

`  `Total input data size to be compressed as a single frame.

`  `Value will be written in frame header, unless if explicitly forbidden using ZSTD\_c\_contentSizeFlag.   This value will also be controlled at end of frame, and trigger an error if not respected.

` `@result : 0, or an error code (which can be tested with ZSTD\_isError()).

`  `Note 1 : pledgedSrcSize==0 actually means zero, aka an empty frame.

`           `In order to mean "unknown content size", pass constant ZSTD\_CONTENTSIZE\_UNKNOWN.

`           `ZSTD\_CONTENTSIZE\_UNKNOWN is default value for any new frame.

`  `Note 2 : pledgedSrcSize is only valid once, for the next frame.

`           `It's discarded at the end of the frame, and replaced by ZSTD\_CONTENTSIZE\_UNKNOWN.

`  `Note 3 : Whenever all input data is provided and consumed in a single round,

`           `for example with ZSTD\_compress2(),

`           `or invoking immediately ZSTD\_compressStream2(,,,ZSTD\_e\_end),

`           `this value is automatically overridden by srcSize instead.

**typedef enum {**

`    `**ZSTD\_reset\_session\_only = 1,     ZSTD\_reset\_parameters = 2,**

`    `**ZSTD\_reset\_session\_and\_parameters = 3 } ZSTD\_ResetDirective;**

**size\_t ZSTD\_CCtx\_reset(ZSTD\_CCtx\* cctx, ZSTD\_ResetDirective reset);**

`  `There are 2 different things that can be reset, independently or jointly :

- The session : will stop compressing current frame, and make CCtx ready to start a new one.

`                  `Useful after an error, or to interrupt any ongoing compression.

`                  `Any internal data not yet flushed is cancelled.

`                  `Compression parameters and dictionary remain unchanged.

`                  `They will be used to compress next frame.

`                  `Resetting session never fails.

- The parameters : changes all parameters back to "default".

`                  `This removes any reference to any dictionary too.

`                  `Parameters can only be changed between 2 sessions (i.e. no compression is currently ongoing)

`                  `otherwise the reset fails, and function returns an error value (which can be tested using ZSTD\_isError())

- Both : similar to resetting the session, followed by resetting parameters.

**size\_t ZSTD\_compress2( ZSTD\_CCtx\* cctx,**

`                       `**void\* dst, size\_t dstCapacity,                  const void\* src, size\_t srcSize);**

`  `Behave the same as ZSTD\_compressCCtx(), but compression parameters are set using the advanced API.   ZSTD\_compress2() always starts a new frame.

`  `Should cctx hold data from a previously unfinished frame, everything about it is forgotten.

- Compression parameters are pushed into CCtx before starting compression, using ZSTD\_CCtx\_set\*()
- The function is always blocking, returns when compression is completed.

`  `Hint : compression runs faster if `dstCapacity` >=  `ZSTD\_compressBound(srcSize)`.

` `@return : compressed size written into `dst` (<= `dstCapacity),

`           `or an error code if it fails (which can be tested using ZSTD\_isError()).

<a name="_page5_x32.00_y310.50"></a>**Advanced decompression API (Requires v1.4.0+)**

**typedef enum {**

`    `**ZSTD\_d\_windowLogMax=100,** /\* Select a size limit (in power of 2) beyond which

* **the streaming API will refuse to allocate memory buffer**
* **in order to protect the host from unreasonable memory requirements.**
* **This parameter is only useful in streaming mode, since no internal buffer is allocated in single-pass mode.**
* **By default, a decompression context accepts window sizes <= (1 << ZSTD\_WINDOWLOG\_LIMIT\_DEFAULT).**
* **Special: value 0 means "use default maximum windowLog". \*/**

/\* note : additional experimental parameters are also available

* **within the experimental section of the API.**
* **At the time of this writing, they include :**
* **ZSTD\_d\_format**
* **ZSTD\_d\_stableOutBuffer**
* **ZSTD\_d\_forceIgnoreChecksum**
* **ZSTD\_d\_refMultipleDDicts**
* **Because they are not stable, it's necessary to define ZSTD\_STATIC\_LINKING\_ONLY to access them.**
* **note : never ever use experimentalParam? names directly**

`     `**\*/**

`     `**ZSTD\_d\_experimentalParam1=1000,**

`     `**ZSTD\_d\_experimentalParam2=1001,**

`     `**ZSTD\_d\_experimentalParam3=1002,**

`     `**ZSTD\_d\_experimentalParam4=1003**

**} ZSTD\_dParameter;**

**ZSTD\_bounds ZSTD\_dParam\_getBounds(ZSTD\_dParameter dParam);**

`  `All parameters must belong to an interval with lower and upper bounds,

`  `otherwise they will either trigger an error or be automatically clamped.  @return : a structure, ZSTD\_bounds, which contains

- an error status field, which must be tested using ZSTD\_isError()
- both lower and upper bounds, inclusive

**size\_t ZSTD\_DCtx\_setParameter(ZSTD\_DCtx\* dctx, ZSTD\_dParameter param, int value);**

`  `Set one compression parameter, selected by enum ZSTD\_dParameter.

`  `All parameters have valid bounds. Bounds can be queried using ZSTD\_dParam\_getBounds().

`  `Providing a value beyond bound will either clamp it, or trigger an error (depending on parameter).   Setting a parameter is only possible during frame initialization (before starting decompression).  @return : 0, or an error code (which can be tested using ZSTD\_isError()).

**size\_t ZSTD\_DCtx\_reset(ZSTD\_DCtx\* dctx, ZSTD\_ResetDirective reset);**

`  `Return a DCtx to clean state.

`  `Session and parameters can be reset jointly or separately.

`  `Parameters can only be reset when no active frame is being decompressed.

` `@return : 0, or an error code, which can be tested with ZSTD\_isError()

<a name="_page6_x32.00_y58.50"></a>**Streaming**

**typedef struct ZSTD\_inBuffer\_s {**

`  `**const void\* src;**    /\*\*< start of input buffer \*/

`  `**size\_t size;**        /\*\*< size of input buffer \*/

`  `**size\_t pos;**         /\*\*< position where reading stopped. Will be updated. Necessarily 0 <= pos <= size \*/ **} ZSTD\_inBuffer;**

**typedef struct ZSTD\_outBuffer\_s {**

`  `**void\*  dst;**         /\*\*< start of output buffer \*/

`  `**size\_t size;**        /\*\*< size of output buffer \*/

`  `**size\_t pos;**         /\*\*< position where writing stopped. Will be updated. Necessarily 0 <= pos <= size \*/ **} ZSTD\_outBuffer;**

<a name="_page6_x32.00_y204.50"></a>**Streaming compression - HowTo**

`  `A ZSTD\_CStream object is required to track streaming operation.

`  `Use ZSTD\_createCStream() and ZSTD\_freeCStream() to create/release resources.

`  `ZSTD\_CStream objects can be reused multiple times on consecutive compression operations.

`  `It is recommended to re-use ZSTD\_CStream since it will play nicer with system's memory, by re-using already allocated memory.

`  `For parallel execution, use one separate ZSTD\_CStream per thread.

`  `note : since v1.3.0, ZSTD\_CStream and ZSTD\_CCtx are the same thing.

`  `Parameters are sticky : when starting a new compression on the same context,   it will re-use the same sticky parameters as previous compression session.

`  `When in doubt, it's recommended to fully initialize the context before usage.   Use ZSTD\_CCtx\_reset() to reset the context and ZSTD\_CCtx\_setParameter(),

`  `ZSTD\_CCtx\_setPledgedSrcSize(), or ZSTD\_CCtx\_loadDictionary() and friends to

`  `set more specific parameters, the pledged source size, or load a dictionary.

`  `Use ZSTD\_compressStream2() with ZSTD\_e\_continue as many times as necessary to

`  `consume input stream. The function will automatically update both `pos`

`  `fields within `input` and `output`.

`  `Note that the function may not consume the entire input, for example, because

`  `the output buffer is already full, in which case `input.pos < input.size`.

`  `The caller must check if input has been entirely consumed.

`  `If not, the caller must make some room to receive more compressed data,

`  `and then present again remaining input data.

`  `note: ZSTD\_e\_continue is guaranteed to make some forward progress when called,

`        `but doesn't guarantee maximal forward progress. This is especially relevant

`        `when compressing with multiple threads. The call won't block if it can

`        `consume some input, but if it can't it will wait for some, but not all,

`        `output to be flushed.

` `@return : provides a minimum amount of data remaining to be flushed from internal buffers            or an error code, which can be tested using ZSTD\_isError().

`  `At any moment, it's possible to flush whatever data might remain stuck within internal buffer,

`  `using ZSTD\_compressStream2() with ZSTD\_e\_flush. `output->pos` will be updated.

`  `Note that, if `output->size` is too small, a single invocation with ZSTD\_e\_flush might not be enough (return code > 0).   In which case, make some room to receive more compressed data, and call again ZSTD\_compressStream2() with ZSTD\_e\_flush.   You must continue calling ZSTD\_compressStream2() with ZSTD\_e\_flush until it returns 0, at which point you can change the   operation.

`  `note: ZSTD\_e\_flush will flush as much output as possible, meaning when compressing with multiple threads, it will

`        `block until the flush is complete or the output buffer is full.

`  `@return : 0 if internal buffers are entirely flushed,

`            `>0 if some data still present within internal buffer (the value is minimal estimation of remaining size),

`            `or an error code, which can be tested using ZSTD\_isError().

`  `Calling ZSTD\_compressStream2() with ZSTD\_e\_end instructs to finish a frame.

`  `It will perform a flush and write frame epilogue.

`  `The epilogue is required for decoders to consider a frame completed.

`  `flush operation is the same, and follows same rules as calling ZSTD\_compressStream2() with ZSTD\_e\_flush.

`  `You must continue calling ZSTD\_compressStream2() with ZSTD\_e\_end until it returns 0, at which point you are free to   start a new frame.

`  `note: ZSTD\_e\_end will flush as much output as possible, meaning when compressing with multiple threads, it will

`        `block until the flush is complete or the output buffer is full.

`  `@return : 0 if frame fully completed and fully flushed,

`            `>0 if some data still present within internal buffer (the value is minimal estimation of remaining size),             or an error code, which can be tested using ZSTD\_isError().

**typedef ZSTD\_CCtx ZSTD\_CStream;**  /\*\*< CCtx and CStream are now effectively same object (>= v1.3.0) \*/

**ZSTD\_CStream management functions**

**ZSTD\_CStream\* ZSTD\_createCStream(void); size\_t ZSTD\_freeCStream(ZSTD\_CStream\* zcs);**  /\* accept NULL pointer \*/

**Streaming compression functions**

**typedef enum {**

`    `**ZSTD\_e\_continue=0,** /\* collect more data, encoder decides when to output compressed result, for optimal compression ratio \*/     **ZSTD\_e\_flush=1,**    /\* flush any data provided so far,

* **it creates (at least) one new block, that can be decoded immediately on reception;**
* **frame will continue: any future data can still reference previously compressed data, improving compression.**
* **note : multithreaded compression will block to flush as much output as possible. \*/**

`    `**ZSTD\_e\_end=2**       /\* flush any remaining data \_and\_ close current frame.

* **note that frame is only closed after compressed data is fully flushed (return value == 0).**
* **After that point, any additional data starts a new frame.**
* **note : each frame is independent (does not reference any content from previous frame).**

**: note : multithreaded compression will block to flush as much output as possible. \*/**

**} ZSTD\_EndDirective;**

**size\_t ZSTD\_compressStream2( ZSTD\_CCtx\* cctx,**

`                             `**ZSTD\_outBuffer\* output,**

`                             `**ZSTD\_inBuffer\* input,**

`                             `**ZSTD\_EndDirective endOp);**

`  `Behaves about the same as ZSTD\_compressStream, with additional control on end directive.

- Compression parameters are pushed into CCtx before starting compression, using ZSTD\_CCtx\_set\*()
- Compression parameters cannot be changed once compression is started (save a list of exceptions in multi-threading mode)
- output->pos must be <= dstCapacity, input->pos must be <= srcSize
- output->pos and input->pos will be updated. They are guaranteed to remain below their respective limit.
- endOp must be a valid directive
- When nbWorkers==0 (default), function is blocking : it completes its job before returning to caller.
- When nbWorkers>=1, function is non-blocking : it copies a portion of input, distributes jobs to internal worker threads, flush to output w

`                                                  `and then immediately returns, just indicating that there is some data remaining to be flush                                                   The function nonetheless guarantees forward progress : it will return only after it reads o

- Exception : if the first call requests a ZSTD\_e\_end directive and provides enough dstCapacity, the function delegates to ZSTD\_compress2() 
- @return provides a minimum amount of data remaining to be flushed from internal buffers

`            `or an error code, which can be tested using ZSTD\_isError().

`            `if @return != 0, flush is not fully completed, there is still some data left within internal buffers.

`            `This is useful for ZSTD\_e\_flush, since in this case more flushes are necessary to empty all buffers.

`            `For ZSTD\_e\_end, @return == 0 when internal buffers are fully flushed and frame is completed.

- after a ZSTD\_e\_end directive, if internal buffer is not fully flushed (@return != 0),

`            `only ZSTD\_e\_end or ZSTD\_e\_flush operations are allowed.

`            `Before starting a new compression job, or changing compression parameters,

`            `it is required to fully flush internal buffers.

**size\_t ZSTD\_CStreamInSize(void);**    /\*\*< recommended size for input buffer \*/

**size\_t ZSTD\_CStreamOutSize(void);**   /\*\*< recommended size for output buffer. Guarantee to successfully flush at least one complete compressed 

**size\_t ZSTD\_initCStream(ZSTD\_CStream\* zcs, int compressionLevel);**

/\*!

* **Alternative for ZSTD\_compressStream2(zcs, output, input, ZSTD\_e\_continue).**
* **NOTE: The return value is different. ZSTD\_compressStream() returns a hint for**
* **the next read size (if non-zero and not an error). ZSTD\_compressStream2()**
* **returns the minimum nb of bytes left to flush (if non-zero and not an error).**

` `**\*/**

**size\_t ZSTD\_compressStream(ZSTD\_CStream\* zcs, ZSTD\_outBuffer\* output, ZSTD\_inBuffer\* input);** /\*! Equivalent to ZSTD\_compressStream2(zcs, output, &emptyInput, ZSTD\_e\_flush). \*/

**size\_t ZSTD\_flushStream(ZSTD\_CStream\* zcs, ZSTD\_outBuffer\* output);**

/\*! Equivalent to ZSTD\_compressStream2(zcs, output, &emptyInput, ZSTD\_e\_end). \*/

**size\_t ZSTD\_endStream(ZSTD\_CStream\* zcs, ZSTD\_outBuffer\* output);**

`     `ZSTD\_CCtx\_reset(zcs, ZSTD\_reset\_session\_only);

`     `ZSTD\_CCtx\_refCDict(zcs, NULL); // clear the dictionary (if any)

`     `ZSTD\_CCtx\_setParameter(zcs, ZSTD\_c\_compressionLevel, compressionLevel);

<a name="_page7_x32.00_y584.50"></a>**Streaming decompression - HowTo**

`  `A ZSTD\_DStream object is required to track streaming operations.

`  `Use ZSTD\_createDStream() and ZSTD\_freeDStream() to create/release resources.   ZSTD\_DStream objects can be re-used multiple times.

`  `Use ZSTD\_initDStream() to start a new decompression operation.  @return : recommended first input size

`  `Alternatively, use advanced API to set specific properties.

`  `Use ZSTD\_decompressStream() repetitively to consume your input.

`  `The function will update both `pos` fields.

`  `If `input.pos < input.size`, some input has not been consumed.

`  `It's up to the caller to present again remaining data.

`  `The function tries to flush all data decoded immediately, respecting output buffer size.

`  `If `output.pos < output.size`, decoder has flushed everything it could.

`  `But if `output.pos == output.size`, there might be some data left within internal buffers.,

`  `In which case, call ZSTD\_decompressStream() again to flush whatever remains in the buffer.

`  `Note : with no additional input provided, amount of data flushed is necessarily <= ZSTD\_BLOCKSIZE\_MAX.  @return : 0 when a frame is completely decoded and fully flushed,

`        `or an error code, which can be tested using ZSTD\_isError(),

`        `or any other value > 0, which means there is still some decoding or flushing to do to complete current frame :                                 the return value is a suggested next input size (just a hint for better latency)

`                                `that will never request more than the remaining frame size.

**typedef ZSTD\_DCtx ZSTD\_DStream;**  /\*\*< DCtx and DStream are now effectively same object (>= v1.3.0) \*/

**ZSTD\_DStream management functions**

**ZSTD\_DStream\* ZSTD\_createDStream(void); size\_t ZSTD\_freeDStream(ZSTD\_DStream\* zds);**  /\* accept NULL pointer \*/

**Streaming decompression functions**

**size\_t ZSTD\_DStreamInSize(void);**    /\*!< recommended size for input buffer \*/

**size\_t ZSTD\_DStreamOutSize(void);**   /\*!< recommended size for output buffer. Guarantee to successfully flush at least one complete block in a

<a name="_page8_x32.00_y252.50"></a>**Simple dictionary API**

**size\_t ZSTD\_compress\_usingDict(ZSTD\_CCtx\* ctx,**

`                               `**void\* dst, size\_t dstCapacity,                          const void\* src, size\_t srcSize,**

`                         `**const void\* dict,size\_t dictSize,**

`                               `**int compressionLevel);**

`  `Compression at an explicit compression level using a Dictionary.

`  `A dictionary can be any arbitrary data segment (also called a prefix),

`  `or a buffer with specified information (see zdict.h).

`  `Note : This function loads the dictionary, resulting in significant startup delay.          It's intended for a dictionary used only once.

`  `Note 2 : When `dict == NULL || dictSize < 8` no dictionary is used. 

**size\_t ZSTD\_decompress\_usingDict(ZSTD\_DCtx\* dctx,**

`                                 `**void\* dst, size\_t dstCapacity,                            const void\* src, size\_t srcSize,**

`                           `**const void\* dict,size\_t dictSize);**

`  `Decompression using a known Dictionary.

`  `Dictionary must be identical to the one used during compression.

`  `Note : This function loads the dictionary, resulting in significant startup delay.          It's intended for a dictionary used only once.

`  `Note : When `dict == NULL || dictSize < 8` no dictionary is used. 

<a name="_page8_x32.00_y487.00"></a>**Bulk processing dictionary API**

**ZSTD\_CDict\* ZSTD\_createCDict(const void\* dictBuffer, size\_t dictSize,                              int compressionLevel);**

`  `When compressing multiple messages or blocks using the same dictionary,

`  `it's recommended to digest the dictionary only once, since it's a costly operation.

`  `ZSTD\_createCDict() will create a state from digesting a dictionary.

`  `The resulting state can be used for future compression operations with very limited startup cost.

`  `ZSTD\_CDict can be created once and shared by multiple threads concurrently, since its usage is read-only.

` `@dictBuffer can be released after ZSTD\_CDict creation, because its content is copied within CDict.

`  `Note 1 : Consider experimental function `ZSTD\_createCDict\_byReference()` if you prefer to not duplicate @dictBuffer content.

`  `Note 2 : A ZSTD\_CDict can be created from an empty @dictBuffer,

`      `in which case the only thing that it transports is the @compressionLevel.

`      `This can be useful in a pipeline featuring ZSTD\_compress\_usingCDict() exclusively,

`      `expecting a ZSTD\_CDict parameter with any data, including those without a known dictionary. 

**size\_t      ZSTD\_freeCDict(ZSTD\_CDict\* CDict);**

`  `Function frees memory allocated by ZSTD\_createCDict().

`  `If a NULL pointer is passed, no operation is performed. 

**size\_t ZSTD\_compress\_usingCDict(ZSTD\_CCtx\* cctx,**

`                                `**void\* dst, size\_t dstCapacity,                           const void\* src, size\_t srcSize,**

`                          `**const ZSTD\_CDict\* cdict);**

`  `Compression using a digested Dictionary.

`  `Recommended when same dictionary is used multiple times.

`  `Note : compression level is \_decided at dictionary creation time\_,

`     `and frame parameters are hardcoded (dictID=yes, contentSize=yes, checksum=no) 

**ZSTD\_DDict\* ZSTD\_createDDict(const void\* dictBuffer, size\_t dictSize);**

`  `Create a digested dictionary, ready to start decompression operation without startup delay.   dictBuffer can be released after DDict creation, as its content is copied inside DDict. 

**size\_t      ZSTD\_freeDDict(ZSTD\_DDict\* ddict);**

`  `Function frees memory allocated with ZSTD\_createDDict()   If a NULL pointer is passed, no operation is performed. 

**size\_t ZSTD\_decompress\_usingDDict(ZSTD\_DCtx\* dctx,**

`                                  `**void\* dst, size\_t dstCapacity,                             const void\* src, size\_t srcSize,**

`                            `**const ZSTD\_DDict\* ddict);**

`  `Decompression using a digested Dictionary.

`  `Recommended when same dictionary is used multiple times. 

<a name="_page9_x32.00_y234.00"></a>**Dictionary helper functions**

**unsigned ZSTD\_getDictID\_fromDict(const void\* dict, size\_t dictSize);**

`  `Provides the dictID stored within dictionary.

`  `if @return == 0, the dictionary is not conformant with Zstandard specification.   It can still be loaded, but as a content-only dictionary. 

**unsigned ZSTD\_getDictID\_fromCDict(const ZSTD\_CDict\* cdict);**

`  `Provides the dictID of the dictionary loaded into `cdict`.

`  `If @return == 0, the dictionary is not conformant to Zstandard specification, or empty.   Non-conformant dictionaries can still be loaded, but as content-only dictionaries. 

**unsigned ZSTD\_getDictID\_fromDDict(const ZSTD\_DDict\* ddict);**

`  `Provides the dictID of the dictionary loaded into `ddict`.

`  `If @return == 0, the dictionary is not conformant to Zstandard specification, or empty.   Non-conformant dictionaries can still be loaded, but as content-only dictionaries. 

**unsigned ZSTD\_getDictID\_fromFrame(const void\* src, size\_t srcSize);**

`  `Provides the dictID required to decompressed the frame stored within `src`.

`  `If @return == 0, the dictID could not be decoded.

`  `This could for one of the following reasons :

- The frame does not require a dictionary to be decoded (most common case).
- The frame was built with dictID intentionally removed. Whatever dictionary is necessary is a hidden information.

`    `Note : this use case also happens when using a non-conformant dictionary.

- `srcSize` is too small, and as a result, the frame header could not be decoded (only possible if `srcSize < ZSTD\_FRAMEHEADERSIZE\_MAX`).
- This is not a Zstandard frame.

`  `When identifying the exact failure cause, it's possible to use ZSTD\_getFrameHeader(), which will provide a more precise error code. 

<a name="_page9_x32.00_y540.00"></a>**Advanced dictionary and prefix API (Requires v1.4.0+)**

` `This API allows dictionaries to be used with ZSTD\_compress2(),

` `ZSTD\_compressStream2(), and ZSTD\_decompressDCtx(). Dictionaries are sticky, and  only reset with the context is reset with ZSTD\_reset\_parameters or

` `ZSTD\_reset\_session\_and\_parameters. Prefixes are single-use.

**size\_t ZSTD\_CCtx\_loadDictionary(ZSTD\_CCtx\* cctx, const void\* dict, size\_t dictSize);**

`  `Create an internal CDict from `dict` buffer.

`  `Decompression will have to use same dictionary.

` `@result : 0, or an error code (which can be tested with ZSTD\_isError()).

`  `Special: Loading a NULL (or 0-size) dictionary invalidates previous dictionary,

`           `meaning "return to no-dictionary mode".

`  `Note 1 : Dictionary is sticky, it will be used for all future compressed frames.

`           `To return to "no-dictionary" situation, load a NULL dictionary (or reset parameters).   Note 2 : Loading a dictionary involves building tables.

`           `It's also a CPU consuming operation, with non-negligible impact on latency.

`           `Tables are dependent on compression parameters, and for this reason,

`           `compression parameters can no longer be changed after loading a dictionary.

`  `Note 3 :`dict` content will be copied internally.

`           `Use experimental ZSTD\_CCtx\_loadDictionary\_byReference() to reference content instead.            In such a case, dictionary buffer must outlive its users.

`  `Note 4 : Use ZSTD\_CCtx\_loadDictionary\_advanced()

`           `to precisely select how dictionary content must be interpreted. 

**size\_t ZSTD\_CCtx\_refCDict(ZSTD\_CCtx\* cctx, const ZSTD\_CDict\* cdict);**

`  `Reference a prepared dictionary, to be used for all next compressed frames.

`  `Note that compression parameters are enforced from within CDict,

`  `and supersede any compression parameter previously set within CCtx.

`  `The parameters ignored are labelled as "superseded-by-cdict" in the ZSTD\_cParameter enum docs.   The ignored parameters will be used again if the CCtx is returned to no-dictionary mode.

`  `The dictionary will remain valid for future compressed frames using same CCtx.

` `@result : 0, or an error code (which can be tested with ZSTD\_isError()).

`  `Special : Referencing a NULL CDict means "return to no-dictionary mode".

`  `Note 1 : Currently, only one dictionary can be managed.

`           `Referencing a new dictionary effectively "discards" any previous one.

`  `Note 2 : CDict is just referenced, its lifetime must outlive its usage within CCtx. 

**size\_t ZSTD\_CCtx\_refPrefix(ZSTD\_CCtx\* cctx,**

`                     `**const void\* prefix, size\_t prefixSize);**

`  `Reference a prefix (single-usage dictionary) for next compressed frame.

`  `A prefix is \*\*only used once\*\*. Tables are discarded at end of frame (ZSTD\_e\_end).

`  `Decompression will need same prefix to properly regenerate data.

`  `Compressing with a prefix is similar in outcome as performing a diff and compressing it,

`  `but performs much faster, especially during decompression (compression speed is tunable with compression level).  @result : 0, or an error code (which can be tested with ZSTD\_isError()).

`  `Special: Adding any prefix (including NULL) invalidates any previous prefix or dictionary

`  `Note 1 : Prefix buffer is referenced. It \*\*must\*\* outlive compression.

`           `Its content must remain unmodified during compression.

`  `Note 2 : If the intention is to diff some large src data blob with some prior version of itself,

`           `ensure that the window size is large enough to contain the entire source.

`           `See ZSTD\_c\_windowLog.

`  `Note 3 : Referencing a prefix involves building tables, which are dependent on compression parameters.

`           `It's a CPU consuming operation, with non-negligible impact on latency.

`           `If there is a need to use the same prefix multiple times, consider loadDictionary instead.

`  `Note 4 : By default, the prefix is interpreted as raw content (ZSTD\_dct\_rawContent).

`           `Use experimental ZSTD\_CCtx\_refPrefix\_advanced() to alter dictionary interpretation. 

**size\_t ZSTD\_DCtx\_loadDictionary(ZSTD\_DCtx\* dctx, const void\* dict, size\_t dictSize);**

`  `Create an internal DDict from dict buffer,

`  `to be used to decompress next frames.

`  `The dictionary remains valid for all future frames, until explicitly invalidated.

` `@result : 0, or an error code (which can be tested with ZSTD\_isError()).

`  `Special : Adding a NULL (or 0-size) dictionary invalidates any previous dictionary,

`            `meaning "return to no-dictionary mode".

`  `Note 1 : Loading a dictionary involves building tables,

`           `which has a non-negligible impact on CPU usage and latency.

`           `It's recommended to "load once, use many times", to amortize the cost

`  `Note 2 :`dict` content will be copied internally, so `dict` can be released after loading.

`           `Use ZSTD\_DCtx\_loadDictionary\_byReference() to reference dictionary content instead.   Note 3 : Use ZSTD\_DCtx\_loadDictionary\_advanced() to take control of

`           `how dictionary content is loaded and interpreted.

**size\_t ZSTD\_DCtx\_refDDict(ZSTD\_DCtx\* dctx, const ZSTD\_DDict\* ddict);**

`  `Reference a prepared dictionary, to be used to decompress next frames.

`  `The dictionary remains active for decompression of future frames using same DCtx.

`  `If called with ZSTD\_d\_refMultipleDDicts enabled, repeated calls of this function   will store the DDict references in a table, and the DDict used for decompression   will be determined at decompression time, as per the dict ID in the frame.

`  `The memory for the table is allocated on the first call to refDDict, and can be   freed with ZSTD\_freeDCtx().

` `@result : 0, or an error code (which can be tested with ZSTD\_isError()).

`  `Note 1 : Currently, only one dictionary can be managed.

`           `Referencing a new dictionary effectively "discards" any previous one.

`  `Special: referencing a NULL DDict means "return to no-dictionary mode".

`  `Note 2 : DDict is just referenced, its lifetime must outlive its usage from DCtx.

**size\_t ZSTD\_DCtx\_refPrefix(ZSTD\_DCtx\* dctx,**

`                     `**const void\* prefix, size\_t prefixSize);**

`  `Reference a prefix (single-usage dictionary) to decompress next frame.

`  `This is the reverse operation of ZSTD\_CCtx\_refPrefix(),

`  `and must use the same prefix as the one used during compression.

`  `Prefix is \*\*only used once\*\*. Reference is discarded at end of frame.

`  `End of frame is reached when ZSTD\_decompressStream() returns 0.

` `@result : 0, or an error code (which can be tested with ZSTD\_isError()).

`  `Note 1 : Adding any prefix (including NULL) invalidates any previously set prefix or dictionary

`  `Note 2 : Prefix buffer is referenced. It \*\*must\*\* outlive decompression.

`           `Prefix buffer must remain unmodified up to the end of frame,

`           `reached when ZSTD\_decompressStream() returns 0.

`  `Note 3 : By default, the prefix is treated as raw content (ZSTD\_dct\_rawContent).

`           `Use ZSTD\_CCtx\_refPrefix\_advanced() to alter dictMode (Experimental section)

`  `Note 4 : Referencing a raw content prefix has almost no cpu nor memory cost.

`           `A full dictionary is more costly, as it requires building tables.

**size\_t ZSTD\_sizeof\_CCtx(const ZSTD\_CCtx\* cctx);**

**size\_t ZSTD\_sizeof\_DCtx(const ZSTD\_DCtx\* dctx);**

**size\_t ZSTD\_sizeof\_CStream(const ZSTD\_CStream\* zcs); size\_t ZSTD\_sizeof\_DStream(const ZSTD\_DStream\* zds); size\_t ZSTD\_sizeof\_CDict(const ZSTD\_CDict\* cdict); size\_t ZSTD\_sizeof\_DDict(const ZSTD\_DDict\* ddict);**

`  `These functions give the \_current\_ memory usage of selected object.

`  `Note that object memory usage can evolve (increase or decrease) over time. 

<a name="_page11_x32.00_y125.50"></a>**experimental API (static linking only)**

` `The following symbols and constants

` `are not planned to join "stable API" status in the near future.

` `They can still change in future versions.

` `Some of them are planned to remain in the static\_only section indefinitely.

` `Some of them might be removed in the future (especially when redundant with existing stable functions)

**typedef struct {**

`    `**unsigned int offset;**      /\* The offset of the match. (NOT the same as the offset code)

* **If offset == 0 and matchLength == 0, this sequence represents the last**
* **literals in the block of litLength size.**

`                               `**\*/**

`    `**unsigned int litLength;**   /\* Literal length of the sequence. \*/     **unsigned int matchLength;** /\* Match length of the sequence. \*/

/\* Note: Users of this API may provide a sequence with matchLength == litLength == offset == 0.

* **In this case, we will treat the sequence as a marker for a block boundary.**

`                               `**\*/**

`    `**unsigned int rep;**         /\* Represents which repeat offset is represented by the field 'offset'.

* **Ranges from [0, 3].**

`                               `**\***

* **Repeat offsets are essentially previous offsets from previous sequences sorted in**
* **recency order. For more detail, see doc/zstd\_compression\_format.md**

`                               `**\***

* **If rep == 0, then 'offset' does not contain a repeat offset.**
* **If rep > 0:**
* **If litLength != 0:**
* **rep == 1 --> offset == repeat\_offset\_1**
* **rep == 2 --> offset == repeat\_offset\_2**
* **rep == 3 --> offset == repeat\_offset\_3**
* **If litLength == 0:**
* **rep == 1 --> offset == repeat\_offset\_2**
* **rep == 2 --> offset == repeat\_offset\_3**
* **rep == 3 --> offset == repeat\_offset\_1 - 1**

`                               `**\***

* **Note: This field is optional. ZSTD\_generateSequences() will calculate the value of**
* **'rep', but repeat offsets do not necessarily need to be calculated from an external**
* **sequence provider's perspective. For example, ZSTD\_compressSequences() does not**
* **use this 'rep' field at all (as of now).**

`                               `**\*/**

**} ZSTD\_Sequence;**

**typedef struct {**

`    `**unsigned windowLog;           unsigned chainLog;            unsigned hashLog;             unsigned searchLog;           unsigned minMatch;            unsigned targetLength;        ZSTD\_strategy strategy;   } ZSTD\_compressionParameters;**

**typedef struct {**

`    `**int contentSizeFlag;     int checksumFlag;        int noDictIDFlag;    } ZSTD\_frameParameters;**

/\*\*< largest match distance : larger == more compression, more memory needed during decompression \*/ /\*\*< fully searched segment : larger == more compression, slower, more memory (useless for fast) \*/ /\*\*< dispatch table : larger == faster, more memory \*/

/\*\*< nb of searches : larger == more compression, slower \*/

/\*\*< match length searched : larger == faster decompression, sometimes less compression \*/

/\*\*< acceptable match size for optimal parser (only) : larger == more compression, slower \*/

/\*\*< see ZSTD\_strategy definition above \*/

/\*\*< 1: content size will be in frame header (when known) \*/

/\*\*< 1: generate a 32-bits checksum using XXH64 algorithm at end of frame, for error detection \*/

/\*\*< 1: no dictID will be saved into frame header (dictID is only useful for dictionary compression) \*/

**typedef struct {**

`    `**ZSTD\_compressionParameters cParams;     ZSTD\_frameParameters fParams;**

**} ZSTD\_parameters;**

**typedef enum {**

`    `**ZSTD\_dct\_auto = 0,**       /\* dictionary is "full" when starting with ZSTD\_MAGIC\_DICTIONARY, otherwise it is "rawContent" \*/     **ZSTD\_dct\_rawContent = 1,** /\* ensures dictionary is always loaded as rawContent, even if it starts with ZSTD\_MAGIC\_DICTIONARY \*/     **ZSTD\_dct\_fullDict = 2**    /\* refuses to load a dictionary if it does not respect Zstandard's specification, starting with ZSTD\_MAGIC\_DICTI **} ZSTD\_dictContentType\_e;**

**typedef enum {**

`    `**ZSTD\_dlm\_byCopy = 0,**  /\*\*< Copy dictionary content internally \*/

`    `**ZSTD\_dlm\_byRef = 1**    /\*\*< Reference dictionary content -- the dictionary buffer must outlive its users. \*/ **} ZSTD\_dictLoadMethod\_e;**

**typedef enum {**

`    `**ZSTD\_f\_zstd1 = 0,**           /\* zstd frame format, specified in zstd\_compression\_format.md (default) \*/     **ZSTD\_f\_zstd1\_magicless = 1**  /\* Variant of zstd frame format, without initial 4-bytes magic number.

* **Useful to save 4 bytes per generated frame.**
* **Decoder cannot recognise automatically this format, requiring this instruction. \*/**

**} ZSTD\_format\_e;**

**typedef enum {**

/\* Note: this enum controls ZSTD\_d\_forceIgnoreChecksum \*/     **ZSTD\_d\_validateChecksum = 0,**

`    `**ZSTD\_d\_ignoreChecksum = 1**

**} ZSTD\_forceIgnoreChecksum\_e;**

**typedef enum {**

/\* Note: this enum controls ZSTD\_d\_refMultipleDDicts \*/     **ZSTD\_rmd\_refSingleDDict = 0,**

`    `**ZSTD\_rmd\_refMultipleDDicts = 1**

**} ZSTD\_refMultipleDDicts\_e;**

**typedef enum {**

/\* Note: this enum and the behavior it controls are effectively internal

* **implementation details of the compressor. They are expected to continue**
* **to evolve and should be considered only in the context of extremely**
* **advanced performance tuning.**

`     `**\***

* **Zstd currently supports the use of a CDict in three ways:**

`     `**\***

* **- The contents of the CDict can be copied into the working context. This**
* **means that the compression can search both the dictionary and input**
* **while operating on a single set of internal tables. This makes**
* **the compression faster per-byte of input. However, the initial copy of**
* **the CDict's tables incurs a fixed cost at the beginning of the**
* **compression. For small compressions (< 8 KB), that copy can dominate**
* **the cost of the compression.**

`     `**\***

* **- The CDict's tables can be used in-place. In this model, compression is**
* **slower per input byte, because the compressor has to search two sets of**
* **tables. However, this model incurs no start-up cost (as long as the**
* **working context's tables can be reused). For small inputs, this can be**
* **faster than copying the CDict's tables.**

`     `**\***

* **- The CDict's tables are not used at all, and instead we use the working**
* **context alone to reload the dictionary and use params based on the source**
* **size. See ZSTD\_compress\_insertDictionary() and ZSTD\_compress\_usingDict().**
* **This method is effective when the dictionary sizes are very small relative**
* **to the input size, and the input size is fairly large to begin with.**

`     `**\***

* **Zstd has a simple internal heuristic that selects which strategy to use**
* **at the beginning of a compression. However, if experimentation shows that**
* **Zstd is making poor choices, it is possible to override that choice with**
* **this enum.**

`     `**\*/**

`    `**ZSTD\_dictDefaultAttach = 0,** /\* Use the default heuristic. \*/     **ZSTD\_dictForceAttach   = 1,** /\* Never copy the dictionary. \*/     **ZSTD\_dictForceCopy     = 2,** /\* Always copy the dictionary. \*/     **ZSTD\_dictForceLoad     = 3**  /\* Always reload the dictionary \*/

**} ZSTD\_dictAttachPref\_e;**

**typedef enum {**

`  `**ZSTD\_lcm\_auto = 0,**          /\*\*< Automatically determine the compression mode based on the compression level.

* **Negative compression levels will be uncompressed, and positive compression**
* **levels will be compressed. \*/**

`  `**ZSTD\_lcm\_huffman = 1,**       /\*\*< Always attempt Huffman compression. Uncompressed literals will still be

* **emitted if Huffman compression is not profitable. \*/**

`  `**ZSTD\_lcm\_uncompressed = 2**   /\*\*< Always emit uncompressed literals. \*/

**} ZSTD\_literalCompressionMode\_e;**

**typedef enum {**
**
`  `/\* Note: This enum controls features which are conditionally beneficial. Zstd typically will make a final

* **decision on whether or not to enable the feature (ZSTD\_ps\_auto), but setting the switch to ZSTD\_ps\_enable**
* **or ZSTD\_ps\_disable allow for a force enable/disable the feature.**

`   `**\*/**

`  `**ZSTD\_ps\_auto = 0,**         /\* Let the library automatically determine whether the feature shall be enabled \*/   **ZSTD\_ps\_enable = 1,**       /\* Force-enable the feature \*/

`  `**ZSTD\_ps\_disable = 2**       /\* Do not use the feature \*/

<a name="_page12_x32.00_y753.50"></a>**} ZSTD\_paramSwitch\_e;**

**Frame size functions**

**ZSTDLIB\_STATIC\_API unsigned long long ZSTD\_findDecompressedSize(const void\* src, size\_t srcSize);**

`  ``src` should point to the start of a series of ZSTD encoded and/or skippable frames   `srcSize` must be the \_exact\_ size of this series

`       `(i.e. there should be a frame boundary at `src + srcSize`)

`  `@return : - decompressed size of all data in all successive frames

- if the decompressed size cannot be determined: ZSTD\_CONTENTSIZE\_UNKNOWN
- if an error occurred: ZSTD\_CONTENTSIZE\_ERROR

`   `note 1 : decompressed size is an optional field, that may not be present, especially in streaming mode.             When `return==ZSTD\_CONTENTSIZE\_UNKNOWN`, data to decompress could be any size.

`            `In which case, it's necessary to use streaming mode to decompress data.

`   `note 2 : decompressed size is always present when compression is done with ZSTD\_compress()

`   `note 3 : decompressed size can be very large (64-bits value),

`            `potentially larger than what local system can handle as a single memory segment.

`            `In which case, it's necessary to use streaming mode to decompress data.

`   `note 4 : If source is untrusted, decompressed size could be wrong or intentionally modified.

`            `Always ensure result fits within application's authorized limits.

`            `Each application can set its own limits.

`   `note 5 : ZSTD\_findDecompressedSize handles multiple frames, and so it must traverse the input to

`            `read each contained frame header.  This is fast as most of the data is skipped,

`            `however it does mean that all frame data must be present and valid. 

**ZSTDLIB\_STATIC\_API unsigned long long ZSTD\_decompressBound(const void\* src, size\_t srcSize);**

`  ``src` should point to the start of a series of ZSTD encoded and/or skippable frames

`  ``srcSize` must be the \_exact\_ size of this series

`       `(i.e. there should be a frame boundary at `src + srcSize`)

`  `@return : - upper-bound for the decompressed size of all data in all successive frames

- if an error occurred: ZSTD\_CONTENTSIZE\_ERROR

`  `note 1  : an error can occur if `src` contains an invalid or incorrectly formatted frame.

`  `note 2  : the upper-bound is exact when the decompressed size field is available in every ZSTD encoded frame of `src`.             in this case, `ZSTD\_findDecompressedSize` and `ZSTD\_decompressBound` return the same value.

`  `note 3  : when the decompressed size field isn't available, the upper-bound for that frame is calculated by:

`              `upper-bound = # blocks \* min(128 KB, Window\_Size)

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_frameHeaderSize(const void\* src, size\_t srcSize);**

`  `srcSize must be >= ZSTD\_FRAMEHEADERSIZE\_PREFIX.

` `@return : size of the Frame Header,

`           `or an error code (if srcSize is too small) 

**typedef enum {**

`  `**ZSTD\_sf\_noBlockDelimiters = 0,**         /\* Representation of ZSTD\_Sequence has no block delimiters, sequences only \*/   **ZSTD\_sf\_explicitBlockDelimiters = 1**    /\* Representation of ZSTD\_Sequence contains explicit block delimiters \*/

**} ZSTD\_sequenceFormat\_e;**

` `Generate sequences using ZSTD\_compress2, given a source buffer.

` `Each block will end with a dummy sequence

` `with offset == 0, matchLength == 0, and litLength == length of last literals.  litLength may be == 0, and if so, then the sequence of (of: 0 ml: 0 ll: 0)

` `simply acts as a block delimiter.

` `zc can be used to insert custom compression params.  This function invokes ZSTD\_compress2

` `The output of this function can be fed into ZSTD\_compressSequences() with CCtx  setting of ZSTD\_c\_blockDelimiters as ZSTD\_sf\_explicitBlockDelimiters

` `@return : number of sequences generated

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_mergeBlockDelimiters(ZSTD\_Sequence\* sequences, size\_t seqsSize);**

` `Given an array of ZSTD\_Sequence, remove all sequences that represent block delimiters/last literals  by merging them into into the literals of the next sequence.

` `As such, the final generated result has no explicit representation of block boundaries,  and the final last literals segment is not represented in the sequences.

` `The output of this function can be fed into ZSTD\_compressSequences() with CCtx  setting of ZSTD\_c\_blockDelimiters as ZSTD\_sf\_noBlockDelimiters

` `@return : number of sequences left after merging

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_compressSequences(ZSTD\_CCtx\* const cctx, void\* dst, size\_t dstSize,                       const ZSTD\_Sequence\* inSeqs, size\_t inSeqsSize,**

`                      `**const void\* src, size\_t srcSize);**

` `Compress an array of ZSTD\_Sequence, generated from the original source buffer, into dst.

` `If a dictionary is included, then the cctx should reference the dict. (see: ZSTD\_CCtx\_refCDict(), ZSTD\_CCtx\_loadDictionary(), etc.)  The entire source is compressed into a single frame.

` `The compression behavior changes based on cctx params. In particular:

`    `If ZSTD\_c\_blockDelimiters == ZSTD\_sf\_noBlockDelimiters, the array of ZSTD\_Sequence is expected to contain     no block delimiters (defined in ZSTD\_Sequence). Block boundaries are roughly determined based on

`    `the block size derived from the cctx, and sequences may be split. This is the default setting.

`    `If ZSTD\_c\_blockDelimiters == ZSTD\_sf\_explicitBlockDelimiters, the array of ZSTD\_Sequence is expected to contain     block delimiters (defined in ZSTD\_Sequence). Behavior is undefined if no block delimiters are provided.

`    `If ZSTD\_c\_validateSequences == 0, this function will blindly accept the sequences provided. Invalid sequences cause undefined     behavior. If ZSTD\_c\_validateSequences == 1, then if sequence is invalid (see doc/zstd\_compression\_format.md for

`    `specifics regarding offset/matchlength requirements) then the function will bail out and return an error.

`    `In addition to the two adjustable experimental params, there are other important cctx params.

- ZSTD\_c\_minMatch MUST be set as less than or equal to the smallest match generated by the match finder. It has a minimum value of ZSTD\_M
- ZSTD\_c\_compressionLevel accordingly adjusts the strength of the entropy coder, as it would in typical compression.
- ZSTD\_c\_windowLog affects offset validation: this function will return an error at higher debug levels if a provided offset

`      `is larger than what the spec allows for a given window log and dictionary (if present). See: doc/zstd\_compression\_format.md

` `Note: Repcodes are, as of now, always re-calculated within this function, so ZSTD\_Sequence::rep is unused.

` `Note 2: Once we integrate ability to ingest repcodes, the explicit block delims mode must respect those repcodes exactly,          and cannot emit an RLE block that disagrees with the repcode history

` `@return : final compressed size or a ZSTD error.

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_writeSkippableFrame(void\* dst, size\_t dstCapacity,**

`                                `**const void\* src, size\_t srcSize, unsigned magicVariant);**

` `Generates a zstd skippable frame containing data given by src, and writes it to dst buffer.

` `Skippable frames begin with a a 4-byte magic number. There are 16 possible choices of magic number,  ranging from ZSTD\_MAGIC\_SKIPPABLE\_START to ZSTD\_MAGIC\_SKIPPABLE\_START+15.

` `As such, the parameter magicVariant controls the exact skippable frame magic number variant used, so  the magic number used will be ZSTD\_MAGIC\_SKIPPABLE\_START + magicVariant.

` `Returns an error if destination buffer is not large enough, if the source size is not representable

` `with a 4-byte unsigned int, or if the parameter magicVariant is greater than 15 (and therefore invalid).

` `@return : number of bytes written or a ZSTD error.

**size\_t ZSTD\_readSkippableFrame(void\* dst, size\_t dstCapacity, unsigned\* magicVariant,                                 const void\* src, size\_t srcSize);**

` `Retrieves a zstd skippable frame containing data given by src, and writes it to dst buffer.

` `The parameter magicVariant will receive the magicVariant that was supplied when the frame was written,  i.e. magicNumber - ZSTD\_MAGIC\_SKIPPABLE\_START.  This can be NULL if the caller is not interested

` `in the magicVariant.

` `Returns an error if destination buffer is not large enough, or if the frame is not skippable.  @return : number of bytes written or a ZSTD error.

**unsigned ZSTD\_isSkippableFrame(const void\* buffer, size\_t size);**

`  `Tells if the content of `buffer` starts with a valid Frame Identifier for a skippable frame.

<a name="_page14_x32.00_y526.50"></a>**Memory management**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateCCtxSize(int compressionLevel);**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateCCtxSize\_usingCParams(ZSTD\_compressionParameters cParams); ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateCCtxSize\_usingCCtxParams(const ZSTD\_CCtx\_params\* params); ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateDCtxSize(void);**

`  `These functions make it possible to estimate memory usage   of a future {D,C}Ctx, before its creation.

`  `ZSTD\_estimateCCtxSize() will provide a memory budget large enough

`  `for any compression level up to selected one.

`  `Note : Unlike ZSTD\_estimateCStreamSize\*(), this estimate

`         `does not include space for a window buffer.

`         `Therefore, the estimation is only guaranteed for single-shot compressions, not streaming.   The estimate will assume the input may be arbitrarily large,

`  `which is the worst case.

`  `When srcSize can be bound by a known and rather "small" value,

`  `this fact can be used to provide a tighter estimation

`  `because the CCtx compression context will need less memory.

`  `This tighter estimation can be provided by more advanced functions

`  `ZSTD\_estimateCCtxSize\_usingCParams(), which can be used in tandem with ZSTD\_getCParams(),

`  `and ZSTD\_estimateCCtxSize\_usingCCtxParams(), which can be used in tandem with ZSTD\_CCtxParams\_setParameter().   Both can be used to estimate memory using custom compression parameters and arbitrary srcSize limits.

`  `Note 2 : only single-threaded compression is supported.

`  `ZSTD\_estimateCCtxSize\_usingCCtxParams() will return an error code if ZSTD\_c\_nbWorkers is >= 1.

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateCStreamSize(int compressionLevel);**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateCStreamSize\_usingCParams(ZSTD\_compressionParameters cParams); ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateCStreamSize\_usingCCtxParams(const ZSTD\_CCtx\_params\* params); ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateDStreamSize(size\_t windowSize);**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateDStreamSize\_fromFrame(const void\* src, size\_t srcSize);**

`  `ZSTD\_estimateCStreamSize() will provide a budget large enough for any compression level up to selected one.

`  `It will also consider src size to be arbitrarily "large", which is worst case.

`  `If srcSize is known to always be small, ZSTD\_estimateCStreamSize\_usingCParams() can provide a tighter estimation.

`  `ZSTD\_estimateCStreamSize\_usingCParams() can be used in tandem with ZSTD\_getCParams() to create cParams from compressionLevel.

`  `ZSTD\_estimateCStreamSize\_usingCCtxParams() can be used in tandem with ZSTD\_CCtxParams\_setParameter(). Only single-threaded compression is s   Note : CStream size estimation is only correct for single-threaded compression.

`  `ZSTD\_DStream memory budget depends on window Size.

`  `This information can be passed manually, using ZSTD\_estimateDStreamSize,

`  `or deducted from a valid frame Header, using ZSTD\_estimateDStreamSize\_fromFrame();

`  `Note : if streaming is init with function ZSTD\_init?Stream\_usingDict(),

`         `an internal ?Dict will be created, which additional size is not estimated here.

`         `In this case, get total size by adding ZSTD\_estimate?DictSize 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateCDictSize(size\_t dictSize, int compressionLevel);**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateCDictSize\_advanced(size\_t dictSize, ZSTD\_compressionParameters cParams, ZSTD\_dictLoadMethod\_e dictLoad ZSTDLIB\_STATIC\_API size\_t ZSTD\_estimateDDictSize(size\_t dictSize, ZSTD\_dictLoadMethod\_e dictLoadMethod);**

`  `ZSTD\_estimateCDictSize() will bet that src size is relatively "small", and content is copied, like ZSTD\_createCDict().

`  `ZSTD\_estimateCDictSize\_advanced() makes it possible to control compression parameters precisely, like ZSTD\_createCDict\_advanced().   Note : dictionaries created by reference (`ZSTD\_dlm\_byRef`) are logically smaller.

**ZSTDLIB\_STATIC\_API ZSTD\_CCtx\*    ZSTD\_initStaticCCtx(void\* workspace, size\_t workspaceSize); ZSTDLIB\_STATIC\_API ZSTD\_CStream\* ZSTD\_initStaticCStream(void\* workspace, size\_t workspaceSize);**    /\*\*< same as ZSTD\_initStaticCCtx() \*/

`  `Initialize an object using a pre-allocated fixed-size buffer.

`  `workspace: The memory area to emplace the object into.

`             `Provided pointer \*must be 8-bytes aligned\*.

`             `Buffer must outlive object.

`  `workspaceSize: Use ZSTD\_estimate\*Size() to determine

`                 `how large workspace must be to support target scenario.

` `@return : pointer to object (same address as workspace, just different type),

`           `or NULL if error (size too small, incorrect alignment, etc.)

`  `Note : zstd will never resize nor malloc() when using a static buffer.

`         `If the object requires more memory than available,

`         `zstd will just error out (typically ZSTD\_error\_memory\_allocation).

`  `Note 2 : there is no corresponding "free" function.

`           `Since workspace is allocated externally, it must be freed externally too.

`  `Note 3 : cParams : use ZSTD\_getCParams() to convert a compression level

`           `into its associated cParams.

`  `Limitation 1 : currently not compatible with internal dictionary creation, triggered by

`                 `ZSTD\_CCtx\_loadDictionary(), ZSTD\_initCStream\_usingDict() or ZSTD\_initDStream\_usingDict().   Limitation 2 : static cctx currently not compatible with multi-threading.

`  `Limitation 3 : static dctx is incompatible with legacy support.

**ZSTDLIB\_STATIC\_API ZSTD\_DStream\* ZSTD\_initStaticDStream(void\* workspace, size\_t workspaceSize);**    /\*\*< same as ZSTD\_initStaticDCtx() \*/

**typedef void\* (\*ZSTD\_allocFunction) (void\* opaque, size\_t size);**

**typedef void  (\*ZSTD\_freeFunction) (void\* opaque, void\* address);**

**typedef struct { ZSTD\_allocFunction customAlloc; ZSTD\_freeFunction customFree; void\* opaque; } ZSTD\_customMem; static**

**#ifdef \_\_GNUC\_\_**

**\_\_attribute\_\_((\_\_unused\_\_))**

**#endif**

**ZSTD\_customMem const ZSTD\_defaultCMem = { NULL, NULL, NULL };**  /\*\*< this constant defers to stdlib's functions \*/

`  `These prototypes make it possible to pass your own allocation/free functions.

`  `ZSTD\_customMem is provided at creation time, using ZSTD\_create\*\_advanced() variants listed below.   All allocation/free operations will be completed using these custom variants instead of regular  ones.

**typedef struct POOL\_ctx\_s ZSTD\_threadPool;**

**ZSTDLIB\_STATIC\_API ZSTD\_threadPool\* ZSTD\_createThreadPool(size\_t numThreads); ZSTDLIB\_STATIC\_API void ZSTD\_freeThreadPool (ZSTD\_threadPool\* pool);**  /\* accept NULL pointer \*/ **ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtx\_refThreadPool(ZSTD\_CCtx\* cctx, ZSTD\_threadPool\* pool);**

`  `These prototypes make it possible to share a thread pool among multiple compression contexts.   This can limit resources for applications with multiple threads where each one uses

`  `a threaded compression mode (via ZSTD\_c\_nbWorkers parameter).

`  `ZSTD\_createThreadPool creates a new thread pool with a given number of threads.

`  `Note that the lifetime of such pool must exist while being used.

`  `ZSTD\_CCtx\_refThreadPool assigns a thread pool to a context (use NULL argument value

`  `to use an internal thread pool).

<a name="_page15_x32.00_y741.50"></a>  ZSTD\_freeThreadPool frees a thread pool, accepts NULL pointer.

**Advanced compression functions**

**ZSTDLIB\_STATIC\_API ZSTD\_CDict\* ZSTD\_createCDict\_byReference(const void\* dictBuffer, size\_t dictSize, int compressionLevel);**

`  `Create a digested dictionary for compression

`  `Dictionary content is just referenced, not duplicated.

`  `As a consequence, `dictBuffer` \*\*must\*\* outlive CDict,

`  `and its content must remain unmodified throughout the lifetime of CDict.

`  `note: equivalent to ZSTD\_createCDict\_advanced(), with dictLoadMethod==ZSTD\_dlm\_byRef 

**ZSTDLIB\_STATIC\_API ZSTD\_compressionParameters ZSTD\_getCParams(int compressionLevel, unsigned long long estimatedSrcSize, size\_t dictSize);**

` `@return ZSTD\_compressionParameters structure for a selected compression level and estimated srcSize.  `estimatedSrcSize` value is optional, select 0 if not known 

**ZSTDLIB\_STATIC\_API ZSTD\_parameters ZSTD\_getParams(int compressionLevel, unsigned long long estimatedSrcSize, size\_t dictSize);**

`  `same as ZSTD\_getCParams(), but @return a full `ZSTD\_parameters` object instead of sub-component `ZSTD\_compressionParameters`.   All fields of `ZSTD\_frameParameters` are set to default : contentSize=1, checksum=0, noDictID=0 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_checkCParams(ZSTD\_compressionParameters params);**

`  `Ensure param values remain within authorized range.

` `@return 0 on success, or an error code (can be checked with ZSTD\_isError()) 

**ZSTDLIB\_STATIC\_API ZSTD\_compressionParameters ZSTD\_adjustCParams(ZSTD\_compressionParameters cPar, unsigned long long srcSize, size\_t dictSize**

`  `optimize params for a given `srcSize` and `dictSize`.

` ``srcSize` can be unknown, in which case use ZSTD\_CONTENTSIZE\_UNKNOWN.

` ``dictSize` must be `0` when there is no dictionary.

`  `cPar can be invalid : all parameters will be clamped within valid range in the @return struct.   This function never fails (wide contract) 

**ZSTD\_DEPRECATED("use ZSTD\_compress2") size\_t ZSTD\_compress\_advanced(ZSTD\_CCtx\* cctx,**

`                              `**void\* dst, size\_t dstCapacity,                         const void\* src, size\_t srcSize,**

`                        `**const void\* dict,size\_t dictSize,**

`                              `**ZSTD\_parameters params);**

`  `Note : this function is now DEPRECATED.

`         `It can be replaced by ZSTD\_compress2(), in combination with ZSTD\_CCtx\_setParameter() and other parameter setters.   This prototype will generate compilation warnings. 

**ZSTD\_DEPRECATED("use ZSTD\_compress2 with ZSTD\_CCtx\_loadDictionary") size\_t ZSTD\_compress\_usingCDict\_advanced(ZSTD\_CCtx\* cctx,**

`                                  `**void\* dst, size\_t dstCapacity,**

`                            `**const void\* src, size\_t srcSize,**

`                            `**const ZSTD\_CDict\* cdict,**

`                                  `**ZSTD\_frameParameters fParams);**

`  `Note : this function is now DEPRECATED.

`         `It can be replaced by ZSTD\_compress2(), in combination with ZSTD\_CCtx\_loadDictionary() and other parameter setters.   This prototype will generate compilation warnings. 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtx\_loadDictionary\_byReference(ZSTD\_CCtx\* cctx, const void\* dict, size\_t dictSize);**

`  `Same as ZSTD\_CCtx\_loadDictionary(), but dictionary content is referenced, instead of being copied into CCtx.   It saves some memory, but also requires that `dict` outlives its usage within `cctx` 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtx\_loadDictionary\_advanced(ZSTD\_CCtx\* cctx, const void\* dict, size\_t dictSize, ZSTD\_dictLoadMethod\_e dictLoa**

`  `Same as ZSTD\_CCtx\_loadDictionary(), but gives finer control over

`  `how to load the dictionary (by copy ? by reference ?)

`  `and how to interpret it (automatic ? force raw mode ? full mode only ?) 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtx\_refPrefix\_advanced(ZSTD\_CCtx\* cctx, const void\* prefix, size\_t prefixSize, ZSTD\_dictContentType\_e dictCon**

`  `Same as ZSTD\_CCtx\_refPrefix(), but gives finer control over

`  `how to interpret prefix content (automatic ? force raw mode (default) ? full mode only ?) 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtx\_getParameter(const ZSTD\_CCtx\* cctx, ZSTD\_cParameter param, int\* value);**

`  `Get the requested compression parameter value, selected by enum ZSTD\_cParameter,   and store it into int\* value.

` `@return : 0, or an error code (which can be tested with ZSTD\_isError()).

**ZSTDLIB\_STATIC\_API ZSTD\_CCtx\_params\* ZSTD\_createCCtxParams(void); ZSTDLIB\_STATIC\_API size\_t ZSTD\_freeCCtxParams(ZSTD\_CCtx\_params\* params);**  /\* accept NULL pointer \*/

`  `Quick howto :

- ZSTD\_createCCtxParams() : Create a ZSTD\_CCtx\_params structure
- ZSTD\_CCtxParams\_setParameter() : Push parameters one by one into

`                                     `an existing ZSTD\_CCtx\_params structure.                                      This is similar to                                      ZSTD\_CCtx\_setParameter().

- ZSTD\_CCtx\_setParametersUsingCCtxParams() : Apply parameters to

`                                    `an existing CCtx.

`                                    `These parameters will be applied to

`                                    `all subsequent frames.

- ZSTD\_compressStream2() : Do compression using the CCtx.
- ZSTD\_freeCCtxParams() : Free the memory, accept NULL pointer.

`  `This can be used with ZSTD\_estimateCCtxSize\_advanced\_usingCCtxParams()   for static allocation of CCtx for single-threaded compression.

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtxParams\_reset(ZSTD\_CCtx\_params\* params);**   Reset params to default values.

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtxParams\_init(ZSTD\_CCtx\_params\* cctxParams, int compressionLevel);**

`  `Initializes the compression parameters of cctxParams according to

`  `compression level. All other parameters are reset to their default values.

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtxParams\_init\_advanced(ZSTD\_CCtx\_params\* cctxParams, ZSTD\_parameters params);**

`  `Initializes the compression and frame parameters of cctxParams according to   params. All other parameters are reset to their default values.

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtxParams\_setParameter(ZSTD\_CCtx\_params\* params, ZSTD\_cParameter param, int value);**

`  `Similar to ZSTD\_CCtx\_setParameter.

`  `Set one compression parameter, selected by enum ZSTD\_cParameter.

`  `Parameters must be applied to a ZSTD\_CCtx using   ZSTD\_CCtx\_setParametersUsingCCtxParams().

` `@result : a code representing success or failure (which can be tested with            ZSTD\_isError()).

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtxParams\_getParameter(const ZSTD\_CCtx\_params\* params, ZSTD\_cParameter param, int\* value);**

` `Similar to ZSTD\_CCtx\_getParameter.

` `Get the requested value of one compression parameter, selected by enum ZSTD\_cParameter.  @result : 0, or an error code (which can be tested with ZSTD\_isError()).

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_CCtx\_setParametersUsingCCtxParams(         ZSTD\_CCtx\* cctx, const ZSTD\_CCtx\_params\* params);**

`  `Apply a set of ZSTD\_CCtx\_params to the compression context.

`  `This can be done even after compression is started,

`    `if nbWorkers==0, this will have no impact until a new compression is started.

`    `if nbWorkers>=1, new parameters will be picked up at next job,

`       `with a few restrictions (windowLog, pledgedSrcSize, nbWorkers, jobSize, and overlapLog are not updated).

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_compressStream2\_simpleArgs (**

`                `**ZSTD\_CCtx\* cctx,**

`                `**void\* dst, size\_t dstCapacity, size\_t\* dstPos,           const void\* src, size\_t srcSize, size\_t\* srcPos,**

`                `**ZSTD\_EndDirective endOp);**

`  `Same as ZSTD\_compressStream2(),

`  `but using only integral types as arguments.

`  `This variant might be helpful for binders from dynamic languages

`  `which have troubles handling structures containing memory pointers.

<a name="_page17_x32.00_y699.50"></a>**Advanced decompression functions**

**ZSTDLIB\_STATIC\_API unsigned ZSTD\_isFrame(const void\* buffer, size\_t size);**

`  `Tells if the content of `buffer` starts with a valid Frame Identifier.

`  `Note : Frame Identifier is 4 bytes. If `size < 4`, @return will always be 0.

`  `Note 2 : Legacy Frame Identifiers are considered valid only if Legacy Support is enabled.

`  `Note 3 : Skippable Frame Identifiers are considered valid. 

**ZSTDLIB\_STATIC\_API ZSTD\_DDict\* ZSTD\_createDDict\_byReference(const void\* dictBuffer, size\_t dictSize);**

`  `Create a digested dictionary, ready to start decompression operation without startup delay.   Dictionary content is referenced, and therefore stays in dictBuffer.

`  `It is important that dictBuffer outlives DDict,

`  `it must remain read accessible throughout the lifetime of DDict 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_DCtx\_loadDictionary\_byReference(ZSTD\_DCtx\* dctx, const void\* dict, size\_t dictSize);**

`  `Same as ZSTD\_DCtx\_loadDictionary(),

`  `but references `dict` content instead of copying it into `dctx`.

`  `This saves memory if `dict` remains around.,

`  `However, it's imperative that `dict` remains accessible (and unmodified) while being used, so it must outlive decompression. 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_DCtx\_loadDictionary\_advanced(ZSTD\_DCtx\* dctx, const void\* dict, size\_t dictSize, ZSTD\_dictLoadMethod\_e dictLoa**

`  `Same as ZSTD\_DCtx\_loadDictionary(),

`  `but gives direct control over

`  `how to load the dictionary (by copy ? by reference ?)

`  `and how to interpret it (automatic ? force raw mode ? full mode only ?). 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_DCtx\_refPrefix\_advanced(ZSTD\_DCtx\* dctx, const void\* prefix, size\_t prefixSize, ZSTD\_dictContentType\_e dictCon**

`  `Same as ZSTD\_DCtx\_refPrefix(), but gives finer control over

`  `how to interpret prefix content (automatic ? force raw mode (default) ? full mode only ?) 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_DCtx\_setMaxWindowSize(ZSTD\_DCtx\* dctx, size\_t maxWindowSize);**

`  `Refuses allocating internal buffers for frames requiring a window size larger than provided limit.

`  `This protects a decoder context from reserving too much memory for itself (potential attack scenario).

`  `This parameter is only useful in streaming mode, since no internal buffer is allocated in single-pass mode.   By default, a decompression context accepts all window sizes <= (1 << ZSTD\_WINDOWLOG\_LIMIT\_DEFAULT)

` `@return : 0, or an error code (which can be tested using ZSTD\_isError()).

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_DCtx\_getParameter(ZSTD\_DCtx\* dctx, ZSTD\_dParameter param, int\* value);**

`  `Get the requested decompression parameter value, selected by enum ZSTD\_dParameter,   and store it into int\* value.

` `@return : 0, or an error code (which can be tested with ZSTD\_isError()).

**ZSTD\_DEPRECATED("use ZSTD\_DCtx\_setParameter() instead")**

**size\_t ZSTD\_DCtx\_setFormat(ZSTD\_DCtx\* dctx, ZSTD\_format\_e format);**

`  `This function is REDUNDANT. Prefer ZSTD\_DCtx\_setParameter().

`  `Instruct the decoder context about what kind of data to decode next.

`  `This instruction is mandatory to decode data without a fully-formed header,   such ZSTD\_f\_zstd1\_magicless for example.

` `@return : 0, or an error code (which can be tested using ZSTD\_isError()). 

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_decompressStream\_simpleArgs (**

`                `**ZSTD\_DCtx\* dctx,**

`                `**void\* dst, size\_t dstCapacity, size\_t\* dstPos,           const void\* src, size\_t srcSize, size\_t\* srcPos);**

`  `Same as ZSTD\_decompressStream(),

`  `but using only integral types as arguments.

`  `This can be helpful for binders from dynamic languages

`  `which have troubles handling structures containing memory pointers.

<a name="_page18_x32.00_y631.50"></a>**Advanced streaming functions**

`  `Warning : most of these functions are now redundant with the Advanced API.   Once Advanced API reaches "stable" status,

`  `redundant functions will be deprecated, and then at some point removed.

**Advanced Streaming compression functions**

**ZSTD\_DEPRECATED("use ZSTD\_CCtx\_reset, see zstd.h for detailed instructions") size\_t ZSTD\_initCStream\_srcSize(ZSTD\_CStream\* zcs,**

`             `**int compressionLevel,**

`             `**unsigned long long pledgedSrcSize);**

` `This function is DEPRECATED, and equivalent to:

`     `ZSTD\_CCtx\_reset(zcs, ZSTD\_reset\_session\_only);

`     `ZSTD\_CCtx\_refCDict(zcs, NULL); // clear the dictionary (if any)

`     `ZSTD\_CCtx\_setParameter(zcs, ZSTD\_c\_compressionLevel, compressionLevel);      ZSTD\_CCtx\_setPledgedSrcSize(zcs, pledgedSrcSize);

` `pledgedSrcSize must be correct. If it is not known at init time, use

` `ZSTD\_CONTENTSIZE\_UNKNOWN. Note that, for compatibility with older programs,  "0" also disables frame content size field. It may be enabled in the future.  This prototype will generate compilation warnings.

**ZSTD\_DEPRECATED("use ZSTD\_CCtx\_reset, see zstd.h for detailed instructions") size\_t ZSTD\_initCStream\_usingDict(ZSTD\_CStream\* zcs,**

`         `**const void\* dict, size\_t dictSize,**

`               `**int compressionLevel);**

` `This function is DEPRECATED, and is equivalent to:

`     `ZSTD\_CCtx\_reset(zcs, ZSTD\_reset\_session\_only);

`     `ZSTD\_CCtx\_setParameter(zcs, ZSTD\_c\_compressionLevel, compressionLevel);      ZSTD\_CCtx\_loadDictionary(zcs, dict, dictSize);

` `Creates of an internal CDict (incompatible with static CCtx), except if

` `dict == NULL or dictSize < 8, in which case no dict is used.

` `Note: dict is loaded with ZSTD\_dct\_auto (treated as a full zstd dictionary if

` `it begins with ZSTD\_MAGIC\_DICTIONARY, else as raw content) and ZSTD\_dlm\_byCopy.  This prototype will generate compilation warnings.

**ZSTD\_DEPRECATED("use ZSTD\_CCtx\_reset, see zstd.h for detailed instructions") size\_t ZSTD\_initCStream\_advanced(ZSTD\_CStream\* zcs,**

`        `**const void\* dict, size\_t dictSize,**

`              `**ZSTD\_parameters params,**

`              `**unsigned long long pledgedSrcSize);**

` `This function is DEPRECATED, and is approximately equivalent to:

`     `ZSTD\_CCtx\_reset(zcs, ZSTD\_reset\_session\_only);

`     `// Pseudocode: Set each zstd parameter and leave the rest as-is.      for ((param, value) : params) {

`         `ZSTD\_CCtx\_setParameter(zcs, param, value);

`     `}

`     `ZSTD\_CCtx\_setPledgedSrcSize(zcs, pledgedSrcSize);

`     `ZSTD\_CCtx\_loadDictionary(zcs, dict, dictSize);

` `dict is loaded with ZSTD\_dct\_auto and ZSTD\_dlm\_byCopy.

` `pledgedSrcSize must be correct.

` `If srcSize is not known at init time, use value ZSTD\_CONTENTSIZE\_UNKNOWN.  This prototype will generate compilation warnings.

**ZSTD\_DEPRECATED("use ZSTD\_CCtx\_reset and ZSTD\_CCtx\_refCDict, see zstd.h for detailed instructions") size\_t ZSTD\_initCStream\_usingCDict(ZSTD\_CStream\* zcs, const ZSTD\_CDict\* cdict);**

` `This function is DEPRECATED, and equivalent to:

`     `ZSTD\_CCtx\_reset(zcs, ZSTD\_reset\_session\_only);      ZSTD\_CCtx\_refCDict(zcs, cdict);

` `note : cdict will just be referenced, and must outlive compression session  This prototype will generate compilation warnings.

**ZSTD\_DEPRECATED("use ZSTD\_CCtx\_reset and ZSTD\_CCtx\_refCDict, see zstd.h for detailed instructions") size\_t ZSTD\_initCStream\_usingCDict\_advanced(ZSTD\_CStream\* zcs,**

`                   `**const ZSTD\_CDict\* cdict,**

`                         `**ZSTD\_frameParameters fParams,**

`                         `**unsigned long long pledgedSrcSize);**

`   `This function is DEPRECATED, and is approximately equivalent to:

`     `ZSTD\_CCtx\_reset(zcs, ZSTD\_reset\_session\_only);

`     `// Pseudocode: Set each zstd frame parameter and leave the rest as-is.      for ((fParam, value) : fParams) {

`         `ZSTD\_CCtx\_setParameter(zcs, fParam, value);

`     `}

`     `ZSTD\_CCtx\_setPledgedSrcSize(zcs, pledgedSrcSize);

`     `ZSTD\_CCtx\_refCDict(zcs, cdict);

` `same as ZSTD\_initCStream\_usingCDict(), with control over frame parameters.  pledgedSrcSize must be correct. If srcSize is not known at init time, use  value ZSTD\_CONTENTSIZE\_UNKNOWN.

` `This prototype will generate compilation warnings.

**ZSTD\_DEPRECATED("use ZSTD\_CCtx\_reset, see zstd.h for detailed instructions") size\_t ZSTD\_resetCStream(ZSTD\_CStream\* zcs, unsigned long long pledgedSrcSize);**

` `This function is DEPRECATED, and is equivalent to:

`     `ZSTD\_CCtx\_reset(zcs, ZSTD\_reset\_session\_only);

`     `ZSTD\_CCtx\_setPledgedSrcSize(zcs, pledgedSrcSize);

` `Note: ZSTD\_resetCStream() interprets pledgedSrcSize == 0 as ZSTD\_CONTENTSIZE\_UNKNOWN, but

`       `ZSTD\_CCtx\_setPledgedSrcSize() does not do the same, so ZSTD\_CONTENTSIZE\_UNKNOWN must be        explicitly specified.

`  `start a new frame, using same parameters from previous frame.

`  `This is typically useful to skip dictionary loading stage, since it will re-use it in-place.

`  `Note that zcs must be init at least once before using ZSTD\_resetCStream().

`  `If pledgedSrcSize is not known at reset time, use macro ZSTD\_CONTENTSIZE\_UNKNOWN.

`  `If pledgedSrcSize > 0, its value must be correct, as it will be written in header, and controlled at the end.

`  `For the time being, pledgedSrcSize==0 is interpreted as "srcSize unknown" for compatibility with older programs,   but it will change to mean "empty" in future version, so use macro ZSTD\_CONTENTSIZE\_UNKNOWN instead.

` `@return : 0, or an error code (which can be tested using ZSTD\_isError())

`  `This prototype will generate compilation warnings.

**typedef struct {**

`    `**unsigned long long ingested;**   /\* nb input bytes read and buffered \*/

`    `**unsigned long long consumed;**   /\* nb input bytes actually compressed \*/

`    `**unsigned long long produced;**   /\* nb of compressed bytes generated and buffered \*/     **unsigned long long flushed;**    /\* nb of compressed bytes flushed : not provided; can be tracked from caller side \*/     **unsigned currentJobID;**         /\* MT only : latest started job nb \*/

`    `**unsigned nbActiveWorkers;**      /\* MT only : nb of workers actively compressing at probe time \*/

**} ZSTD\_frameProgression;**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_toFlushNow(ZSTD\_CCtx\* cctx);**

`  `Tell how many bytes are ready to be flushed immediately.

`  `Useful for multithreading scenarios (nbWorkers >= 1).

`  `Probe the oldest active job, defined as oldest job not yet entirely flushed,

`  `and check its output buffer.

` `@return : amount of data stored in oldest job and ready to be flushed immediately.   if @return == 0, it means either :

+ there is no active job (could be checked with ZSTD\_frameProgression()), or
+ oldest job is still actively compressing data,

`    `but everything it has produced has also been flushed so far,

`    `therefore flush speed is limited by production speed of oldest job

`    `irrespective of the speed of concurrent (and newer) jobs.

**Advanced Streaming decompression functions**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_initDStream\_usingDict(ZSTD\_DStream\* zds, const void\* dict, size\_t dictSize);**

`     `ZSTD\_DCtx\_reset(zds, ZSTD\_reset\_session\_only);      ZSTD\_DCtx\_loadDictionary(zds, dict, dictSize);

` `note: no dictionary will be used if dict == NULL or dictSize < 8

` `Note : this prototype will be marked as deprecated and generate compilation warnings on reaching v1.5.x

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_initDStream\_usingDDict(ZSTD\_DStream\* zds, const ZSTD\_DDict\* ddict);**

`     `ZSTD\_DCtx\_reset(zds, ZSTD\_reset\_session\_only);      ZSTD\_DCtx\_refDDict(zds, ddict);

` `note : ddict is referenced, it must outlive decompression session

` `Note : this prototype will be marked as deprecated and generate compilation warnings on reaching v1.5.x

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_resetDStream(ZSTD\_DStream\* zds);**      ZSTD\_DCtx\_reset(zds, ZSTD\_reset\_session\_only);

` `re-use decompression parameters from previous init; saves dictionary loading

` `Note : this prototype will be marked as deprecated and generate compilation warnings on reaching v1.5.x

<a name="_page20_x32.00_y675.50"></a>**Buffer-less and synchronous inner streaming functions**

`  `This is an advanced API, giving full control over buffer management, for users which need direct control over memory.   But it's also a complex one, with several restrictions, documented below.

<a name="_page20_x32.00_y753.50"></a>  Prefer normal streaming API for an easier experience.

**Buffer-less streaming compression (synchronous mode)**

`  `A ZSTD\_CCtx object is required to track streaming operations.

`  `Use ZSTD\_createCCtx() / ZSTD\_freeCCtx() to manage resource.

`  `ZSTD\_CCtx object can be re-used multiple times within successive compression operations.

`  `Start by initializing a context.

`  `Use ZSTD\_compressBegin(), or ZSTD\_compressBegin\_usingDict() for dictionary compression.

`  `It's also possible to duplicate a reference context which has already been initialized, using ZSTD\_copyCCtx()

`  `Then, consume your input using ZSTD\_compressContinue().

`  `There are some important considerations to keep in mind when using this advanced function :

- ZSTD\_compressContinue() has no internal buffer. It uses externally provided buffers only.
- Interface is synchronous : input is consumed entirely and produces 1+ compressed blocks.
- Caller must ensure there is enough space in `dst` to store compressed data under worst case scenario.

`    `Worst case evaluation is provided by ZSTD\_compressBound().

`    `ZSTD\_compressContinue() doesn't guarantee recover after a failed compression.

- ZSTD\_compressContinue() presumes prior input \*\*\*is still accessible and unmodified\*\*\* (up to maximum distance size, see WindowLog).

`    `It remembers all previous contiguous blocks, plus one separated memory segment (which can itself consists of multiple contiguous blocks)

- ZSTD\_compressContinue() detects that prior input has been overwritten when `src` buffer overlaps.

`    `In which case, it will "discard" the relevant memory section from its history.

`  `Finish a frame with ZSTD\_compressEnd(), which will write the last block(s) and optional checksum.

`  `It's possible to use srcSize==0, in which case, it will write a final empty block to end the frame.   Without last block mark, frames are considered unfinished (hence corrupted) by compliant decoders.

`  ``ZSTD\_CCtx` object can be re-used (ZSTD\_compressBegin()) to compress again.

**Buffer-less streaming compression functions**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_compressBegin(ZSTD\_CCtx\* cctx, int compressionLevel);**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_compressBegin\_usingDict(ZSTD\_CCtx\* cctx, const void\* dict, size\_t dictSize, int compressionLevel); ZSTDLIB\_STATIC\_API size\_t ZSTD\_compressBegin\_usingCDict(ZSTD\_CCtx\* cctx, const ZSTD\_CDict\* cdict);** /\*\*< note: fails if cdict==NULL \*/ **ZSTDLIB\_STATIC\_API size\_t ZSTD\_copyCCtx(ZSTD\_CCtx\* cctx, const ZSTD\_CCtx\* preparedCCtx, unsigned long long pledgedSrcSize);** /\*\*<  note: if pl

**size\_t ZSTD\_compressBegin\_advanced(ZSTD\_CCtx\* cctx, const void\* dict, size\_t dictSize, ZSTD\_parameters params, unsigned long long pledgedSrcS**

<a name="_page21_x32.00_y351.50"></a>**Buffer-less streaming decompression (synchronous mode)**

`  `A ZSTD\_DCtx object is required to track streaming operations.   Use ZSTD\_createDCtx() / ZSTD\_freeDCtx() to manage it.

`  `A ZSTD\_DCtx object can be re-used multiple times.

`  `First typical operation is to retrieve frame parameters, using ZSTD\_getFrameHeader().

`  `Frame header is extracted from the beginning of compressed frame, so providing only the frame's beginning is enough.   Data fragment must be large enough to ensure successful decoding.

` ``ZSTD\_frameHeaderSize\_max` bytes is guaranteed to always be large enough.

`  `@result : 0 : successful decoding, the `ZSTD\_frameHeader` structure is correctly filled.

`           `>0 : `srcSize` is too small, please provide at least @result bytes on next attempt.

`           `errorCode, which can be tested using ZSTD\_isError().

`  `It fills a ZSTD\_frameHeader structure with important information to correctly decode the frame,

`  `such as the dictionary ID, content size, or maximum back-reference distance (`windowSize`).

`  `Note that these values could be wrong, either because of data corruption, or because a 3rd party deliberately spoofs false information.   As a consequence, check that values remain within valid application range.

`  `For example, do not allocate memory blindly, check that `windowSize` is within expectation.

`  `Each application can set its own limits, depending on local restrictions.

`  `For extended interoperability, it is recommended to support `windowSize` of at least 8 MB.

`  `ZSTD\_decompressContinue() needs previous data blocks during decompression, up to `windowSize` bytes.

`  `ZSTD\_decompressContinue() is very sensitive to contiguity,

`  `if 2 blocks don't follow each other, make sure that either the compressor breaks contiguity at the same place,   or that previous contiguous segment is large enough to properly handle maximum back-reference distance.

`  `There are multiple ways to guarantee this condition.

`  `The most memory efficient way is to use a round buffer of sufficient size.

`  `Sufficient size is determined by invoking ZSTD\_decodingBufferSize\_min(),

`  `which can @return an error code if required value is too large for current system (in 32-bits mode).

`  `In a round buffer methodology, ZSTD\_decompressContinue() decompresses each block next to previous one,   up to the moment there is not enough room left in the buffer to guarantee decoding another full block,   which maximum size is provided in `ZSTD\_frameHeader` structure, field `blockSizeMax`.

`  `At which point, decoding can resume from the beginning of the buffer.

`  `Note that already decoded data stored in the buffer should be flushed before being overwritten.

`  `There are alternatives possible, for example using two or more buffers of size `windowSize` each, though they consume more memory.

`  `Finally, if you control the compression process, you can also ignore all buffer size rules,   as long as the encoder and decoder progress in "lock-step",

`  `aka use exactly the same buffer sizes, break contiguity at the same place, etc.

`  `Once buffers are setup, start decompression, with ZSTD\_decompressBegin().

`  `If decompression requires a dictionary, use ZSTD\_decompressBegin\_usingDict() or ZSTD\_decompressBegin\_usingDDict().

`  `Then use ZSTD\_nextSrcSizeToDecompress() and ZSTD\_decompressContinue() alternatively.

`  `ZSTD\_nextSrcSizeToDecompress() tells how many bytes to provide as 'srcSize' to ZSTD\_decompressContinue().   ZSTD\_decompressContinue() requires this \_exact\_ amount of bytes, or it will fail.

` `@result of ZSTD\_decompressContinue() is the number of bytes regenerated within 'dst' (necessarily <= dstCapacity).   It can be zero : it just means ZSTD\_decompressContinue() has decoded some metadata item.

`  `It can also be an error code, which can be tested with ZSTD\_isError().

`  `A frame is fully decoded when ZSTD\_nextSrcSizeToDecompress() returns zero.   Context can then be reset to start a new decompression.

`  `Note : it's possible to know if next input to present is a header or a block, using ZSTD\_nextInputType().   This information is not required to properly decode a frame.

`  `== Special case : skippable frames 

`  `Skippable frames allow integration of user-defined data into a flow of concatenated frames.

`  `Skippable frames will be ignored (skipped) by decompressor.

`  `The format of skippable frames is as follows :

1) Skippable frame ID - 4 Bytes, Little endian format, any value from 0x184D2A50 to 0x184D2A5F
1) Frame Size - 4 Bytes, Little endian format, unsigned 32-bits
1) Frame Content - any content (User Data) of length equal to Frame Size

`  `For skippable frames ZSTD\_getFrameHeader() returns zfhPtr->frameType==ZSTD\_skippableFrame.

`  `For skippable frames ZSTD\_decompressContinue() always returns 0 : it only skips the content.

**Buffer-less streaming decompression functions**

**typedef enum { ZSTD\_frame, ZSTD\_skippableFrame } ZSTD\_frameType\_e;**

**typedef struct {**

`    `**unsigned long long frameContentSize;** /\* if == ZSTD\_CONTENTSIZE\_UNKNOWN, it means this field is not available. 0 means "empty" \*/     **unsigned long long windowSize;**       /\* can be very large, up to <= frameContentSize \*/

`    `**unsigned blockSizeMax;**

`    `**ZSTD\_frameType\_e frameType;**          /\* if == ZSTD\_skippableFrame, frameContentSize is the size of skippable content \*/

`    `**unsigned headerSize;**

`    `**unsigned dictID;**

`    `**unsigned checksumFlag;**

**} ZSTD\_frameHeader;**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_getFrameHeader(ZSTD\_frameHeader\* zfhPtr, const void\* src, size\_t srcSize);**   /\*\*< doesn't consume input \*/

/\*! ZSTD\_getFrameHeader\_advanced() :

* **same as ZSTD\_getFrameHeader(),**
* **with added capability to select a format (like ZSTD\_f\_zstd1\_magicless) \*/**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_getFrameHeader\_advanced(ZSTD\_frameHeader\* zfhPtr, const void\* src, size\_t srcSize, ZSTD\_format\_e format); ZSTDLIB\_STATIC\_API size\_t ZSTD\_decodingBufferSize\_min(unsigned long long windowSize, unsigned long long frameContentSize);**  /\*\*< when frame c

`  `decode Frame Header, or requires larger `srcSize`.

` `@return : 0, `zfhPtr` is correctly filled,

`          `>0, `srcSize` is too small, value is wanted `srcSize` amount,            or an error code, which can be tested using ZSTD\_isError() 

**typedef enum { ZSTDnit\_frameHeader, ZSTDnit\_blockHeader, ZSTDnit\_block, ZSTDnit\_lastBlock, ZSTDnit\_checksum, ZSTDnit\_skippableFrame } ZSTD\_nex**

<a name="_page22_x32.00_y423.50"></a>**Block level API**

`    `Frame metadata cost is typically ~12 bytes, which can be non-negligible for very small blocks (< 100 bytes).

`    `But users will have to take in charge needed metadata to regenerate data, such as compressed and content sizes.

`    `A few rules to respect :

- Compressing and decompressing require a context structure
  - Use ZSTD\_createCCtx() and ZSTD\_createDCtx()
- It is necessary to init context before starting
  - compression : any ZSTD\_compressBegin\*() variant, including with dictionary
  - decompression : any ZSTD\_decompressBegin\*() variant, including with dictionary
  - copyCCtx() and copyDCtx() can be used too
- Block size is limited, it must be <= ZSTD\_getBlockSize() <= ZSTD\_BLOCKSIZE\_MAX == 128 KB
+ If input is larger than a block size, it's necessary to split input data into multiple blocks
+ For inputs larger than a single block, consider using regular ZSTD\_compress() instead.

`        `Frame metadata is not that costly, and quickly becomes negligible as source size grows larger than a block.

- When a block is considered not compressible enough, ZSTD\_compressBlock() result will be 0 (zero) !

`      `===> In which case, nothing is produced into `dst` !

+ User \_\_must\_\_ test for such outcome and deal directly with uncompressed data
+ A block cannot be declared incompressible if ZSTD\_compressBlock() return value was != 0.

`        `Doing so would mess up with statistics history, leading to potential data corruption.

+ ZSTD\_decompressBlock() \_doesn't accept uncompressed data as input\_ !!
+ In case of multiple successive blocks, should some of them be uncompressed,

`        `decoder must be informed of their existence in order to follow proper history.

`        `Use ZSTD\_insertBlock() for such a case.

**Raw zstd block functions**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_getBlockSize   (const ZSTD\_CCtx\* cctx);**

**ZSTDLIB\_STATIC\_API size\_t ZSTD\_compressBlock  (ZSTD\_CCtx\* cctx, void\* dst, size\_t dstCapacity, const void\* src, size\_t srcSize); ZSTDLIB\_STATIC\_API size\_t ZSTD\_decompressBlock(ZSTD\_DCtx\* dctx, void\* dst, size\_t dstCapacity, const void\* src, size\_t srcSize); ZSTDLIB\_STATIC\_API size\_t ZSTD\_insertBlock    (ZSTD\_DCtx\* dctx, const void\* blockStart, size\_t blockSize);**  /\*\*< insert uncompressed block in

[ref1]: Aspose.Words.9ddb20c2-f748-4660-86d0-d1402aeef992.001.png
