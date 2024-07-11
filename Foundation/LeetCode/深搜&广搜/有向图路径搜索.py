import copy
from collections import deque, defaultdict


def longest_path(edges):
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    end_nodes = defaultdict(int)

    for start, end in edges:
        graph[start].append(end)
        in_degree[end] += 1
        in_degree[start] = in_degree.get(start, 0)
    all_path = set()
    start_nodes = ['A01']
    if in_degree['A01'] != 0:
        in_degree['A01'] += 1
    for start_node in start_nodes:
        queue = deque([(start_node, [start_node])])
        while queue:
            _in_degree = copy.deepcopy(in_degree)
            node, path = queue.popleft()
            for i in path:
                _in_degree[i] -= 1
            if not graph[node]:
                all_path.add(tuple(path))
            is_end = True
            for neighbor in graph[node]:
                if _in_degree[neighbor] > 0:
                    is_end = False
                    queue.append((neighbor, path + [neighbor]))
            if is_end:
                all_path.add(tuple(path))

    return [list(i) for i in all_path]


# edges = [["A01", "A02"], ["A02", "A03"], ["A02", "A04"], ["A04", "A05"], ["A05", "A02"], ["A03", "A06"]]
edges = [["A01", "A02"], ["A02", "A04"], ["A04", "A02"], ["A04", "A05"]]
# edges = [["A01", "A02"], ["A05", "A03"]]
# edges = [["A01", "A02"], ["A02", "A03"], ["A03", "A01"], ["A01", "A04"], ["A04", "A01"], ["A01", "A05"]]
# edges = [["A01", "A02"], ["A02", "A03"], ["A03", "A04"], ["A04", "A05"], ["A05", "A01"], ["A01", "A06"], ["A06", "A07"]]
# edges = [["A01", "A02"], ["A02", "A03"], ["A03", "A04"], ["A04", "A05"], ["A05", "A02"], ["A02", "A06"], ["A06", "A07"]]

result = longest_path(edges)
print(result)
