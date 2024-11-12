class Solution:
    def isHappy(self, n: int) -> bool:
        seen = set()
        next_n = self.square_sum_digits(n)
        while not next_n in seen:
            if next_n == 1:
                return True
            seen.add(next_n)
            next_n = self.square_sum_digits(next_n)
            print(next_n)
        return False

    def square_sum_digits(self, n):
        squares = [d ** 2 for d in self.digits(n)]
        return sum(squares)
    
    def digits(self, n):
        current = n
        while True:
            q, r = divmod(current, 10)
            yield r
            if q == 0:
                break
            current = q



s = Solution()
print([s.isHappy(n) for n in (2,)])
