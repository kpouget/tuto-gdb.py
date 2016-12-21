CFLAGS := -g

all : prodconsum.dwarf
	@echo
	@echo "###"
	@echo "### $< is ready."
	@echo "###"
	@echo

prodconsum : prodconsum.c
	 gcc ${CFLAGS} $< -o $@ -lpthread

prodconsum.dwarf : prodconsum
	dwarfdump $< > $@	

clean :
	rm -f prodconsum prodconsum.dwarf
