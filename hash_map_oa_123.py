# Name: Christian Simonian
# OSU Email: simoniac@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/15/2023
# Description:

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        and the current load factor of the table is greater than or equal to 0.5

        :param: Key and value object to add to the hashmap
        :return: None
        """
        # if self.table_load() >= 0.5:
        #     new_cap = self._capacity * 2
        #     self.resize_table(new_cap)
        #
        # hash_val = self._hash_function(key)
        # j_counter = 0
        # no_available = True
        #
        # while no_available is True:
        #     index = (hash_val + j_counter ** 2) % self.get_capacity()
        #     temp = self._buckets.get_at_index(index)
        #     entry = HashEntry(key, value)
        #
        #     if temp is None:
        #         no_available = False
        #         self._buckets.set_at_index(index, entry)
        #         self._size = self._size + 1
        #
        #     if key == self._buckets.get_at_index(index).key:
        #         no_available = False
        #         if self._buckets.get_at_index(index).is_tombstone is True:
        #             self._size = self._size + 1
        #         self._buckets.set_at_index(index, entry)
        #     j_counter += 1


        if self.table_load() >= 0.5:
            new_cap = self._capacity * 2
            self.resize_table(new_cap)

        hash_val = self._hash_function(key)
        j_counter = 0
        no_available = True

        while no_available is True:
            index = (hash_val + j_counter ** 2) % self.get_capacity()
            temp = self._buckets.get_at_index(index)
            entry = HashEntry(key, value)

            if temp is None:
                no_available = False
                self._buckets.set_at_index(index, entry)
                self._size = self._size + 1

            if key == self._buckets.get_at_index(index).key:
                no_available = False
                if self._buckets.get_at_index(index).is_tombstone is True:
                    self._size = self._size + 1
                self._buckets.set_at_index(index, entry)
            j_counter += 1



    def quadratic_prob_helper(self, key: str) -> int:
        """
        Takes in a key and returns the quadratic
        prob of that key

        :param: Key
        :return: Integer representing the index
        """
        hash_val = self._hash_function(key)
        j_counter = 0
        index = (hash_val + j_counter ** 2) % self._capacity
        while self._buckets.get_at_index(index) is not None and self._buckets.get_at_index(index).is_tombstone is False:
            if self._buckets.get_at_index(index).key == key:
                return index
            else:
                j_counter += 1
                index = (hash_val + j_counter ** 2) % self._capacity
        return index





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

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table

        :param: None
        :return: Integer representing the number of empty buckets in hash table
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity of the internal hash table.
        All existing key / value pairs must remain in the new hash map
        and all hash table links must be rehashed.
        If new_capacity is less than the current number of elements do nothing.
        Otherwise, make sure it is a prime number. If it is not then change it to the next prime number.

        :param: integer representing the new capactiy for the bucket
        :return: None
        """

        if new_capacity < self._size:
            return

        elif not self._is_prime(new_capacity):
            cap = self._next_prime(new_capacity)

        elif self._is_prime(new_capacity):
            cap = new_capacity

        old_bucket = self._buckets
        # empty the bucket to make one with greater capacity
        self._buckets = DynamicArray()
        self._capacity = cap
        self._size = 0

        # have to fill the whole bucket (which is a DynamicArray) with None
        # this avoids out of bound errors
        for idx in range(self._capacity):
            self._buckets.append(None)

        for idx in range(old_bucket.length()):
            if old_bucket.get_at_index(idx) is not None and old_bucket.get_at_index(idx).is_tombstone is False:
                entry = old_bucket.get_at_index(idx)
                self.put(entry.key, entry.value)

    def get(self, key: str) -> object:
        """
        Method returns the value associated with the given key.
        If the key is not in HashMap return None

        :param: Key to search for
        :return: Value associated with that key if found. None if not in HashMap.
        """
        index = self.quadratic_prob_helper(key)
        temp = self._buckets.get_at_index(index)
        # ensure that the index has a value and that it has not been removed
        if temp is not None and temp.is_tombstone is False:
            return temp.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True of the given key is in the hashmap.
        Otherwise, returns False

        :param: Key
        :return: Boolean, True if found, False otherwise.
        """
        index = self.quadratic_prob_helper(key)
        temp = self._buckets.get_at_index(index)
        if temp is not None:
            if temp.key == key:
                return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value
        from the HashMap. It then sets self.is_tombstone to True
        If key is not in HashMap method does nothing.

        :param: Key to remove
        :return: None
        """
        if not self.contains_key(key):
            return None

        no_available = True
        j_counter = 0
        hash_val = self._hash_function(key)
        while no_available is True:

            index = (hash_val + j_counter ** 2 ) % self.get_capacity()
            temp = self._buckets.get_at_index(index)

            if key == self._buckets.get_at_index(index).key:
                if temp is True:
                    return
                self._buckets.get_at_index(index).is_tombstone = True
                self._buckets.set_at_index(index, self._buckets.get_at_index(index))
                self._size = self._size - 1
                return

            if temp is None:
                return
            if self._buckets.length() <= index:
                return

            j_counter += 1


    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change
        the underlying hash table capacity

        :param: None
        :return: None
        """
        self._buckets = DynamicArray()
        self._size = 0
        for idx in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method returns a dynamic array where each index contains
        a tuple of a key / value pair stored in the hash map.

        :param: None
        :return: DynamicArray filled with key value pairs
        """
        my_arr = DynamicArray()
        for idx in range(self._buckets.length()):
            temp = self._buckets.get_at_index(idx)
            if temp is not None and temp.is_tombstone is False:
                my_arr.append((temp.key, temp.value))
        return my_arr

    def __iter__(self):
        """
        Method enables the hashmap to iterate across itself.

        :param: None
        :return: None
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Method will return the next item in the hash map
        based on the current location of the iterator.

        :param: None
        :return: None
        """
        try:
            temp = self._buckets.get_at_index(self._index)
            while temp is None or temp.is_tombstone:
                self._index = self._index + 1
                temp = self._buckets.get_at_index(self._index)
        except DynamicArrayException:
            raise StopIteration
        self._index = self._index + 1
        return temp


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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
    m = HashMap(223, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.put('key709', -869)
    # m.remove('key709')
    # # m.remove('key4')
    m.put('key83', 854)
    m.put('key110', 912)
    m.put('key210', -148)
    m.put('key500', -27)
    m.put('key312', -797)
    m.put('key322', 245)
    m.put('key260', 507)
    m.put('key170', 822)

    m.put('key712', 134)
    m.put('key136', 260)
    m.put('key344', -646)
    m.put('key453', -144)
    m.put('key724', 722)
    m.put('key546', -808)
    m.put('key174', -98)
    m.put('key727', -206)
    m.put('key386', 802)
    m.put('key865', 311)
    m.put('key299', -236)
    m.put('key926', -980)
    m.put('key472', -501)
    m.put('key464', 485)
    m.put('key168', -250)
    m.put('key540', 433)
    m.put('key895', -879)
    m.put('key981', 55)
    m.put('key372', -856)
    m.put('key587', -485)
    m.put('key948', 507)
    m.put('key886', -291)
    m.put('key583', 381)
    m.put('key296', -375)
    m.put('key702', 206)
    m.put('key685', -30)
    m.put('key452', -163)
    m.put('key894', 725)
    m.put('key607', 445)
    m.put('key275', 807)
    m.put('key339', 379)
    m.put('key178', -565)
    m.put('key396', -441)
    m.put('key982', 610)
    m.put('key423', 560)
    m.put('key604', 259)
    m.put('key812', 828)
    m.put('key571', -937)
    m.put('key356', -347)
    m.put('key717', 162)
    m.put('key448', 282)
    m.put('key819', -785)
    m.put('key838', -262)
    m.put('key421', 356)
    m.put('key305', 123)
    m.put('key226', -74)
    m.put('key623', 286)
    m.put('key634', -411)
    m.put('key555', 50)
    m.put('key212', -154)
    m.put('key474', 116)
    m.put('key4', 339)
    m.put('key45', -29)
    m.put('key29', 293)
    m.put('key93', 224)
    m.put('key58', 91)
    m.put('key95', -259)
    m.put('key74', -388)
    m.put('key97', -813)
    m.put('key65', 69)
    # print(m.__str__())
    m.remove('key170')
    # print(m.__str__())
    # my_list = []
    # for h in m._buckets:
    #     if h is not None:
    #         print(h.key)

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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
