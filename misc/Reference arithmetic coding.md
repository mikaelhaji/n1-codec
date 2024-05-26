Project Nayuki![](Aspose.Words.8bb75a30-b268-4d55-8051-a31620b245b9.001.png)

![](Aspose.Words.8bb75a30-b268-4d55-8051-a31620b245b9.002.png) Reference arithmetic coding

This project is a clear implementation of [arithmetic coding](https://en.wikipedia.org/wiki/Arithmetic_coding), suitable as a reference for educational purposes. It is provided separately in Java, Python, and C++, and its code is open source. The code can be used for study, and as a solid basis for modification and extension. Consequently, the codebase optimizes for readability and avoids fancy logic, and does not target the best speed/memory/performance.

Arithmetic coding is an ingenious generalization of [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding) that allows each symbol to be coded with a non-whole number of bits (when averaged over the entire message), thus improving compression efficiency. But while Huffman coding is rela- tively straightforward to understand and implement, arithmetic coding involves many subtle details and requires numbers to be handled very carefully to prevent out-of- range conditions, overflow, etc. I will not attempt to explain arithmetic coding on this page, since there are tutorials readily available from searching the web.

The intent and structure of this arithmetic coding implementation are very similar to [my Huffman coding implementation](https://www.nayuki.io/page/reference-huffman-coding). You might want to study that code first if you en- counter difficulty understanding this one.

Source code

Browse the full source code at GitHub: [ https://github.com/nayuki/Reference-arith- metic-coding](https://github.com/nayuki/Reference-arithmetic-coding)![](Aspose.Words.8bb75a30-b268-4d55-8051-a31620b245b9.003.png)

Or  download  a  ZIP  of  all  the  files: [  https://github.com/nayuki/Reference-arith- metic-coding/archive/master.zip](https://github.com/nayuki/Reference-arithmetic-coding/archive/master.zip)![](Aspose.Words.8bb75a30-b268-4d55-8051-a31620b245b9.004.png)

Overview

Arithmetic encoding takes a sequence (stream) of symbols as input and gives a se- quence of bits as output. The intent is to produce a short output for the given input. Each input yields a different output, so the process can be reversed, and the output can be decoded to give back the original input.

In this software, a symbol is a non-negative integer. The symbol limit is one plus the highest allowed symbol. For example, a symbol limit of 4 means that the set of al- lowed symbols is {0, 1, 2, 3}.

The following explains all the submodules in the software package: **Sample applications**

Three pairs of command-line programs fully demonstrate how this software package can be used to encode and decode data using arithmetic coding.

- The class [ArithmeticCompress deriv](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/ArithmeticCompress.java?ts=4)es a static frequency table and writes it to the compressed file, and [ArithmeticDecompress reads ](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/ArithmeticDecompress.java?ts=4)the frequency table and

  uses it to decode all the symbols.

- The  classes  [AdaptiveArithmeticCompress ](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/AdaptiveArithmeticCompress.java?ts=4)and [AdaptiveArithmeticDecompress start with](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/AdaptiveArithmeticDecompress.java?ts=4) a flat frequency table and update it after  each  byte  is  processed,  thus  making  it  reflect  the  statistics  of  the  file  being compressed.
- The classes [PpmCompress an](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/PpmCompress.java?ts=4)d [PpmDecompress implemen](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/PpmDecompress.java?ts=4)t a basic version of pre- [diction by partial matching](https://en.wikipedia.org/wiki/Prediction_by_partial_matching). In PPM, the frequency predictions for the next symbol is based on the previous *n* symbols processed.

**Encoder/decoder**

The  classes  [ArithmeticCoderBase,  ](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/ArithmeticCoderBase.java?ts=4)[ArithmeticEncoder,  and ](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/ArithmeticEncoder.java?ts=4)[ArithmeticDecoder implement](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/ArithmeticDecoder.java?ts=4) the basic algorithms for encoding and decoding

an arithmetic-coded stream. The frequency table can be changed after encoding or de- coding each symbol, as long as the encoder and decoder have the same table at the same position in the symbol stream. At any time, the encoder must not attempt to en- code a symbol that has a zero frequency.

**Frequency tables**

Objects with the interface [FrequencyTable keep](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/FrequencyTable.java?ts=4) track of the frequency of each symbol, and provide cumulative frequencies too. The cumulative frequencies are the essential data that drives arithmetic coding.

**Bitwise I/O streams**

The  classes  [BitInputStream  and ](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/BitInputStream.java?ts=4) [BitOutputStream  are  bit-oriented](https://github.com/nayuki/Reference-arithmetic-coding/blob/master/java/src/BitOutputStream.java?ts=4)  I/O streams, analogous to the standard bytewise I/O streams. However, since they use an underlying bytewise I/O stream, the bit stream’s total length is always a multiple of 8 bits.

**Test suite**

A JUnit [test suite](https://github.com/nayuki/Reference-arithmetic-coding/tree/master/java/test) checks that compressing and decompressing an arbitrary byte se- quence will give back the same byte sequence. This is done on short, simple sequences and on longer random sequences. The test suite checks the 4 main programs mentioned above (ArithmeticCompress, etc.).

**Other languages**

The Python and C++ versions of this library were ported from the Java version. They contain all the core functionality provided by the Java version, but not some of the ex- tended features or verbose documentation comments. The API naming and semantics follow the Java version, unless the target language has a more idiomatic way of doing things (e.g. underscore names and native bigint in Python). All language versions en- code and decode exactly the same data. For example, it is acceptable to encode a file using ArithmeticCompress.java and then decode it using arithmetic-decompress.py.

Limitations

- FrequencyTable works with alphabets of up to Integer.MAX\_VALUE-1 (i.e.

  231 − 2) symbols in Java, UINT32\_MAX-1 (i.e. 232 − 2) symbols in C++, and unlimit- ed symbols in Python.

- FrequencyTable  has  a  maximum  total  of  Integer.MAX\_VALUE  in  Java, UINT32\_MAX in C++, and unlimited in Python.

Suggestions

Here are some ideas on how to use, modify, or extend this software:

- Speed up the frequency table by using [binary indexed trees / Fenwick trees](https://en.wikipedia.org/wiki/Fenwick_tree), so that changing a symbol’s frequency and getting cumulative frequencies are both fast in *O*(log *n*) time.
- Improve the [prediction by partial matching (PPM)](https://en.wikipedia.org/wiki/Prediction_by_partial_matching) model – statistics, order selection, behavior of escapes, exclusions, etc.
- Take an existing compression algorithm that uses Huffman coding, and retrofit it to use arithmetic coding instead. Observe how easy or difficult the adaptation process is, and how much the compression efficiency improves by.

More info

- [Wikipedia: Arithmetic coding](https://en.wikipedia.org/wiki/Arithmetic_coding)
- [Mark Nelson: Data Compression With Arithmetic Coding](https://marknelson.us/posts/2014/10/19/data-compression-with-arithmetic-coding.html)
- [Mark Nelson: Arithmetic Coding + Statistical Modeling = Data Compression](https://marknelson.us/posts/1991/02/01/arithmetic-coding-statistical-modeling-data-compression.html)
- [Arturo Campos: Basic arithmetic coding](https://web.archive.org/web/20091012172510/http://www.arturocampos.com/ac_arithmetic.html)

Categories: [Programming](https://www.nayuki.io/category/programming), [Java](https://www.nayuki.io/category/java), [Python](https://www.nayuki.io/category/python), [C++](https://www.nayuki.io/category/cpp) Last updated: [2018-06-28 ](https://www.nayuki.io/recent-pages/)**Feedback:** Question/comment? [Contact me](https://www.nayuki.io/page/about#contact) [Copyright © 2024 Project Nayuki](https://www.nayuki.io/page/about#copyright)
