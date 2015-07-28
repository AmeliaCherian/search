##### Documents

There are 131896 LA Times documents divided into 730 files. 10 of these, with the most number of relevant documents, were picked below. LA Times seems to have very few relevant documents. Of 57565 judged documents, 3535 are relevant and the rest non-relevant.


```
file     rel  numdocs
======== ===  =======
la112689 11   206
la121289 11   160
la052790 12   241
la100590 12   196
la110890 12   276
la052589 13   221
la081490 14   185
la100889 15   229
la102390 15   177
la042990 16   252
======== ==== ========
TOTAL	 131  2143
```
##### Topics

```
file	  numtopics
========= =========
ten.T	  65
301-350.T 50
351-400.T 50
401-450.T 50
```

The TITLE portions of the TREC topics, in three files, containing 50 topics each. The file's structure is as shown here; the topic ID followed by the text.

```
311  Industrial Espionage
312  Hydroponics
313  Magnetic Levitation-Maglev
```

ten.T are the 65 topics which have at least one relevant document in the set of 2143 LA Times documents (bundled in ten files). 

##### Qrels

```
file            numqrels numtopics
=============== ======== =========
ten.LA          573	 65    
301-350.cd45.LA 13815	 50
351-400.cd45.LA	22491	 50
401-450.cd45.LA	21259	 50
```

Qrels for the LA Times documents. Each file is for a range of 50 TREC topics. The file's structure is as shown below. The columns in order are topic id, unused, docno and the judgement. The second field is of no use. The relevance is binary, denoted by zero or one, in the fourth field.

```
301 0 LA122889-0124 0
301 0 LA123090-0148 0
302 0 LA010490-0100 0
302 0 LA010490-0127 0
302 0 LA010589-0059 1
302 0 LA010690-0044 0
```

ten.LA is a subset containing qrels for only the 2143 documents in the ten-file collection, and, only the 65 topics which have at least one relevant document.
