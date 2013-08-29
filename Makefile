# I like make

all:
	python setup.py build_ext --inplace

clean:
	rm -f *.pyc *.so mods/*.so mods/*/*.c *.c build/temp*/*.o
	-rmdir -p build/temp*
	git status --ignored

debian:
	sudo apt-get install python-pyglet python-imaging

