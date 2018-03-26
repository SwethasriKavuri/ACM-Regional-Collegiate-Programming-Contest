import sys
class Square:
    def __init__(self, val):
        if val != '-':
            self.val = int(val)
        else:
            self.val = '-'

        self.range = None


class Grid:
    def __init__(self, grid, empty_pos, r, c):
        self.grid = grid
        self.to_do = empty_pos
        self.rows = r
        self.cols = c

    def acceptable(self, val, r, c):
        dirs = (-1, 0, 1)
        for i in dirs:
            for j in dirs:
                if i + r >= 0 and j + c >= 0 and i + r < self.rows and j + c < self.cols:
                    if self.grid[i + r][j + c].val == val:
                        return False

        return True

    def solve(self):
        if len(self.to_do) == 0:
            return True

        r, c = self.to_do.pop(0)
        for i in range(len(self.grid[r][c].range)):
            val = self.grid[r][c].range.pop(i)
            if self.acceptable(val, r, c):
                self.grid[r][c].val = val
                # print(r, " ", c, " ", val)
                if self.solve():
                    return True

                self.grid[r][c].val = '-'

            self.grid[r][c].range.insert(i, val)

        self.to_do.insert(0, (r, c))
        return False

    def dump(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                print (self.grid[r][c].val, " ", end ='')

            print ()

        # for a in self.to_do:
        #    print(a)


class Problems:
    def __init__(self, input_file):
        questions = open(input_file, 'r')
        lines = questions.readlines()
        questions.close()

        self.num_problems = int(lines[0].rstrip())
        self.problem_list = []

        j = 1
        for i in range(self.num_problems):
            ind, rows, cols = lines[j].rstrip().split(' ')
            grid = []
            empty_pos = []
            r = rows
            for q in range(int(r)):
                j += 1
                lines[j] = lines[j].rstrip()
                row_vals = lines[j].split(' ')
                grid.append([])
                c = 0
                for val in row_vals:
                    grid[-1].append(Square(val))
                    if val == '-':
                        empty_pos.append((q, c))

                    c += 1

            j += 1
            num_cells = int(lines[j].rstrip())
            for q in range(num_cells):
                j += 1
                temp = lines[j].rstrip().split(' ')
                val_range = int(temp[0])
                val_list = []
                for values in range(1, val_range + 1):
                    val_list.append(values)
                for count in range(val_range):
                    box = temp[1 + count]
                    box = box[1:-1]
                    r, c = box.split(',')
                    r = int(r) - 1
                    c = int(c) - 1
                    if grid[r][c].val != '-':
                        val_list.remove(grid[r][c].val)

                    grid[r][c].range = val_list

            j += 1

            self.problem_list.append(Grid(grid, empty_pos, int(rows), int(cols)))

    def dump(self):
        i = 1
        for p in self.problem_list:
            print(i)
            p.dump()
            i += 1

    def solve(self):
        for p in self.problem_list:
            p.solve()


temp = Problems(sys.argv[1])
temp.solve()
temp.dump()
