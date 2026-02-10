import sys

def readinventory(filename):
    """Read phoneme inventory and store in a dictionary."""
    featdict = {}
    allsegments = set()

    with open(filename, encoding='utf-8') as f:
        lines = [line.strip() for line in f]
    fields = lines[0].split()
    for f in fields:
        featdict[f] = {}
        featdict[f]['name'] = f
        featdict[f]['+'] = set()
        featdict[f]['-'] = set()
    for i in range(1, len(lines)):
        thisline = lines[i]
        if len(thisline) == 0:
            continue
        linefields = thisline.split()
        if len(linefields) != len(fields) + 1:
            print("Field length mismatch on line " + str(i+1))
            sys.exit(1)
        phoneme = linefields[0]
        allsegments |= {phoneme}
        for j in range(1,len(linefields)):
            if linefields[j] == '+' or linefields[j] == '-':
                featdict[fields[j-1]][linefields[j]] |= {phoneme}

    return featdict, allsegments

    
def reccheck(fd, basefeats, basemodes, feats, modes, correct, baseindex):

    def store_feats(fd, feats, modes):
        """Store features for one solution in dictionary indexed by length."""
        global solutions
        length = len(feats)
        if length not in solutions:
            solutions[length] = []
        thissol = []
        for idx, feat in enumerate(feats):
            thissol.append(modes[idx] + fd[feat]['name'])
        solutions[length].append('[' + ','.join(thissol) + ']')
        if verbose:
            print('[' + ','.join(thissol) + ']')
            
    def check_feats(fd, feats, modes, correct):
        """Check if proposed feature combination is a valid solution."""
        newbase = allsegments
        for idx, feat in enumerate(feats):
            mode = modes[idx]
            newbase = newbase & fd[feat][mode]
        if newbase != correct:
            return False
        return True
        
    global maxlen
    if len(feats) > maxlen: # Bound the search
        return
    if check_feats(fd, feats, modes, correct): # New solution
        store_feats(fd, feats, modes)
        if len(feats) < maxlen:
            maxlen = len(feats)
    numelem = len(basefeats)
    for i in range(baseindex, numelem):  # Add one feature
        if basefeats[i] not in feats:    # If we didn't add this already
            reccheck(fd, basefeats, basemodes, feats + [basefeats[i]], modes + [basemodes[i]], correct, i + 1)
    return

def greedy(fd, basefeats, basemodes, correct):
    """Implement greedy search based on C.

    Greedily choose compatible feature specifications that minimize overgeneration,
    tracking the current candidate set as an intersection of chosen specs.
    """
    candidate = allsegments
    chosen = []
    while True:
        sols = []
        if verbose:
            print("===============================")
        for f, m in zip(basefeats, basemodes):
            newcandidate = candidate & fd[f][m]
            extrasegs = newcandidate - correct
            length = len(extrasegs)
            if verbose:
                print("Len of " + fd[f]['name'] + " is " + str(length))
            sols.append((newcandidate, fd[f]['name'], length, m))
        bestsol = min(sols, key=lambda x: x[2])
        candidate = bestsol[0]
        chosen.append(bestsol[3] + bestsol[1])

        if candidate == correct:
            break
    print("Greedy solution:", chosen)


##############################################################################

if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " [-v] inventoryfile phonemeset")
    sys.exit(1)

verbose = False
i = 1
if sys.argv[1] == '-v':
    verbose = True
    i += 1
        
inventoryfile = sys.argv[i]
testset = set(sys.argv[i+1].split(','))

fd, allsegments = readinventory(inventoryfile)
features = [f for f in fd]

base = allsegments
feats, modes = [], []

print("Calculating C for phoneme set " + "{" + ','.join(testset) + "}")
for feat in features:
    if testset <= fd[feat]['+']:
        base = base & fd[feat]['+']
        print("+" + fd[feat]['name'], end=' ')
        feats.append(feat)
        modes.append('+')
    elif testset <= fd[feat]['-']:
        base = base & fd[feat]['-']
        print("-" + fd[feat]['name'], end=' ')
        feats.append(feat)
        modes.append('-')

print()

solutions = {}

if base == testset:
    print("Set is a natural class")
    print("Trying branch-and-bound")
    maxlen = len(feats)
    reccheck(fd, feats, modes, [], [], base, 0)
    minsol = min(solutions.keys())
    print("Minimal solution(s):")
    for s in solutions[minsol]:
        print(s)
    print("Trying greedy search")
    greedy(fd, feats, modes, base)
else:
    print("Set is not a natural class")
