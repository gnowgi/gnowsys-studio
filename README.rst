==============
GNOWSYS Studio
==============

A collaborative workspace (studio) for constructing and publishing semantic
knowledge networks and ontologies.  


Features
========

The application is devided into two sub-apps.  Gstudio and
Objectapp. The former includes classes for organizing the network or
constructing an ontology.  The latter includes classes for holding the
instances of object-types, process-types and system-types. 

Gstudio Components
------------------

* Metatypes

  To hold Classes which have other classes as its members. e.g. "abstract noun", "adjective", "phylem", "class", "genus", "species" etc.
* Object types

  To hold Classes: e.g. "thing", "being", "living being", "animals", "cat", "place", "person" etc.
* Relation types
  
To define binary relations (object properties) between classes and objects.  e.g., "part of", "friend of", "composed of", "located in" etc.
* Attribute types
  
  To define datatype properties for classes and objects. e.g., "population", "size", "length", "height", "first name", "phone number" etc.
* System types 
  
  To bring together some of the classes into a system or
  an ontology, a collection of the types defined above for
  convenience. You can bring together the required classes, relations
  and attributes into 
* Process types

  To define a process as prior and post states of classes or objects.
* Attributes

  To store attributes
* Relations

  To store binary relations
* Node Specification

  A node specified (described) by its relations or attributes or both.  
* Relation Specification
  
  To create an expression using a relation with a subject, e.g.,
  "friend of Tom", "components of a cell" etc.

* Attribute Specification

  To specify an attribute by a subject to say for example: population
  of India, color of a flower etc.  These do not yeild a proposition
  but an expression, which can be used as a subject in another
  sentence.

* Expression
  
  Expression is more like a relation between two terms, but it does not yeild a proposition, e.g., 
  "Researchers in  India", "students residing in India" etc.  It is modelled more like relation
  class, except that the result is not a proposition/triple.

* Union
  
  To define a class by a union relation between two or more classes.

* Complement

  To define a class as a compleemnt of two or more classes.

* Intersection

  To define a class as an intersection between two or more classes.

Objectapp Components
------------------

* Objects
  
  To hold the instances of Object types: "Mumbai", "Tom" etc.

* Systems

  To hold the instances of System types.  

* Processes

  To hold the instances of processes.

Online Collaborative Platform
=============================

The application is built as a collaborative on line platform with the following features.

Version Control
---------------

All the changes by the users will be recorded.  This feature is implemented using  using django-reversion.

User Registration
-----------------

Basic registration, authentication mechanism.


Network Navigation using SVG graphs
==================================

* neighbourhood graphs and concept graphs



Other Semantic Web features
===========================

* data in RDF format
* rdf feed to a triple store
* sparql endpoint

Features to be implemented
==========================

* export and import of standard knowledge representation languages: CL, OWL, XTM etc.

Features adopted from Django-Blog-Zinnia
========================================

The following features are adopted from django-blog-zinnia code base
with a lot of gratitude.  Thanks to an excellent codebase of
django-blog-zinnia, which taught us best software development
practices as well! After reviewing each feature for the purpose of
semantic blogging, we will retain or extend the following features.

The features listed here are not thourougly tested.  There is a likelyhood of misbehavior. 

* Comments
* Sitemaps
* Archives views
* Related entries
* Private entries
* RSS or Atom Feeds
* Tags 
* Advanced search engine
* Prepublication and expiration
* Editing in MarkDown, Textile or reStructuredText
* Widgets (Popular entries, Similar entries, ...)
* Spam protection with Akismet or TypePad
* Admin dashboard
* MetaWeblog API, xmlrpc
* Ping Directories
* Ping External links
* Bit.ly support
* Twitter support
* Gravatar support
* Django-CMS plugins
* Collaborative work
* Tags autocompletion
* Entry model extendable
* Pingback/Trackback support
* Blogger conversion utility
* WordPress conversion utility
* WYMeditor, TinyMCE and MarkItUp support
* Ready to use and extendables templates
* Windows Live Writer compatibility

Examples
========

A sandbox site will give you a preview of the application.  Visit http://sbox.gnowledge.org/

Project Page
============

The project management is done from Savannah: https://savannah.gnu.org/projects/gnowsys/

Mailing list
============

Join this list if you are intersted in using or contributing as a hacker.

http://gnowledge.org/cgi-bin/mailman/listinfo/gnowsys-dev
