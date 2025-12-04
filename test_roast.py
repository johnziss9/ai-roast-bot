from modules.generator import RoastGenerator

print("Testing Roast Generator...")
print("-" * 50)

generator = RoastGenerator()
roast = generator.generate_roast()

print("Generated Roast:")
print(roast)
print("-" * 50)
