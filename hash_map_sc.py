# Name: Christian Simonian
# OSU Email: simoniac@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/15/2023
# Description: HashMap class using linked list. Class contains methods:
# put, table_load, empty_buckets,  resize_table, get
# contains_key, remove, clear, get_keys_and_values
# Outside the class a find_mode function is implemented


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key / value pair in the hash map. If the key already exists
        in the hash map, its associated value must be replaced with the new value.
        If the key is not in the hashmap, a new key / value pair must be added.
        Table must be resized to double its current capacity when this method is called
        and the current load factor of the table is greater than or equal to 1.0

        :param: Key and value object to add to the hashmap
        :return: None
        """
        if self.table_load() >= 1:
            new_cap = self._capacity * 2
            self.resize_table(new_cap)

        hash_val = self._hash_function(key)
        index = hash_val % self._capacity
        # represents linked list as whole for each index
        chain = self._buckets.get_at_index(index)
        existing_node = chain.contains(key)
        if existing_node is not None:
            existing_node.value = value
        else:
            chain.insert(key, value)
            self._size = self._size + 1

    def empty_buckets(self) -> int:
        """
        Method returns the number of empty buckets in
        the hash table

        :param: None
        :return: Integer representing the number of empty buckets in the hash table
        """
        empty = 0
        for idx in range(self._buckets.length()):
            if self._buckets.get_at_index(idx).length() == 0:
                empty += 1
        return empty

    def table_load(self) -> float:
        """
        Returns the current hash table load factor

        :param: None
        :return: Float value representing the load factor
        """
        if self._buckets.length() == 0:
            return 0.0
        load_factor = self._size / self._buckets.length()
        return load_factor

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change
        the underlying hash table capacity

        :param: None
        :return: None
        """
        self._buckets = DynamicArray()
        self._size = 0
        # sets the whole capacity of the dynamicArray with a LinkedList in each bucket
        for idx in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity of the internal hash table.
        All existing key / value pairs must remain in the new hash map
        and all hash table links must be rehashed.
        If new_capacity is less than 1 do nothing. Otherwise, make sure
        it is a prime number. If it is not then change it to the next prime number.

        :param: integer representing the new capactiy for the bucket
        :return: None
        """
        if new_capacity < 1:
            return
        elif new_capacity >= 1 and not self._is_prime(new_capacity):
            cap = self._next_prime(new_capacity)

        elif new_capacity >= 1 and self._is_prime(new_capacity):
            cap = new_capacity
        # save the old bucket
        old_bucket = self._buckets
        # empty the bucket to make one with greater capacity
        self._buckets = DynamicArray()
        self._capacity = cap
        # clear sets the size to 0 but then appends a LinkedList class
        # to each bucket for the whole capacity of the dynamic array
        self.clear()
        for idx in range(old_bucket.length()):
            # do not need to check if empty bc iterator does that and will skip if empty
            for val in old_bucket.get_at_index(idx):
                current_node = val
                self.put(current_node.key, current_node.value)

    def get(self, key: str):
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None

        :param: Key to search for
        :return: The keys value. If key id noy in the hashmap then return None
        """
        # find bucket in constant time with hash_val and index
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity
        temp = self._buckets.get_at_index(index).contains(key)
        if temp is not None:
            return temp.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map
        Otherwise it returns False

        :param: Key to search for
        :return: Boolean. True is found, false if not.
        """
        # find bucket in constant time with hash_val and index
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity
        temp = self._buckets.get_at_index(index).contains(key)
        # if temp is empty return False other it will return True
        return temp is not None

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hashmap, the method does nothing.

        :param: Key to search for and remove if found
        :return: None
        """
        # find bucket in constant time with hash_val and index
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity
        if self.contains_key(key):
            self._buckets.get_at_index(index).remove(key)
            self._size = self._size - 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple
        of a key / value pair stored in the hashmap.

        :param: None
        :return: DynamicArray containing tuples of key value pairs
        """
        my_arr = DynamicArray()
        for idx in range(self._buckets.length()):
            for node in self._buckets.get_at_index(idx):
                my_arr.append((node.key, node.value))
        return my_arr


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives a DynamicArray which is not guaranteed to be sorted. Function
    will return a tuple containing, in this order, a dynamic array comprising
    the mode (most occurring) value(s) of the given array, and an integer representing
    the highest frequency of occurrence for the mode value(s)

    param: DynamicArray
    return: Tuple consisting of a dynamicArray and an integer representing
    the number of occurrences
    """
    map = HashMap()
    max_count = 0
    mode_values = DynamicArray()

    # traverse through the dynamic array
    for idx in range(da.length()):
        key = da.get_at_index(idx)

        # if the value from the dynamic array is already
        # a key in the hash map then add 1 to the value
        if map.contains_key(key):
            occurrence = map.get(key)
            map.put(key, occurrence + 1)
        # if not found in hashmap add it and initialize its
        # value to 1
        elif not map.contains_key(key):
            map.put(key, 1)

        # if a keys value is greater than the max_count
        if map.get(key) > max_count:
            # set the new max_count to the keys value
            max_count = map.get(key)
            # create new DynamicArray and add key to it
            mode_values = DynamicArray()
            mode_values.append(key)

        # if a keys value is equal to the max count append it to the
        # mode_values array
        elif map.get(key) == max_count:
            mode_values.append(key)

    return mode_values, max_count

    # map.put(node.key, node.value)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
