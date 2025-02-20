
set(AMPS_SRC_FILES
  amps_allreduce.c
  amps_bcast.c
  amps_clear.c
  amps_createinvoice.c
  amps_exchange.c
  amps_finalize.c
  amps_init.c
  amps_invoice.c
  amps_irecv.c
  amps_newpackage.c
  amps_pack.c
  amps_print.c
  amps_recv.c
  amps_send.c
  amps_sizeofinvoice.c
  amps_test.c
  amps_unpack.c
  amps_vector.c
  )

if(${PARFLOW_HAVE_CUDA})
  list(APPEND AMPS_SRC_FILES amps_gpupacking.cu)
endif(${PARFLOW_HAVE_CUDA})
