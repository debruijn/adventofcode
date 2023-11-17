DAY=1
YEAR=2019
N_EXAMPLES=1

create:
	# Copy template script and adjust x to day number
	cp util/aoc_x.py aoc_${YEAR}/aoc_${DAY}.py
	sed -i 's/_x/_${DAY}/g' aoc_${YEAR}/aoc_${DAY}.py
	sed -i 's/day=None/day=${DAY}/g' aoc_${YEAR}/aoc_${DAY}.py
	sed -i 's/year=None/year=${YEAR}/g' aoc_${YEAR}/aoc_${DAY}.py

	# Copy empty data file -> no longer needed now we use aocd.get_data()
	# cp util/aoc_x_data aoc_${YEAR}/aoc_${DAY}_data

	# Copy empty example data file, N_EXAMPLES times -> no longer needed now we use aocd.models.Puzzle().examples -> TODO: think about what to do for new 2023 puzzles
	# for i in $$(seq 1 ${N_EXAMPLES}); do \
	# 	cp util/aoc_x_exampledata aoc_${YEAR}/aoc_${DAY}_exampledata$$i; \
	# done


# TODO: put the above steps in a folder per day
# TODO: think about what to do for new 2023 puzzles concerning examples, currently falling back to using manual files

sync:  # Reminder for what command is to sync a project with the committed Pipfile.lock
	pipenv sync

get_cookie:  # Make sure to install browser-cookie3 as well
	aocd-token > ~/.config/aocd/token