DAY=7
N_EXAMPLES=1

create:
	# Copy template script and adjust x to day number
	cp aoc_x.py aoc_${DAY}.py
	sed -i 's/_x/_${DAY}/g' aoc_${DAY}.py

	# Copy empty data file
	cp aoc_x_data aoc_${DAY}_data

	# Copy empty example data file, N_EXAMPLES times
	for i in $$(seq 1 ${N_EXAMPLES}); do \
		cp aoc_x_exampledata aoc_${DAY}_exampledata$$i; \
	done


# TODO: create "add example" that sees latest example file and adds a new one
# TODO: put the above steps in a folder