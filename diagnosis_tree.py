graph = {
    "Diabetes": ["Hyperglykämie", "HbA1c"],
    "Hyperglykämie": ["Insulin"],
    "HbA1c": [],
    "Insulin": []
}

def explore_concepts(graph, start):
  result = []
  stack = [start]
  visited = []

  while stack:
    current = stack.pop()
    if current not in visited:
      visited.append(current)
      result.append(current)

      for neighbor in graph[current]:
        if neighbor not in visited and neighbor not in stack:
          stack.append(neighbor)

  return result

print(explore_concepts(graph, "Diabetes"))