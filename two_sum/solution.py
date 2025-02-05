from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = {} 
        for i,p in enumerate(nums):
            if target-p in d: # search its partner
                return [d[target-p],i]
            d[p] = i