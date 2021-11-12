# Rules for calculating fis points
___
### Information
This file contains information on calculating the fis-points of a FIS Cross Country race. Use the *fispoints.py* file to calculate the fis-points.

#### Requirements
 - Python3.6 or higher

#### Usage
 -
Run the *fispoints.py* file as follows:

    $~python3 fispoints.py <racefile.csv>
The csv file have to be buildt up as follows:

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
applied to the race.<br/>

 - If the calculated penalty is less than the minimum penalty, the
minimum penalty will be applied to the race.<br/>


## Final calculation

$$P_{final} = P_{race} + p$$

Final calculation is dependent on the value of penalty. If the calculated value is lower then the minimum penalty, the minimum penalty is used. If the calculated value is higher then the minimum penalty, the calculated penalty is used.