import json, uuid, sys
from pprint import pprint
from neo4j.v1 import GraphDatabase


VERSION = str(sys.argv[1])
print('Version:',VERSION)

PASSWORD = sys.argv[2]

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", PASSWORD))

#Load predictions JSON
with open('reactant_product_data.json') as f:
    data = json.load(f)

#Collect nodes
papers = []
chemicals = [] #Collect all the identifiers associated with each chemical
reactions = {}
for reaction in data['reaction']:

	#Reactant
	reactant_id = reaction['reactant_id']
	chemicals.append(reactant_id)
	
	#Product
	product_id = reaction['product_id']
	chemicals.append(product_id)
		
	#Paper
	paper = reaction['pmid']
	papers.append(paper)
	
#Create all the chemical nodes
chemicals = sorted(list(set(chemicals)))
print('Found',len(chemicals),'chemicals.')
for chem in chemicals:
	print('Making TMChemical node:', chem)
	with driver.session() as session:
		session.run('CREATE (c:TMchemical {id: "' + chem + '", version: "' + VERSION + '"}) RETURN c')
	session.close()
	
#Create all the publication nodes
papers = sorted(list(set(papers)))
print('Found',len(papers),'papers.')
for paper in papers:
	print('Making TMpaper node:', paper)
	with driver.session() as session:
		session.run('CREATE (p:TMpaper {pmid: "' + paper + '", version: "' + VERSION + '"}) RETURN p')
	session.close()

#Link up all the components of each reaction
for reaction in data['reaction']:
	#Reactant
	reactant_id = reaction['reactant_id']
	reactant_mention = reaction['reactant_mention']
	
	#Product
	product_id = reaction['product_id']
	product_mention = reaction['product_mention']
		
	#Paper
	paper = reaction['pmid']

	with driver.session() as session:
		#Link reactant to paper
		session.run('MATCH (paper:TMpaper {pmid:"' + paper + '", version:"' + VERSION + '"}), (chem:TMchemical {id:"' + reactant_id + '", version:"' + VERSION + '"}) CREATE (paper)-[:mentionsReactant {mention: "' + reactant_mention + '"}]->(chem)')
		#Link product to paper
		session.run('MATCH (paper:TMpaper {pmid:"' + paper + '", version:"' + VERSION + '"}), (chem:TMchemical {id:"' + product_id + '", version:"' + VERSION + '"}) CREATE (paper)-[:mentionsProduct {mention: "' + product_mention + '"}]->(chem)')
		#Link reactant and product (both ways)
		session.run('MATCH (reactant:TMchemical {id:"' + reactant_id + '", version:"' + VERSION + '"}), (product:TMchemical {id:"' + product_id + '", version:"' + VERSION + '"}) CREATE (reactant)-[:TMpair]->(product)')
	session.close()	