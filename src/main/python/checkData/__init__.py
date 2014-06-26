"""
This package contains programs that check the integrity of the edX data dumps.

Many of these programs are for historical reasons, but it is good to keep then around
as regression tests. Each has a description of the invariants that it checks on the
various research data.

The one that remains of interest is testKAnon.py, which will take a data set that is
supposed to be de-identified and checks to insure that there is no set of properties/fields
in the dataset that both
    tie to the external world, and
    in not shared by at least k other data lines in the set
where k is a user-supplied value. More complete documentation of that program is found in
the program file itself.
"""