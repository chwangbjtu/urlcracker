##target lib###
LIBS=libnetsvc
#DEST=../../../../lib/netsvc/0.1.4
DEST=../../lib
##complier##
CXX=g++
CXXFLAGS=${flags} -static
LDFLAGS=
##include dir and source dir##
INCLUDE_DIRS=-I./include
SRC_DIRS=. ./linux

##objects##
SRC=$(foreach srcdir, $(SRC_DIRS), $(wildcard $(srcdir)/*.cpp))
OBJS=$(patsubst %.cpp, %.o, $(SRC))

vpath %.h $(INCLUDE_DIRS)
vpath %.cpp $(SRC_DIRS)

$(LIBS):$(OBJS)
	
	@if [ ! -d ${DEST} ]; then mkdir -p ${DEST}; fi
	@if [ ! -z "${flags}" ] && [[ "${flags}" =~ ((^)|([[:blank:]]))-g(([[:blank:]])|($$)) ]];then ar r $(DEST)/$@d.a $^; else ar r $(DEST)/$@.a $^; fi

$(OBJS):%.o:%.cpp 
	$(CXX) $(CXXFLAGS) $(INCLUDE_DIRS) -c $< $(LDFLAGS) -o $@ 
	
.PHONY : clean

clean:
	rm -rf $(OBJS)

