CC=g++
CFLAGS=-std=c++20
LDFLAGS=-lmata

NAME1=bench-reduction

LINK=utils/utils.cc

.PHONY: all clean

all: $(NAME1)

$(NAME1): $(NAME1).cc
	$(CC) $(CFLAGS) $(NAME1).cc $(LINK) -o $(NAME1) $(LDFLAGS)

clean:
	rm bench-reduction
