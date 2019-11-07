CFLAGS=-std=c11 -g -static

minc: minc.c

test: minc 
	./test.sh

clean:
	rm -f 9cc *.o *~ tmp*

.PHONY: test clean
