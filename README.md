## Probabilistic data structures for stream processing

This repository contains various data structures and algorithms to estimate
cardinalities and frequencies of large data streams. A lot of the implementations
very heavily influenced by (a great blog article about those sketches)(https://highlyscalable.wordpress.com/2012/05/01/probabilistic-structures-web-analytics-data-mining/)

By now, the following sketches are implemented

- Linear cardinality estimation counter that grows linearliy with increasing stream sizes
- Loglog counter to estimate the cardinality of large streams with sublinear growth
- Count-Min-Sketch to estimate frequencies of elements of a large stream
