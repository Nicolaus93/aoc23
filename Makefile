
DAY ?= $(shell date +%d)
YEAR ?= $(shell date +%Y)
FILE_TEMPLATE = utils/solution_template.py

.PHONY: solution-dir
solution-dir:
	mkdir src/day${DAY} 	\
	&& cp ${FILE_TEMPLATE} src/day${DAY}/part1.py		\
	&& touch src/day${DAY}/test.txt \
	&& touch src/day${DAY}/input.txt
#	&& rpl "day=1" "day=${DAY}" src/day${DAY}/part1.py \

.PHONY: part2
part2:
	cp src/day${DAY}/part1.py src/day${DAY}/part2.py

.PHONY: tox
tox:
	python -m tox

.PHONY: deps
deps:  ## Install dependencies
	pip install -r requirements.txt
