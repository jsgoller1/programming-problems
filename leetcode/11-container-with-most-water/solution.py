"""
Given n non-negative integers a1, a2, ..., an , where each represents a point at coordinate (i, ai),
n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0).

Translation: in the given array, the values are the heights of the lines. (see picture)

Find two lines, which together with x-axis forms a container, such that the container contains the most water.

Note: You may not slant the container and n is at least 2.

Example:
Input: [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: There are 6 partitions in between in[1] (8) and in[-1] (7); as such, there are 7 columns that could be filled with water. Because
7 is lower of the two, we can fill 7 columns with 7 units of water (imagine the intermediary lines are very porous and take up no space themselves)
resulting in 49.

Constraints:
  - You cannot "slant" the container (i.e. have a diagonal water surface maybe?)
  - n >= 2
----------------------------
Cases:
  1: [1, 8, 6, 2, 5, 4, 8, 3, 7]          (pick arr[1] and arr[-1])
  2: [2, 1, 8, 6, 2, 5, 4, 8, 3, 7, 1, 2] (pick arr[2] and arr[-3])
  3: [1, ..., 99, 1, 1, 99, ..., 1]       (pick 8s)
  4: [1, 1, 1, 1, 1]                      (pick first and last)
  5: [1,1,1,1,1,1,2,2]                    (pick first and last)
  6: [5,1,10,1,10,1,5]                    (pick outermost 5s)
  7: [4,1,10,1,10,1,4]                    (pick outermost 4s - 24)

- Brute force:
  - count the amount of water for every possible combination O(n^2)
- Trapping Rainwater can be done in O(N) time by using a stack, but that catches _all_ rainwater.
  - Also, doing the two-passes with the stacks would give us the two 8-height lines, which is wrong
- Do we need to examine every pair?
  - Probably not; we should be able to reach a point where "this could never be greater"
  - Can't sort
- We do need to look at every line at least once
- If we pick two lines, there is no way to catch more water by picking any lines in between that are shorter; could by picking greater.
  - if we pick the two maxes, we don't need to look any further inwards for better lines
  - what do we need to do so we know we don't need to look outwards? Is there a way to quickly disqualify remaining elements
- Suppose we've picked the maxes in [...,20,...21,6,7,8,9], which are 20 and 21. Reapplying the same logic,
 there is no reason to pick any line with a taller/equal line to its right; 6,7, and 8 cannot be the correct answer.
 Same logic applies to other side as well. However this is still problematic with [...,20,...21,10,9,8,7]
- Suppose we had a 10 element array ending in 7. Picking this a side, the greatest possible
value of caught water is 70. Call this a "positional max" - the highest value possible given its position in the array.
- Once we locate a max, if we find the positional max between it and the end of the array, there is no reason to consider
any other values as bounds between the max and the array end.

------------------------------------
Plan:

"Two pointers" approaches:
- What if starting at outermost, we determine if moving either inwards results in a better solution?
  - Would fail on case #2

- Start in the middle and work outwards
  - [1, 8, 6, 2, 5, 4, 8, 3, 7]
                 5, 4
                   [4, 10,12,16]  right edge given left is 5
    [5  16 12 4  4]               left edge given right is 4

  - correct on case #1
  - Would break on case #3
- Start with the array maxes and work outwards
  - correctly does cases 1-5
  - Could this strategy be tricked into picking the wrong elements?
    - Fails #7
       max is 24 with outermost 4s, but strategy picks 20 with two 10s.
- Start with outermost and look no further inwards than maxes; only replace if we find a boundary that is better than the outermost
    - passes 1,4-7, fails 2 and 3

- Obtain maxes in array, then get positional maxes between each and array end, then return greatest of:
  - left max, right max
  - left pmax, right max
  - left max, right pmax
  - left pmax, right pmax

--------
Review:
- Finding maxes and pos maxes is SUPER complicated.
- Do we even need to find "maxes"? Is finding just the positional maxes sufficient?
  - No, there are cases where the positional max is not the correct choice.
------------------------------
Got asked this again in a mock interview and screwed it up again; reimplemented the correct answer for practice.
"""

class Solution:
    def maxArea(self, heights):
        l = 0
        r = len(heights)-1
        area = -1
        while l < r:
            area = max(area, min(heights[l], heights[r]) * abs(l - r))
            if heights[l] <= heights[r]:
                l += 1
            else:
                r -= 1
        return area

if __name__ == '__main__':
    s = Solution()
    cases = [
        # (pick arr[1] and arr[-1])
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        # (pick arr[2] and arr[-3])
        ([2, 1, 8, 6, 2, 5, 4, 8, 3, 7, 1, 2],49),
        # (pick 99s)
        ([1, 1, 1, 1, 99, 1, 1, 99, 1, 1, 1, 1],297),
        # (pick first and last)
        ([1, 1, 1, 1, 1],4),
        # (pick first and last)
        ([1, 1, 1, 1, 1, 1, 2, 2],7),
        # (pick outermost 5s)
        ([5, 1, 10, 1, 10, 1, 5],30),
        # (pick outermost 4s - 24)
        ([4, 1, 10, 1, 10, 1, 4],24),
        # pick leftmost 10 and right 7
        ([4, 1, 10, 1, 10, 1, 7],28),
        # pick leftmost 2 and right 3
        ([1, 2, 4, 3], 4),
        # pick 10s
        ([1, 10, 1, 11, 1, 10, 1], 40),
        # ????
        ([76,155,15,188,180,154,84,34,187,142,22,5,27,183,111,128,50,58,2,112,179,2,100,111,115,76,134,120,118,103,31,146,58,198,134,38,104,170,25,92,112,199,49,140,135,160,20,185,171,23,98,150,177,198,61,92,26,147,164,144,51,196,42,109,194,177,100,99,99,125,143,12,76,192,152,11,152,124,197,123,147,95,73,124,45,86,168,24,34,133,120,85,81,163,146,75,92,198,126,191], 18048),
        #
        ([2,3,4,5,18,17,6],17)
    ]
    for case in cases:
      assert s.maxArea(case[0]) == case[1]
