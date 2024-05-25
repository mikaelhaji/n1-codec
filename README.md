# The N1 Codec

**An implementation of _<ins>24+ lossless compression algorithms_</ins> from dictionary-based codecs to specialized audio codecs tailored for Neuralink's N1 Implant, achieving compression ratios up to a _<ins>high of 3.11x._</ins>**

The [Neuralink Compression Challenge](https://content.neuralink.com/compression-challenge/README.html) is a challenge announced by [Bliss Chapman](https://x.com/chapman_bliss/status/1791895723744837905) aimed at drastically reducing the data bandwidth requirements for the N1 implant without losing a single sample. This implant, situated in the motor cortex of a non-human primate, generates around 200 Mbps of data from 1024 electrodes, each sampling at 20 kHz with 10-bit resolution. 

To transmit this data wirelessly in real-time, a _<ins>compression ratio greater than 200x</ins>_ is necessary, all while operating under stringent conditions of _<ins>less than 1 ms latency</ins>_ and <ins>_power consumption below 10 mW_</ins>.

**The goal of this project was to deterministically get a sense of how well-established lossless compression techniques could effectively compress this unique type of data.**


> [!IMPORTANT]
>
> **There were 6 groups that these algorithms were categorized in based on their core methodologies and performance characteristics:**
>
> 1. _Dictionary-Based Codecs (zstd, lz4, lz4hc, gzip, zlib, bz2 etc.)_
> 2. _Predictive Codecs (delta etc.)_
> 3. _Entropy Codecs (huffman, arithmetic etc.)_
> 4. _Run-Length Encoding Codecs_
> 5. _Specialized Audio Codecs (wavpack etc.)_
> 6. _Blosc Hybrid Codecs_
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







### Key Metrics Overview
Presentation of the key metrics used to evaluate compression performance, such as compression ratio, decompression speed, entropy changes, and any error metrics that were tracked.

Compression Ratio (CR), computed by dividing the number of bytes in the original data file by the number
of bytes written to disk after compression. The higher the compression ratio, the lower disk space the com225 pressed data will occupy. For example, a CR of 2 implies that the compressed data occupies half of the disk
space (50%) compared to uncompressed data, a CR of 4 occupies 25% of the disk space, and so on.
• Compression speed (in units of xRT, or “times real-time”), computed by dividing the time needed to compress an entire recording divided by the original recording duration (see duration in Table 1).
• Decompression speed (in xRT), computed by dividing the time needed to decompress all channels (384) in
230 a 10 s time range by 10.



## Algorithms Deployed
### Dictionary-Based Codecs
- **Performance Analysis**: Charts and graphs that compare the compression ratios and speeds of each dictionary-based codec.
- **Best Use Case Scenarios**: Analysis of the types of data or situations in which these algorithms excel.

### Predictive Coding
- **Detailed Analysis**: Insights into the predictive mechanisms of these algorithms and how they are leveraged for neural data compression.

### Entropy Coders
- **Entropy Analysis**: Visuals displaying the entropy of data before and after compression, highlighting the effectiveness of these coders in reducing data redundancy.
- **In-depth Comparison**: Explanation of the factors leading to the quick invalidation of certain models, providing a deeper understanding of their limitations.

### Run-Length Encoding (RLE)
- **Use Case Efficiency**: Detailed discussion on the simplicity and efficiency of RLE in specific data scenarios.

### Specialized Audio Codecs
- **Adaptability to Neural Data**: Exploration of how these codecs, typically used in audio compression, can be adapted for compressing neural data, including potential benefits and drawbacks.

### Blosc Framework
- **Multicore Efficiency**: Benchmark data showing the performance of Blosc in multicore processing environments, emphasizing its scalability and efficiency.

## Next Steps
### Future Directions
Outline of potential improvements, further research areas, and next steps for advancing the project, including algorithm optimization and exploration of new compression techniques.

### Collaboration Opportunities
An invitation for collaboration, encouraging contributions, feedback, and suggestions from the community and other researchers to help advance the project.







 Lossless compression reduces the size of a file without removing any information, meaning the
original data will be perfectly intact following decompression. The final size of the compressed file depends
45 on the randomness or redundancy of the data it contains (a file with more random/unpredictable values will be
less compressible). Different lossless compressors employ different strategies for eliminating redundancy, but so
far there has been no systematic comparison of how they interact with continuously sampled electrophysiology
signals, which display high correlations across both space and time.







