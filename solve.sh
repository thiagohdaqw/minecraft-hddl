#!/bin/bash

TIMELIMIT="600s"

while read -r file; do
    time timeout $TIMELIMIT java -jar panda.jar domain.hddl in/$file.hddl | tee out/$file.out
    if [[ "$?" != "0" ]]; then
        rm out/$file.out;
        echo "$file.hddl" >> tle.out
    fi
done << EOF
p-003-004-004-004
p-004-004-004-004
p-004-005-004-005
p-004-005-005-005
p-005-005-005-005
p-005-006-005-006
p-005-006-006-006
p-006-006-006-006
p-006-007-006-007
p-006-007-007-007
p-007-007-007-007.hddl
p-007-008-007-008.hddl
p-007-008-008-008.hddl
p-008-008-008-008.hddl
p-008-009-008-009.hddl
p-008-009-009-009.hddl
p-009-009-009-009.hddl
p-010-009-009-010.hddl
p-010-010-010-010.hddl
p-5-5-5-06
p-5-5-5-07
p-5-5-5-08
p-5-5-5-09
p-5-5-5-12
p-5-5-5-12
p-5-5-5-13
p-5-5-5-14
p-5-5-5-15
p-5-5-5-16
EOF