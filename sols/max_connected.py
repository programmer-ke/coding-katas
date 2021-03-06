class Solution:
    def maxConnected(self, grid):
        maxCount = 0
        for y in range(0, len(grid)):
            for x in range(0, len(grid[y])):
                count = self.__traverse(grid, x, y, {})
                maxCount = max(count, maxCount)
        return maxCount

    def __traverse(self, grid, x, y, seen):
        return self.__traverseHelper(grid, x, y, 0, seen)

    def __traverseHelper(self, grid, x, y, count, seen):
        key = "%s,%s" % (x, y)
        if seen.get(key) is not None:
            return 0
        seen[key] = True

        color = grid[y][x]
        neighbors = self.__getNeighbors(grid, x, y)
        sum_ = 1
        for point in neighbors:
            i = point[0]
            j = point[1]
            if grid[j][i] != color:
                continue
            seen[key] = True
            # sum_ += self.__traverseHelper(grid, i, j, 1, seen)
            sum_ += self.__traverseHelperIterative(grid, i, j, 1, seen)
        return sum_

    def __traverseHelperIterative(self, grid, x, y, count, seen):
        color = grid[y][x]
        sum_ = 0
        stack = []
        stack.append([x, y])
        while len(stack) > 0:
            p = stack.pop()
            item_x = p[0]
            item_y = p[1]
            key = "%s,%s" % (item_x, item_y)
            if seen.get(key) is not None:
                continue
            if grid[item_y][item_x] != color:
                continue
            seen[key] = True
            sum_ = sum_ + 1
            neighbors = self.__getNeighbors(grid, item_x, item_y)
            for point in neighbors:
                stack.append([point[0], point[1]])
        return sum_

    def __getNeighbors(self, grid, x, y):
        coords = []
        neighbors = [
            [-1, 0],
            [0, -1],
            [1, 0],
            [0, 1],
        ]
        for n in neighbors:
            coordX = x + n[0]
            coordY = y + n[1]
            if (
                coordX < 0
                or coordY < 0
                or coordY >= len(grid)
                or coordX >= len(grid[0])
            ):
                continue
            coords.append([coordX, coordY])
        return coords


grid = [["r", "g", "b"],
        ["r", "r", "r"],
        ["g", "g", "r"]]

print(Solution().maxConnected(grid))
