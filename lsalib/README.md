A Latent Semantic Analysis Library
==================================

Author(s): Keith Murray

Contact: kmurrayis@gmail.com

Requirements:
=============
Python 2.7.6
	Standard Libraries:
	os, sys, and math
	Added Libraries:
	numpy, scipy, sklearn

Installation:
=============
```python
pip install lsalib
```


Usage:
======
This library is a termDocMatrix class. 
It was built to follow the Thesis of Sam Way, found here http://digitalcommons.unl.edu/elecengtheses/42/

```python
>>> import lsalib
# To use this, initalize a varible,
>>> lsa = lsalib.termDocMatrix()

# After this, you can add documents to the matrix. This can be done in a number of ways
# With Strings:
>>> lsa.add("HELLO WORLD! THE WIND RISES, WE MUST TRY TO LIVE")

# With Dictionaries (a key:count relationship)
>>> lsa.add({"tree":5, "apple":3, "WORLD":8, "planes":2})

# With lists of strings:
>>> lsa.add(["apples", "oranges", "apples", "WORLD", "HELLO"])

# With lists of dictionaries which follow the key:count relationship:
>>> lsa.add([D1, D2, D3, D4])
```

It's important to note that there is no processing done on any of the inputs. 
This means the inputs are case sensitive, any symbol such as a comma tied to a word will
also be included in the term list. 
Therefore "Apples", "apples", and "apples," are all treated as unique words.
If this is undesirable, the strings will need to be preprocessed before lsa.add() is called.

As each document is added to the matrix, a term frequency weighting is applied. 




```python
# Once all documents are added to the matrix, the inverse document frequency weighting
# can be called:
>>> lsa.weight_idf()

# And once that has completed, use lsa.nmf to reduce the weighted term doc matrix 
# to it's basis k components for the terms and documents:
>>> P, Q = lsa.nmf(5)

# P is the basis vector set for the terms, and has a dimensionality of terms x k,
# Q is the basis vector set for the documents, and has a dimensionality of docs x k,
# P x Q.T will yield an approximation of the original term document matrix with a certain error

# This error is stored in lsa.er
>>> print lsa.er
```

