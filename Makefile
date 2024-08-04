DAY=13

YEAR=2017
N_EXAMPLES=1

create_year_folder:
	# Do this once to set up a folder for that year
	mkdir aoc_${YEAR}

create:
	# Copy template script and adjust x to day number
	cp util/aoc_x.py aoc_${YEAR}/aoc_${DAY}.py
	sed -i 's/_x/_${DAY}/g' aoc_${YEAR}/aoc_${DAY}.py
	sed -i 's/day=None/day=${DAY}/g' aoc_${YEAR}/aoc_${DAY}.py
	sed -i 's/year=None/year=${YEAR}/g' aoc_${YEAR}/aoc_${DAY}.py

add_empty_example_file:
	for i in $$(seq 1 ${N_EXAMPLES}); do \
		touch aoc_${YEAR}/aoc_${DAY}_exampledata$$i; \
	done

add_empty_data_file:
	touch aoc_${YEAR}/aoc_${DAY}_data

# TODO: put the above steps in a folder per day
# TODO: think about what to do for new 2023 puzzles concerning examples, currently falling back to using manual files

sync:  # Reminder for what command is to sync a project with the committed Pipfile.lock
	pipenv sync

get_cookie:  # Make sure to install browser-cookie3 as well
	aocd-token > ~/.config/aocd/token