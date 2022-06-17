def generateDescriptor(row: list):
    """Generate a row descriptor from a list of pixels"""
    descriptor = []
    i = 0
    for p in row:
        if p:
            i += 1
        if not p and i > 0:
            descriptor.append(i)
            i = 0
    if i != 0:
        descriptor.append(i)
    if len(descriptor) == 0:
        return []
    return descriptor


def generatePossibleCombinationsForRow(descriptor: list, size: int):
    """Generate all possible combinations for a row. Size is size of
    the row meaning width of horizontal and height for vertical rows."""
    pixelsInRow = sum(descriptor)
    for bitCombination in range(2**size):
        if bin(bitCombination).count("1") != pixelsInRow:
            continue
        if descriptor == generateDescriptor(list(map(lambda x: bool(int(x)), list(f"{bitCombination:0{size}b}")))):
            print(list(map(lambda x: bool(int(x)), list(f"{bitCombination:0{size}b}"))))

