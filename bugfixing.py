"""
The problem occurs when unequal columns are introduced into the program (usually in the fort.30 file).

The current idea is to create a table that consists of the largest subarray that would fit into the 122,3,3,2 array.

Then, the excess is made into a second array.

This should be then padded out with None values so that you have a (3,3,2) array. Then I guess it could be added onto
the first array to create the 123,3,3,2 array.

Or this could be just an extra value that is iterated over if the column count is unevevn in the iterate_array function.
"""