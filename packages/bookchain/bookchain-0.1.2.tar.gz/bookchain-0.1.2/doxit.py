import autodox
import bookchain
import bookchain.asyncql

docs = autodox.dox_a_module(bookchain)
with open('dox.md', 'w') as f:
    f.write(docs)

docs = autodox.dox_a_module(bookchain.asyncql)
with open('asyncql_dox.md', 'w') as f:
    f.write(docs)
