# Diebus

Reingold &amp; Dershowitz Calendrica ported to Python

## Motivation

"Calendrical calculations" by Edward Reingold and Nachum Dershowitz (further: R&D), in its consequent editions (see **References**) present a perfect practical guide for the transformation of calendrical dates between different calendar szstems. However, only LISP, Java, and Mathematica implementations are contained, and I was unable to find a usable implementation in a language I need in my daily work (Python being one of them). So I decided to develop a port by myself.

## Scope

This repository contains Python code files, unit tests, and test data for a Python implementation of mathematical formulas contained in R&D books, partially inspired by the original LISP code, as well as by the Java code (written by Robert C. NcNally).

At the time of writing, only the arithmetical calendars described in the RDM editions are implemented and tested. The astronomical calendars are coming soon. Additional calendars introduced in RDU will be added in a later version. Implementations for other programming languages (such as C#, PHP, C++) are planned for some more distant future.

## Contribution

Anybody who would like to collaborate is welcome. Please be so kind, however, to inform me by email before you make changes, thanks.

## References

1. Reingold, Edward M., and Nachum Dershowitz. Calendrical Calculations. 2nd edition. Cambridge, UK ; New York: Cambridge University Press, 2001. ISBN 978-0-521-77167-2. 
    Cited here and in code comments as RDM (Millenium edition).
2. Dershowitz, Nachum, and Edward M. Reingold. Calendrical Calculations. 3rd edition. Cambridge ; New York: Cambridge University Press, 2007. ISBN 978-0-521-70238-6.
    Cited here and in code comments as RD3.
3. Reingold, Edward M., and Nachum Dershowitz. Calendrical Calculations: The Ultimate Edition. 4th edition. Cambridge ; New York: Cambridge University Press, 2018. ISBN 978-1-107-68316-7.
    Cited here and in code comments as RDU (Ultimate edition).
