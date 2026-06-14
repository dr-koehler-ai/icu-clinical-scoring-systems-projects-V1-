graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E"],
    "D": [],
    "E": []
}

def infection_order(graph, start):
  result = []
  queue = [start]
  visited = []

  while queue:
    current = queue.pop(0)
    if current not in visited:
      visited.append(current)
      result.append(current)

      for neighbor in graph[current]:
        if neighbor not in visited and neighbor not in queue:
          queue.append(neighbor)

  return result

print(infection_order(graph, "C"))