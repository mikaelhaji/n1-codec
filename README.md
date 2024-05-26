# The N1 Codec

**An implementation of _<ins>24+ lossless compression algorithms_</ins> from dictionary-based codecs to specialized audio codecs tailored for Neuralink's N1 Implant, achieving compression ratios up to a _<ins>high of 3.11x._</ins>**

The [Neuralink Compression Challenge](https://content.neuralink.com/compression-challenge/README.html) is a challenge announced by [Bliss Chapman](https://x.com/chapman_bliss/status/1791895723744837905) aimed at drastically reducing the data bandwidth requirements for the N1 implant without losing a single sample. This implant, situated in the motor cortex of a non-human primate, generates around 200 Mbps of data from 1024 electrodes, each sampling at 20 kHz with 10-bit resolution. 

To transmit this data wirelessly in real-time, a _<ins>compression ratio greater than 200x</ins>_ is necessary, all while operating under stringent conditions of _<ins>less than 1 ms latency</ins>_ and <ins>_power consumption below 10 mW_</ins>.

**The goal of this project was to deterministically get a sense of how well-established lossless compression techniques could effectively compress this unique type of data.**


> [!IMPORTANT]
>
> **There were 5 groups that these algorithms were categorized in based on their core methodologies and performance characteristics:**
>
> 1. _Dictionary-Based Codecs (zstd, lz4, lz4hc, gzip, zlib, bz2 etc.)_
> 2. _Predictive Codecs (delta etc.)_
> 3. _Entropy Codecs (huffman, arithmetic etc.)_
> 4. _Specialized Audio Codecs (wavpack etc.)_
> 5. _Blosc Hybrid Codecs_
>
> **Despite the common application of these algorithms in various data types, little work has been done to investigate how these compression techniques perform specifically on electrophysiology data.**

### Holistic Overview of Algorithms Deployed:
_24+ lossless compression algorithms were tested & benchmarked against each other._

![Compression_Ratios_Scatter_Plot](https://github.com/mikaelhaji/n1-codec/assets/68840767/ee2df863-3fb9-4741-bdc0-3504a4cfc202)

## Table of Contents
- [Build Instructions](#build-instructions)
  - [Repository Structure](#repository-structure)
  - [How to Run](#how-to-run)
    - [Setup Instructions](#setup-instructions)
    - [Execution Commands](#execution-commands)
- [How to Run](#how-to-run)
- [Data Analysis](#data-analysis)
- [Algorithms Deployed](#algorithms-deployed)
- [Next Steps](#next-steps)

## Build Instructions
### Repository Structure
- **Files:**
  - `encode.py`: Script for encoding the N1 wav files using the compression algorithm you pick.
  - `decode.py`: Script for decoding the compressed audio files to validate lossless compression.
  - `eval.sh`: Bash script to automate the compression and decompression process, and to calculate compression ratios.
  - `grid_search.sh`: Bash script to sweep through all the compression algorithms of your choice and record data to the `~/tests/compression_results.csv` file
  - `Makefile`:Used to build and manage symbolic links for Python encode/decode scripts, and to run evaluation scripts.
- **Directories:**
  - `~/algorithms:` Holds all the algorithm logic. If you wanted to add your own algorithm, you could add it in this directory and call it from `encode.py`.
  - `~/data:` Holds all the data (743 wav files).
  -  `~/tests:` CSV & Notebooks for unit testing.

### How to Run
#### Setup Instructions

**To install all dependencies, simply run:**
```
make install
```

> [!NOTE]
>
> **For WavPack, simply run:** <br>
> 1) Install the WavPack Library <br>
>   a) `brew install wavpack` (Mac) <br>
>   b) `sudo apt-get install wavpack` (Debian Based Systems)
> 2) Go to Home directory in repo & `cd /n1-codec/misc/wavpack-numcodecs`
> 3) Install directory: `pip install .`


### Execution Commands

#### To Evaluate a Single Algorithm's Compression:
1. Ensure that `mode = insert algo mode here` for both `encode.py` and `decode.py`
2. Run `make encode` to make the `encode` executable
3. Run `make decode` to make the `decode` executable
4. Run the `eval.sh` bash script by running `make eval`

#### To Evaluate a Series of Algorithm's Compression:
1. Ensure that `mode = sys.argv[3]` for both `encode.py` and `decode.py`
2. Run `make encode` to make the `encode` executable
3. Run `make decode` to make the `decode` executable
4. Run the `grid_results.sh` bash script by running `make grid`

## Data Analysis
The fundamental characteristics of this dataset are as follows:
- **High Throughput**: The N1 implant generates approximately 200 Mbps of data, stemming from 1024 electrodes.
- **High Sampling Rate**: Each electrode samples neural signals at 20 kHz.
- **Resolution**: The data from each electrode is quantized at 10-bit resolution.

This dataset presents substantial challenges due to its size and complexity, necessitating sophisticated compression strategies to reduce bandwidth effectively while preserving the integrity and quality of the neural signals.

### Desired Compression Ratio of 200x ....
The Neuralink Compression Challenge set a formidable goal of achieving a **200x lossless compression ratio**. This target, while theoretically appealing, presents substantial practical challenges given the **inherent noise and complexity of electrophysiological data**.

In an article a friend and I [wrote last year reviewing all of Neuralink's patents and papers](https://mikaelhaji.medium.com/a-technical-deep-dive-on-elon-musks-neuralink-in-40-mins-71e1100f54d4), we delved deep into what Neuralink had deployed in order to get the most important features from their data.

**Here's a long but insightful excerpt on the compression tactics (w. loss) that Neuralink has deployed:**

> Compression strategies predominantly involve applying thresholds to detect spikes in a specific **range, summary statistics like channel-wise averages, and/or event-based triggers off-chip**. Alternatively, information-theoretic lossless compression techniques **like PNG, TIFF, or ZIP** may be used. In some examples, the reduction in bandwidth from the compression engine can **exceed 1,000 times fewer data**. <br>
>
> These thresholds may be set on the voltage of the signal or the frequency of the signal. Low-frequency and high-frequency signals may not be valuable to the recorder and can be filtered out by the compression engine. Non-spike signals are discarded, essentially reducing the size of the data packets, and compressing the signal. For voltage-based thresholds, a technique called non-linear energy operator (NEO) may be used to automatically find a threshold that accurately detects spikes.

<p align="center">
  <img src="https://github.com/mikaelhaji/n1-codec/assets/68840767/dae26106-b609-4ee1-ae55-d7a52f5c6b9f">
</p>

> Briefly reviewing NEO, it essentially filters the signals for the periods at which there are fast frequency and amplitude changes of spikes, which can be seen as short peaks in the NEO filtered output. <br>
>
$$
\psi[x(n)] = |x(n) \cdot x(n)| - |x(n-1) \cdot x(n+1)|
$$

>
> NEO, represented by **𝝍[x(n)]**, of a signal **x(n)** can be computed as shown above. It simply compares the deviation between the signal at **n** time step and the signal at **n-1** and **n+1** time steps.

$$
\text{Thr} = C \times \frac{1}{N} \sum_{n=1}^{N} \psi[x(n)]
$$

> Furthermore, a threshold for NEO detection can be calculated as the mean of the NEO filtered output multiplied by a **factor C**. In this equation, **N** is the number of samples of the signal. **C **is found empirically and should be tested on several neural datasets beforehand to achieve the best results. <br>
>
> Both the compression engine and controller play a crucial role in throttling the amount of data being generated by each chip. Throttling allows for power and performance efficiency improvements for the N1 system. <br>
>
> Alternatively, during the Neuralink launch event, DJ Seo introduced a novel on-chip spike detection algorithm that involved directly characterizing the shape of a spike. This method is able to **compress neural data by more than 200x and only takes 900 nanoseconds to compute**, which is faster than the time it takes for the brain to realize it happened. This technique even allows for identifying different neurons from the same electrode based on shape.


### Dataset Visualization

**1/ the data is inconsistent & noisy**
<p align="center">
  <img src="https://github.com/mikaelhaji/n1-codec/assets/68840767/9cd227a0-a596-4ed6-acb0-7e379db72b84" width="85%" height="auto">
</p>

The global amplitude statistics for the WAV files are as follows:

- **Mean**: 975.1664476018635
- **Median**: 992.0
- **Standard Deviation**: 3154.619387966767
- **Skewness**: -0.009132604033709467
- **Kurtosis**: 59.332425608861676
<br>

The data exhibits substantial variability, highlighted by **a large standard deviation** indicating **wide fluctuations in signal amplitude**, and **a leptokurtic distribution with a high kurtosis value** suggesting data points are densely clustered around the mean with frequent extreme values. Despite a skewness value near zero indicating symmetry, the mode significantly diverges from the mean and median, underscoring the presence of notable outliers. This combination of statistics suggests **a highly variable dataset with a complex, outlier-influenced structure**.


**2/ mid-range spectral entropy of the data -- yet also extremely variable across files**
<br>
<p align="center">
  <img src="https://github.com/mikaelhaji/n1-codec/assets/68840767/b91f72d7-7c9d-4b0f-95a7-7bd66902bb0f" width="85%" height="auto">
</p>
<br>

The spectral entropy of the electrophysiology data **averages at 4.88**, indicating a moderately complex and unpredictable spectral distribution. The **standard deviation of 1.16** points to significant variability across files, which complicates achieving consistent compression ratios.

**3/ very noisy, random spectogram**
<p align="center">
  <img src="https://github.com/mikaelhaji/n1-codec/assets/68840767/d6a640c6-dfc8-4b51-9264-8477287b85e0" width="85%" height="auto">
</p>



## The Suite of Lossless Algorithms
### Benchmarking Metrics
The following variables were measured in order to effectively benchmark the algorithms against one another:
- **Compression Ratio (CR)**, computed by dividing the number of bytes in the original data file by the number of bytes written to disk after compression. The higher the compression ratio, the lower disk space the compressed data will occupy. For example, a CR of 2 implies that the compressed data occupies half of the disk space (50%) compared to uncompressed data, a CR of 4 occupies 25% of the disk space, and so on.
- **Compression speed** (in units of xRT, or “times real-time”), computed by dividing the time needed to compress an entire recording divided by the original recording duration.
- **Decompression speed** (in xRT), computed by dividing the time needed to decompress the data in a 5s time range by 5.

### Results

![Compression_Decompression_Comparison](https://github.com/mikaelhaji/n1-codec/assets/68840767/29ece761-2312-4506-8b9e-cef51597b66d)


The two best algorithms were huffmand .....o;iwehdblkj

### Huffman

### B2Z

### What was tried & killed

## Next Steps

### Future Directions
[]

Updates I want to make in the future to improve the design, anyone else is welcome to contribute as well:

 Add a simple cache for instructions
 Build an adapter to use GPU with Tiny Tapeout 7
 Add basic branch divergence
 Add basic memory coalescing
 Add basic pipelining
 Optimize control flow and use of registers to improve cycle time
 Write a basic graphics kernel or add simple graphics hardware to demonstrate graphics functionality
For anyone curious to play around or make a contribution, feel free to put up a PR with any improvements you'd like to add 😄



 Lossless compression reduces the size of a file without removing any information, meaning the
original data will be perfectly intact following decompression. The final size of the compressed file depends
45 on the randomness or redundancy of the data it contains (a file with more random/unpredictable values will be
less compressible). Different lossless compressors employ different strategies for eliminating redundancy, but so
far there has been no systematic comparison of how they interact with continuously sampled electrophysiology
signals, which display high correlations across both space and time.







