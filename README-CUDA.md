# Building Parflow with GPU acceleration

**WARNING!** Parflow GPU support is still in beta and there may be issues with it.

The GPU acceleration is currently compatible only with NVIDIA GPUs due to CUDA being the only backend option so far. The minimum supported CUDA compute capability for the hardware is 6.0 (NVIDIA Pascal architecture).

Building with CUDA may improve the performance significantly for large problems but is often slower for test cases and small problems due to initialization overhead associated with the GPU use. Currently, the only preconditioner resulting in a good performance is MGSemi. Installation reference can be found in [Ubuntu recipe](/cmake/recipes/ubuntu-18.10-CUDA), [Dockerfile](Dockerfile_CUDA), and [travis.yml](.travis.yml).


## CMake

Building with GPU acceleration requires a [CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html) installation. However, the performance can be further improved by using pool allocation for Unified Memory (requires [RMM v0.10](https://github.com/rapidsai/rmm/tree/branch-0.10) installation) and direct communication between GPUs (requires a CUDA-Aware MPI library).
The GPU acceleration is activated by specifying *PARFLOW_ACCELERATOR_BACKEND=cuda* option to the CMake, e.g.,

```shell
cmake ../parflow -DPARFLOW_AMPS_LAYER=mpi1 -DCMAKE_BUILD_TYPE=Release -DPARFLOW_ENABLE_TIMING=TRUE -DPARFLOW_HAVE_CLM=ON -DCMAKE_INSTALL_PREFIX=${PARFLOW_DIR} -DPARFLOW_ACCELERATOR_BACKEND=cuda
```
where *DPARFLOW_AMPS_LAYER=mpi1* leverages GPU-based data packing and unpacking. By default, the packed data is copied to a pinned host staging buffer which is then passed for MPI to avoid special requirements for the MPI library. Direct communication between GPUs (with [GPUDirect P2P/RDMA](https://developer.nvidia.com/gpudirect)) can be activated by specifying an environment variable *PARFLOW_USE_GPUDIRECT=1* during runtime in which case the memory copy between CPU and GPU is avoided and a GPU pointer is passed for MPI, but this requires a CUDA-Aware MPI library (support for Unified Memory is not required because the pointers passed to the MPI library point to pinned GPU memory allocations).

Furthermore, RMM library can be activated by specifying the RMM root directory with *DRMM_ROOT=/path/to/rmm_root* as follows:
```shell
cmake ../parflow -DPARFLOW_AMPS_LAYER=mpi1 -DCMAKE_BUILD_TYPE=Release -DPARFLOW_ENABLE_TIMING=TRUE -DPARFLOW_HAVE_CLM=ON -DCMAKE_INSTALL_PREFIX=${PARFLOW_DIR} -DPARFLOW_ACCELERATOR_BACKEND=cuda -DRMM_ROOT=/path/to/RMM
```
## Running Parflow with GPU acceleration

Running Parflow built with GPU support requires that each MPI process has access to a GPU device. Best performance is typically achieved by launching one MPI process per available GPU device. The MPI processes map to the available GPUs by 

```cudaSetDevice(node_local_rank % local_num_devices);```

where node_local_rank and local_num_devices are the node-local rank of the process and the number of GPUs associated with the corresponding node, respectively. Therefore, launching 4 MPI processes per node that has 4 GPUs automatically means that each process uses a different GPU. Launching more processes (than the number of available GPUs) is only supported when using CUDA Multi-Process Service (MPS), but this typically results in reduced performance.

Any existing input script can be run with GPU acceleration; no changes are necessary. However, it is noted that two subsequent runs of the same input script using the same compiled executable are not guaranteed to produce identical results. This is expected behavior due to atomic operations performed by the GPU device (i.e., the order of floating-point operations may change between two subsequent runs).
