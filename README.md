# Calculating FIS points

___

## Information

This file contains information on calculating the fis-points of a FIS Cross Country race. Use the *fispoints.py* file to calculate the fis-points.

### Requirements

- Python3.6 or higher

## Calculation summary

FIS points for individual competitions are calculated based on a *factor*, a *penalty* and time behind the winner. The factor is a fixed value based on competition type. The penalty is calculated based on the **three best ranked** (latest official FIS-list rank) of the **five best finishers**.

Every race is assigned a minimum penalty based on the *race importance* where normal senior FIS competitions have a minimum penalty of 20 points. The individual race points will be the sum of the penalty and the calculated points based on time behind winner and the factor. I.E. the race winner's points will be the penalty (either calculated or minimum penalty).

## FIS-list

FIS points earned by a competitor are valid for 365 days.

### Distance (longer than Sprint)

A competitor's points will be the average of his or her best five results
in distance competitions over the period of the last twelve months.

### Sprint

A competitor's points will be the average of his or her best five results
in sprint competitions over the period of the last twelve months.

### Less than 5 results

A competitor's Sprint FIS points and Distance FIS points represent
the average of the best 5 valid results for each format. If the
competitor has less than 5 valid results the average will be adjusted
according to the following table, but with a minimum of 4 FIS points:

| Less than 5 results                   |
|---------------------------------------|
| best 4 results x 1.1 = FIS points     |
| best 3 results x 1.2 = FIS points     |
| best 2 results x 1.3 = FIS points     |
| best 1 results x 1.4 = FIS points     |

## Usage

Create race csv file as follows:

    $~python3 create_race.py <outfile.csv> --option

Run the *fispoints.py* file as follows:

    $~python3 fispoints.py <infile.csv> <outfile.csv>
The csv file have to be built up as follows:

    bib,name,nsa,time,fislist-point

The program will write the a sorted, ranked list of racers with the racers competition fis-points

## Race points formula

$$ P_{race} = \frac{F \cdot T_x}{T_o} -F $$
$$or$$
$$P_{race} = (\frac{T_x}{T_o}-1)\cdot F$$

    P  = Race points 
    Tx = Time of the classified competitor in seconds
    To = Time of the winner in seconds
    F  = Competition factor

## Factor

| Competition                               | Factor |
|-------------------------------------------|--------|
| Interval start                            | 800    |
| Sprints and Pursuit competitions 2nd part | 1200   |
| Mass start and Skiathlon                  | 1400   |

## Penalty

Every race is given a specific penalty based on the status of the race and the competitors.

The FIS points of the top five competitors from the actual
FIS points list are considered and the three best values are added
and divided by 3.75.
$$p = \frac{\sum_{i=1}^3 a_i}{3.75}$$
$a_i$ = the three best fis-ranked racers among the top five finishers

### Minimum penalty

|     Competition                 | Men | Women |
|---------------------------------|-----|-------|
| U23 World Championships         | 25  | 25    |
| Junior World Championships      | 35  | 35    |
| Senior COC and FIS competitions | 20  | 20    |
| Junior COC and FIS competitions | 35  | 35    |
| EYOF                            | 60  | 60    |

- If the calculated penalty is higher than the
minimum penalty , the calculated penalty will be
applied to the race.

- If the calculated penalty is less than the minimum penalty, the
minimum penalty will be applied to the race.

## Final calculation

$$P_{final} = P_{race} + p$$

Final calculation is dependent on the value of penalty. If the calculated value is lower then the minimum penalty, the minimum penalty is used. If the calculated value is higher then the minimum penalty, the calculated penalty is used.
