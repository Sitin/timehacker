Time Hacker
===========

Next generation time tracking utility. 

Usage
-----

```bash
./timehack.py -h
```

Examples
--------

The following will give 22 results for person who comes to work from 10:15 to 11:20, averagely works 8 hours, finishes
work on 25 minutes earlier/later, has a lunch about 50 minutes with 15 minutes deviation.

```bash
./timehack.py 10:15 11:20 8:00 --presence_deviation 00:25:00 --absence 0:50 --absence_deviation 0:15 --results 22
```
