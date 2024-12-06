#!/bin/env sh
# This small script checks that the BAGUETTE redirection script can be found (i.e. that BAGUETTE has been installed) and runs it.
if python3 -m baguette 2> /dev/null; then
    python3 -m baguette.open "$0" $@
else
    echo "baguette-verse has not been properly installed on this system."
fi
exit