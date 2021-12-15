# SwissBorg-challenge
## Foreword
In this repo, you will find 2 items:
* [arbitrage_swissborg.py](https://github.com/ChrisHellboy/swissborg-challenge/blob/master/arbitrage_swissborg.py) : the program I developed in Python to answer the challenge described here: https://priceonomics.com/jobs/puzzle/
* [what-is-CHSB.md](https://github.com/ChrisHellboy/swissborg-challenge/blob/master/what-is-CHSB.md) : a simple text file which gives my answer the following question: What is the CHSB and what are its key features. I kept it simple and mostly used source material issued on SwissBorg website.

## Running the python script
Try running the following command, you should not require extra library to run:

```python3 arbitrage_swissborg.py```

It should return an array which will look similar to this one:

```[['JPY', 'BTC', 'EUR', 'JPY'], ['EUR', 'JPY', 'BTC', 'EUR'], ['BTC', 'EUR', 'JPY', 'BTC']]```

It contains the different sequences of currencies that could be bought in order to make a profit using arbitrage. 
In this example, we have 3 possible paths to make a profit:
* Path 1: JPY > BTC > EUR > JPY
* Path 2: EUR > JPY > BTC > EUR
* Path 3: BTC > EUR > JPY > BTC

It will also return the paths you could follow to make a profit:
```New opportunity detected:
From  USD  to  BTC  with rate:  0.008609399999999996
From  BTC  to  USD  with rate:  136.6609268
Benefit: 1.1765685831919195 
```

## Applying the Bellman-Ford Algorithm
I have implemented the Bellman-Ford algorithm in order to be able to use negative cycles in a node schema.
Our goal is to find the loops which enables us to make a profit.
To get a better understanding, let's see an example :
Let's say we have 3 currencies, making a benefit would imply the following:
* ```rate(curr1,curr2)*rate(curr2,curr3)*rate(curr3,curr1) > 1```

* ```log(rate(curr1,curr2)*rate(curr2,curr3)*rate(curr3,curr1)) > log(1)```

* ```log(rate(curr1,curr2)) + log(rate(curr2,curr3)) + log(rate(curr3,curr1)) > 0```

* ```-log(rate(curr1,curr2))) - log(rate(curr2,curr3))) - log(rate(curr3,curr1))) < 0```

Seeing the problem under this form shows us we are actually able to use a negative cycle algorithm to make benefits in an arbitrage situation. 


## Algorithm complexity Analysis
*Disclaimer: I am not very confident in this analysis since i have never done such thing in the past but here is a brief try:* 
The complexity of the algorithm will increase when a new currency is added in the pool.
Looking at the amount of loops I have, I see the deepest level of loop i have is 3, now if n is my amount of currency it means i will have ```n^2``` edges and thus my algorithm complexity will be :
```n^4```