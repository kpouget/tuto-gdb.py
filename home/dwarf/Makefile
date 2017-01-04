CFLAGS := -g

HAS_DWARFDUMP := $(shell command -v dwarfdump 2> /dev/null)

TARGET := prodconsum

ifdef HAS_DWARFDUMP
    TARGET := ${TARGET} prodconsum.dwarf
endif

ifndef HAS_DWARFDUMP
    $(warning "dwarfdump not available, cannot generate prodconsum.dwarf")
endif


all : ${TARGET}
	@echo
	@echo "###"
	@echo "### $^ ready."
	@echo "###"
	@echo

prodconsum : prodconsum.c
	 gcc ${CFLAGS} $< -o $@ -lpthread

prodconsum.dwarf : prodconsum
	dwarfdump $< > $@	

clean :
	rm -f prodconsum prodconsum.dwarf
