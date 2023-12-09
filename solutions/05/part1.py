FILE = 'inputs/05/input.txt'

class Almanac:

    def __init__(self, filename) -> None:
        self.seeds = []
        self.transforms_sets = []
        with open(filename, 'r') as infile:
            self.seeds = [int(num) for num in infile.readline().split(':')[1].strip().split()]
            infile.readline()
            infile.readline()
            transform_set = {}
            line = infile.readline()
            while line:
                line = line.strip()
                if not line:
                    pass
                elif line[0].isalpha():
                    self.transforms_sets.append(transform_set)
                    transform_set = {}
                else:
                    nums = [int(num) for num in line.split()]
                    key = (nums[1], nums[1] + nums[2])
                    if key in transform_set:
                        raise ValueError("scenario I didn't account for")
                    transform_set[key] = nums[0] - nums[1]
                line = infile.readline()
            if len(transform_set) > 0:
                self.transforms_sets.append(transform_set)
    
    def _get_seed_location(self, seed):
        i = seed
        for transform_set in self.transforms_sets:
            for transform in transform_set:
                if transform[0] <= i < transform[1]:
                    i = transform_set[transform] + i
                    break
        return i

    def get_min_location(self):
        return min(self._get_seed_location(seed) for seed in self.seeds) 

print(Almanac(FILE).get_min_location())
