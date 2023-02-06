Must do before running this program:

Install Python (version 3.4 or later)

Install matplotlib on the machine being used with this command:

pip install matplotlib

Navigate to the repository you want this program to be placed in.

Download the git repository with this command:

git clone https://github.com/mtczech/fetchmltest.git

Navigate to the root of the new directory with this command:

cd fetchmltest

To run the program, use this command:

python fetchmltest.py "DECAY_FACTOR" "THRESHOLD"

where "DECAY_FACTOR" and "THRESHOLD" will be explained later.

Why not Docker?

The issue with Docker comes from an inability to set up an image that would display the graph. When I tried to display the graph from the Docker image, my system said the program could not access the display needed to show the graph. In the end, because I wasn't sure if the program would run properly on other operating systems even if I did succeed in making it run on mine, I decided to scrap the idea of using Docker.

What machine learning concepts were used?

The model I used to make the graph was a weighted growth model. Basically, the math
behind the model involves calculating the rate of change from one day to the next. For example,
if one day 800,000 receipts were scanned and the next day 850,000 receipts were scanned, the rate of 
change from the first to the second day would be 50,000 receipts/day. However, since change is erratic
from one day to the next, some sort of smoothing is required. To solve this problem, I semi-averaged 
all of the changes from one day to the next. This is where the <DECAY_FACTOR> parameter comes in. 
The daily change is weighted like this: (change/day)*(<DECAY_FACTOR>^d), where d is the number of days
between the day the next change is being calculated for and the day of the change that is currently
being put in. For example, take this example:

Day 0: 900,000 receipts

Day 1: 800,000 receipts (down 100,000)

Day 2: 850,000 receipts (up 50,000)

If the decay factor is 0.9, the expected change from day 2 to day 3 is:
(50000*(0.9^0)) + (-100000*(0.9^1)), or 50000 - 90000, or a drop of 40,000 receipts.

This makes sense because the general trend is downward, but how far back do you want to go?
"DECAY_FACTOR" and the other parameter, "THRESHOLD" control this. The algorithm does not keep
calculating values forever-it stops once the time multiplier is below a certain threshold.
For example, if "THRESHOLD" was greater than 1, only the first value would be calculated
since the multiplier would always be 1 for the first iteration.

Notes on the algorithm/ways to improve:

This algorithm is better for short-term predictions than for long-term ones, since 
if you go far enough into the future with your predictions, you will only be making 
predictions based on changes that didn't actually happen. Because of this, the change/day
will inevitably flatten out, since the process of calculating the values will take in the
same values over and over again. In addition, seasonal trends are not taken into account.

Assumptions being made:

* The parameters "DECAY_FACTOR" and "THRESHOLD" are both floating point values.

* The data file being put in is named "data_daily.csv".

* The data file consists of two columns, one containing the dates of each result and the
other containing the result itself.

* The data is from the year 2021.

* The year being calculated is 2022.
