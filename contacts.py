contacts = {
    "Patient A": ["Patient B", "Patient C"],
    "Patient B": ["Patient A", "Patient D"],
    "Patient C": ["Patient A"],
    "Patient D": ["Patient B"]
}

def count_contacts(graph):
  number_of_contacts = {}
  for person in graph:
    number_of_contacts[person] = len(graph[person])
  return number_of_contacts

print(count_contacts(contacts))