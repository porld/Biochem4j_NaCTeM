import json, uuid, sys
from pprint import pprint
from neo4j.v1 import GraphDatabase

'''
This script links text mined chemicals to Biochem4j chemicals
'''

VERSION = str(sys.argv[1])
print('Version:',VERSION)

PASSWORD = sys.argv[2]

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", PASSWORD))

#Load predictions JSON
with open('reactant_product_data.json') as f:
    data = json.load(f)

#Collect chemical nodes
chemicals = [] #Collect all the identifiers associated with each chemical
for reaction in data['reaction']:

	#Reactant
	reactant_id = reaction['reactant_id']
	chemicals.append(reactant_id)
	
	#Product
	product_id = reaction['product_id']
	chemicals.append(product_id)
		
#Create all the chemical nodes
chemicals = sorted(list(set(chemicals)))
for chem in chemicals:
	identifiers = chem.split('|')
	for id in identifiers:
		if 'CHEBI' in id:
			print(id)
			with driver.session() as session:
				session.run('MATCH (tmchem:TMchemical {id: "' + chem + '", version: "' + VERSION + '"}), (bjchem:Chemical {id: "' + id + '"}) CREATE (tmchem)-[:TMgrounding]->(bjchem)')
			session.close()
