CFLAGS := -g

% : %.c
	 gcc ${CFLAGS}  $< -o $@  


#
# Set demo to y to run the demonstration version of the code 
#

DEMO ?= n
ifeq ($(DEMO),y)
	PY_DIR := demo
	GDB_MSG := USING DEMONSTRATION CODE
else
        PY_DIR := .
	GDB_MSG := USING YOUR CODE
endif

.PHONY: help all clean

BINARY = section

all: ${BINARY}

clean : 
	rm -f ${BINARY}

PREFIX="run_"
help: # list targets starting with $PREFIX
	@echo "set DEMO=n|y to run your code (n) or the demo one (y)"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) 2>/dev/null \
                 | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' \
                 | sort \
                 | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' \
                 | grep ${PREFIX} \
                 | xargs

###########

run_section: ${BINARY}
	gdb ${BINARY} -ex "source $(PY_DIR)/section.py" -ex "echo \n$(GDB_MSG)\n" \
                      -ex "echo \nTEST: break_section start_profiling stop_profiling run\nTEST: run\n\n"

run_return: ${BINARY}
	gdb ${BINARY} -ex "source $(PY_DIR)/break_return.py" -ex "echo \n$(GDB_MSG)\n" \
                      -ex "echo \nTEST: break_return run 1\nTEST: run\n\n"

run_watch: ${BINARY}
	gdb ${BINARY} -ex "source $(PY_DIR)/reg_watchpoint.py" -ex "echo \n$(GDB_MSG)\n" \
                      -ex "echo \nTEST: start\nTEST: reg_watch eax main void *\nTEST: cont\n\n"

run_step: ${BINARY}
	gdb ${BINARY} -ex "source $(PY_DIR)/step_to_next_call.py" -ex "echo \n$(GDB_MSG)\n" \
	              -ex "echo \nTEST: start\nTEST: next * 2\nTEST: step-into-next-call OR step-before-next-call\n\n" \

run_fake: ${BINARY}
	gdb ${BINARY} -ex "source $(PY_DIR)/fake_function.py" -ex "echo \n$(GDB_MSG)\n" \
	              -ex "echo \nTEST: skip_function run OR fake_run_function\nTEST: run\n\n" 

