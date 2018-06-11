#Neo4j Docker set up

#Stop and destroy
echo '1. Removing previous instance'
docker stop biochem4j
docker rm biochem4j

#Restore Biochem4j from zip
echo '2. Unzipping Biochem4j dump'
tar -xzf SYNBIOCHEM-DB.tar.gz

#Set up new Neo4j instance
echo '3. Pointing Neo4j Docker at Biochem4j download data'
docker create --publish=7474:7474 --publish=7687:7687 --volume=$HOME/Biochem4j_NaCTeM/SYNBIOCHEM-DB/neo4j/data:/data --name biochem4j neo4j:3.0.7
echo 'This is now exactly the same as Biochem4j.org'

#Start biochem4j
docker start biochem4j
echo '4. Neo4j started'