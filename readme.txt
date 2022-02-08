README - Sudoku assignment overview

	The algorithm that was used in the solution is a mix of two problems. Constraint Satisfaction and Depth-First Search.
	
	The first step was to work out all the possible values of empty cells based on the existing ones.
	This could be represented in a simple 9x9x9 array that would be an extension of the existing 9x9 sudoku array.
	This 9x9x9 array is going to be referenced by the term 'possibilities' as it stores all possible values of an unsolved
	sudoku at a given state. 
	This approach allows to eliminate all the existing cells from the equation. From now on, all what's being considered are
	the	'empty' cells. They are going to be referenced as 'blanks' from now on.
	
	The second step would be to search for the easiest blanks to solve and eliminate them from the process. 
	These would be ones that have only one possibility left following the initial constraint assignment. They are as good
	as solved and can be treated like filled cells and be ignored in the next section of the algorithm.
	
	It's worth mentioning that the key to this algorithm is to update the constraints after every value assignment.
	In other words, as soon as a blank has only one possibility left in it's own possibility array (one non-zero value),
	it is treated as filled and completed. Then the algorithm updates the possibility array for other values that were constraint
	by this value. The solution is treated as incorrect, if a blank has no non-zero values left in its possibility array.
	
	The last step is the heart of the whole algorithm - Depth-First search with dynamic constraints.
	Here lays a classic backtracking recursive algorithm, that is iterating through all possible values of one blank
	and calls itself based on an assumption that this blank is a correct solution. If the solution is found to be incorrect,
	the algorithm assigns another value and calls itself again.
	Normally, this would be a very inefficient process, but because the algorithm is iterating through all possibilities 
	that are being dynamically updated, the processing time is way shorter than in a regular Depth-First search algorithm.
	
	The time complexity of this algorithm is proportional to the difficulty of the puzzle and it may be represented as
	O(b^n + c), where 'b' represents the branching factor, 'n' represents the number of blanks at the point of calling the
	recursive search function and 'c' represents the number of 'easy' blanks that can be eliminated with little computing power.
	It's worth mentioning that the bigger 'c' is, the shorter 'n' gets, so it is an improvement over the basic Depth-First
	search with O(b^m), where m = n+c. In that case O(b^n + c) will always be more efficient.
	
	The space complexity of this algorithm stays O(b*n) and something to improve would definitely be the possibility array itself.
	9x9x9 array is relatively a big memory load and some work could be done to improve the memory structure. It could be reduced
	to just 9x9 array, but of a dynamic type where integer type would indicate only completed cells and the array of possibilities
	would accompany the blanks. This time without unnecessary zeroes that would take 90% of the completed sudoku possibility array.
	
	Further time could be gained if the algorithm could detect phenomena such as 'Naked Twins'. That way it could save up some
	processing time by jumping straight to a conclusion. Implementing more features like this, that are based on the pure sudoku
	knowledge would be greatly beneficial.
	However for now, the algorithm has achieved a satisfactory level of performance and can deal with the hardest sudoku puzzles
	in a matter of seconds.
	