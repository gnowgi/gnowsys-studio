==========
RDF Graphs
==========

Gstudio is committed to standard representation notations provided by
various standard bodies.  RDF being one of the most widely used
language, we provide methods to obtain RDF representation of all the
data, excluding private information of users and system specific data.
We use rdflib library.  Therefore any notation or RDF store options
provided by rdflib can be supported. 

Currently this feature is implemented as a part of the management
module. Two specific commands are implemented: one to dump all data in
RDF in a file and upload it to the integrated 4store.  The second
command returns RDF graph of a given node id.

More details will be updated as and when we enhance the details of
this feature.
