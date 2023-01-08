from models.singleton import Singleton
from SPARQLWrapper import SPARQLWrapper, JSON

class GraphDatabase(metaclass=Singleton):
    def __init__(self):
        self.sparql = SPARQLWrapper("http://localhost:3030/release/sparql")
    
    async def get_socialmedias_from(self, user_id:int):
        stringQuery = """
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/11/meta-social-media.owl#>

            SELECT ?socialName
                WHERE {
                ?subject rdf:type :User;
                        :email ?name ;
                        :id ?id ;
                        :IsOwnerOf ?social .
                ?social :name ?socialName
                FILTER (?id = '""" +user_id+ """')
                }
            }
        """
        
        results = self._runQuery(stringQuery)
        return self._getSocialMedias(results["results"]["bindings"])
    
    async def get_connections_from(self, user_id:int, type:str|None):

        if type == None:
            type = "Relationship"

        stringQuery = """
            PREFIX my: <http://www.mobile.com/model/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/11/meta-social-media.owl#>

            SELECT DISTINCT ?email ?id ?idConnection ?connectionEmail ?type
                WHERE {
                ?subject rdf:type :User;
                        :email ?email ;
                        :id ?id ;
                        :HasRelationship ?relations .
                ?relations :With ?connection .
                ?relations rdf:type ?type .
                ?connection :id ?idConnection ;
                            :email ?connectionEmail
                FILTER (?id = """+user_id+""" && ?type = :"""+type+""")
                }
        """
        
        results = self._runQuery(stringQuery)
        response = self._getConnections(results["results"]["bindings"])
        return response

    async def get_recommends_from(self, user, connection, socialMedia):
        connectionString = "?type rdfs:subPropertyOf* :RELATIONSHIP ."
        filterString = "?name = '"+user+"' && !isBlank(?recommends)"

        if(socialMedia != None):
            filterString = filterString + " && ?connectionSocialMedia = '"+socialMedia+"'"
        
        if(connection != None):
            connectionString = "?type rdfs:subPropertyOf* :"+connection+" ."

        stringQuery = """
            PREFIX my: <http://www.mobile.com/model/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/11/meta-social-media.owl#>

            SELECT DISTINCT ?recommendName ?socialMedia ?username
            WHERE {
                ?subject rdf:type :Person;
                :Name ?name ;
                :HAS	?social;
                OPTIONAL {
                    """+connectionString+"""
                    ?social ?type ?conections .
                    ?social	?type ?recommends .
                    ?recommends :Name ?socialMedia ;
                        :Username ?username .
                    ?user :HAS ?recommends ;
                        :Name ?recommendName .
                    FILTER NOT EXISTS {?recommends ?type ?social}
                } 
                FILTER ("""+filterString+""")
            }
        """
        results = self._runQuery(stringQuery)
        response = self._getRecommendations(results["results"]["bindings"])
        return response

    async def get_influence_level_from(self, user_id:int):

        stringQuery = """
            PREFIX my: <http://www.mobile.com/model/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/11/meta-social-media.owl#>


        SELECT (count ( distinct ?relations ) AS ?level)
            WHERE {
                ?relations rdf:type :Influence .
                ?relations :With ?user .
                ?user :id ?id .
                FILTER (?id = """+user_id+""")
            }GROUP BY ?id
        """
        results = self._runQuery(stringQuery)
        response = self._getLevel(results["results"]["bindings"], str(user_id))
        return response

    def _runQuery(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert()
    
    def _getSocialMedias(self, results):
        response = []
        for result in results:
            response.append(result["socialName"]["value"])
        return response

    def _getConnections(self, results):
        response = []
        for result in results:
            response.append({
                "name" : result["userConnectedName"]["value"],
                "social_media" : result["connectionSocialMedia"]["value"],
                "username" : result["userConnectedUsername"]["value"]
            })
        return response

    def _getRecommendations(self, results):
        response = []
        for result in results:
            response.append({
                "name" : result["recommendName"]["value"],
                "social_media" : result["socialMedia"]["value"],
                "username" : result["username"]["value"]
            })
        return response
    
    def _getLevel(self, results, id):
        if(len(results) == 0):
            return {
                "user" : id,
                "influence_score" : 0
            }

        result = results[0]
        response ={
            "user" : id,
            "influence_score" : result["level"]["value"]
        }
        return response