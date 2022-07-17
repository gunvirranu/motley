
TESTBENCH = top_tb
SRCS	  = trading_engine.sv
GTKWAVE   = /Applications/gtkwave.app/Contents/Resources/bin/gtkwave

all: simulate

lint:
	verilator -Wall --lint-only $(SRCS)

simulate:
	iverilog -g2005-sv -o $(TESTBENCH).vvp $(SRCS) $(TESTBENCH).sv
	vvp $(TESTBENCH).vvp > $(TESTBENCH)_log.txt

plot: simulate
	$(GTKWAVE) $(TESTBENCH).vcd

clean:
	rm $(TESTBENCH).vvp $(TESTBENCH).vcd $(TESTBENCH)_log.txt
