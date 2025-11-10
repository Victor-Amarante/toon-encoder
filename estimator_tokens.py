from toon_format import estimate_savings, compare_formats, encode

# Measure savings
data = {
  "company": "Tech Corp",
  "employees": [
    {
      "id": 101,
      "name": "Alice",
      "department": "Engineering"
    },
    {
      "id": 102,
      "name": "Bob",
      "department": "Marketing"
    }
  ]
}

results = estimate_savings(data)
print(results)

print(compare_formats(data))

toon_str = encode(data)
print(toon_str)