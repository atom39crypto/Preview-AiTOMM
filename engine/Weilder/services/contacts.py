import csv

# Initialize the dictionaries for contact, website, and apps
contact = {}
website = {}
apps = {}

# Open and read the CSV file
with open('engine/Weilder/services/data.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        # Read the role, name, and value from each row
        role = row['role'].lower()  # Convert to lowercase for consistency
        name = row['name']
        value = row['value']
        
        # Assign the values to the appropriate dictionary based on the role
        if role == 'contact':
            contact[name] = value
        elif role == 'website':
            website[name] = value
        elif role == 'apps':
            apps[name] = value

# Output the dictionaries
print(apps)