# swissborg-challenge
## Foreword
In this repo, you will find 2 items:
* arbitrage_swissborg.py : the program I developed in Python to answer the challenge described here: https://priceonomics.com/jobs/puzzle/
* what-is-CHSB.md : a simple text file which gives my answer the following question: What is the CHSB and what are its key features. I kept it simple and mostly used source material issued on SwissBorg website.

## Running the python script
Try running the following command:

```python3 arbitrage_swissborg.py```

It should return an array which will look similar to this one:

```[['JPY', 'BTC', 'EUR', 'JPY'], ['EUR', 'JPY', 'BTC', 'EUR'], ['BTC', 'EUR', 'JPY', 'BTC']]```

and contains the different sequences of currencies that could be bought in order to make a profit using arbitrage. 
In this example, we have 3 possible paths to make a profit:
* Path 1: JPY > BTC > EUR > JPY
* Path 2: EUR > JPY > BTC > EUR
* Path 3: BTC > EUR > JPY > BTC

