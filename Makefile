# Compilers
NVCC := nvcc

# Include and library paths
INCLUDES := -I$(CUDA_PATH)/include
LIBS := -L$(CUDA_PATH)/lib64 -lcudart

# NVCC compiler flags
NVCC_FLAGS := -arch=sm_86 -std=c++17

# Source and object files
CU_SRCS := bls12-381.cu commitment.cu fr-tensor.cu g1-tensor.cu proof.cu zkrelu.cu zkfc.cu tlookup.cu polynomial.cu zksoftmax.cu
CU_OBJS := $(CU_SRCS:.cu=.o)
CPP_SRCS := $(wildcard *.cpp)
CPP_OBJS := $(CPP_SRCS:.cpp=.o)
TARGETS := test zkattn-test linear-test
TARGET_OBJS := $(TARGETS:=.o)

# Pattern rule for CUDA source files
%.o: %.cu
	$(NVCC) $(NVCC_FLAGS) $(INCLUDES) -dc -dlto $< -o $@

# Pattern rule for C++ source files
%.o: %.cpp
	$(NVCC) -x cu $(NVCC_FLAGS) $(INCLUDES) -dc -dlto $< -o $@

# General rule for building each target
$(TARGETS): % : %.o $(CU_OBJS) $(CPP_OBJS)
	$(NVCC) $(NVCC_FLAGS) $(INCLUDES) $(LIBS) $^ -o $@ -dlto

# Clean rule
clean:
	rm -f $(TARGET_OBJS) $(CU_OBJS) $(CPP_OBJS) $(TARGETS)

# Default rule
all: $(TARGETS)