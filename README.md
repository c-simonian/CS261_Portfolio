# CS261_Portfolio


# Part 1 of Project

# Description
This project implements an optimized HashMap class using dynamic arrays and linked lists for efficient collision resolution. 
The goal is to achieve O(1) average case performance for all operations while storing key/value pairs in a hash map.

# Features
put(): Insert a key/value pair into the hash map.
get(): Retrieve the value associated with a given key.
remove(): Remove a key and its associated value from the hash map.
contains_key(): Check if a key exists in the hash map.
clear(): Remove all key/value pairs from the hash map.
empty_buckets(): Count the number of empty buckets in the hash map.
resize_table(): Resize the hash map's underlying table.
table_load(): Calculate the current load factor of the hash map.
get_keys(): Retrieve a list of all keys in the hash map.
find_mode(): Find the most common value in the hash map.


# Implementation Details
The hash map is implemented using a DynamicArray object to store the hash table and LinkedList objects to handle collision resolution.
Two pre-written hash functions are provided and should be tested to ensure correct behavior.
The number of objects stored in the hash map is limited to between 0 and 1,000,000.
Built-in Python data structures and methods are not used; instead, the provided classes must be used for dynamic arrays and linked lists.
Direct access to variables of the DynamicArray or LinkedList classes is prohibited; only class methods should be used.
The project follows the restrictions and guidelines provided in the assignment source code.


# Part 2 of Project

# Description
This project implements an optimized HashMap class using dynamic arrays for the hash table and open 
addressing with quadratic probing for collision resolution. The goal is to achieve O(1) average case performance 
for all operations while storing key/value pairs in the hash map using open addressing.

# Features
put(): Insert a key/value pair into the hash map.
get(): Retrieve the value associated with a given key.
remove(): Remove a key and its associated value from the hash map.
contains_key(): Check if a key exists in the hash map.
clear(): Remove all key/value pairs from the hash map.
empty_buckets(): Count the number of empty buckets in the hash map.
resize_table(): Resize the hash map's underlying table.
table_load(): Calculate the current load factor of the hash map.
get_keys(): Retrieve a list of all keys in the hash map.
__iter__() and __next__(): Implement an iterator for the hash map.

# Implementation Details
The hash map is implemented using a DynamicArray object to store the hash table.
Open addressing with quadratic probing is used for collision resolution.
The number of objects stored in the hash map is limited to between 0 and 1,000,000.
Built-in Python data structures and methods are not used; only the provided DynamicArray class should be used.
Direct access to variables of the DynamicArray class is prohibited; only class methods should be used.
The project follows the restrictions and guidelines provided in the assignment source code.
