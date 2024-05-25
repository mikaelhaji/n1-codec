# The N1 Codec

**An implementation of _<ins>24+ lossless compression algorithms_</ins> from dictionary-based codecs to specialized audio codecs tailored for Neuralink's N1 Implant, achieving compression ratios up to a _<ins>high of 3.11x._</ins>**

The [Neuralink Compression Challenge](https://content.neuralink.com/compression-challenge/README.html) is a challenge announced by [Bliss Chapman](https://x.com/chapman_bliss/status/1791895723744837905) aimed at drastically reducing the data bandwidth requirements for the N1 implant without losing a single sample. This implant, situated in the motor cortex of a non-human primate, generates around 200 Mbps of data from 1024 electrodes, each sampling at 20 kHz with 10-bit resolution. 

To transmit this data wirelessly in real-time, a _<ins>compression ratio greater than 200x</ins>_ is necessary, all while operating under stringent conditions of _<ins>less than 1 ms latency</ins>_ and <ins>_power consumption below 10 mW_</ins>.

**The goal was to deterministically get a sense of how well-established lossless compression techniques could effectively compress this unique type of data.**


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


[INSERT OVERVIEW OF ALL COMPRESSION ALGOS HERE WITH 2-3 POINTS]


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
A detailed explanation of how the repository is organized, including directories and their contents, which will help users navigate and utilize the various scripts and data files effectively.

### How to Run
#### Setup Instructions
Comprehensive step-by-step instructions on how to set up the necessary environment, install dependencies, and prepare the data for running the compression algorithms.

#### Execution Commands
Clear and concise commands for running the compression scripts, including examples of command-line arguments and expected outputs to ensure reproducibility of results.



--------


### Setup Instructions

### Execution Commands
Clear and concise commands for running the compression scripts, including examples of command-line arguments and expected outputs to ensure reproducibility of results.

## Data Analysis
### Preprocessing Insights
Discussion of the preprocessing steps required for the data before applying the compression algorithms, including any data normalization or filtering techniques applied.

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





# n1-codec
A highly efficient compression algorithm for the N1 implant. (neuralink's compression challenge)



## Table of Contents
- Overview (what the hell is the challenge in broad strokes, insert a picture of the data pre and post compression to demonstrate complete losslessness, the 6 buckets of compression algos deployed) & results
- Repository Structure
- How to Run
- Data Analysis
- Algorithms Deployed
  - bucket x
    - analysis
- Next Steps

 Lossless compression reduces the size of a file without removing any information, meaning the
original data will be perfectly intact following decompression. The final size of the compressed file depends
45 on the randomness or redundancy of the data it contains (a file with more random/unpredictable values will be
less compressible). Different lossless compressors employ different strategies for eliminating redundancy, but so
far there has been no systematic comparison of how they interact with continuously sampled electrophysiology
signals, which display high correlations across both space and time.







