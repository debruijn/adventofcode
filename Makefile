DAY=13
YEAR=2020
N_EXAMPLES=1

create:
	# Copy template script and adjust x to day number
	cp util/aoc_x.py aoc_${YEAR}/aoc_${DAY}.py
	sed -i 's/_x/_${DAY}/g' aoc_${YEAR}/aoc_${DAY}.py
	sed -i 's/day=None/day=${DAY}/g' aoc_${YEAR}/aoc_${DAY}.py

	# Copy empty data file
	cp util/aoc_x_data aoc_${YEAR}/aoc_${DAY}_data

	# Copy empty example data file, N_EXAMPLES times
	for i in $$(seq 1 ${N_EXAMPLES}); do \
		cp util/aoc_x_exampledata aoc_${YEAR}/aoc_${DAY}_exampledata$$i; \
	done


# TODO: create "add example" that sees latest example file and adds a new one
# TODO: put the above steps in a folder per day

sync:  # Reminder for what command is to sync a project with the committed Pipfile.lock
	pipenv sync
