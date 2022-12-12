from models.singleton import Singleton
from SPARQLWrapper import SPARQLWrapper, JSON

class Database(metaclass=Singleton):
    def __init__(self):
        self.sparql = SPARQLWrapper("http://localhost:3030/release/sparql")
    
    async def get_socialmedias_from(self, user):
        stringQuery = """
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/11/meta-social-media.owl#>

            SELECT ?socialName
            WHERE {
                ?subject rdf:type :Person;
                        :Name ?name ;
                        :HAS ?social .
                ?social :Name ?socialName .
            FILTER (?name = '""" +user+ """')
            }
        """
        
        results = self._runQuery(stringQuery)
        return self._getSocialMedias(results["results"]["bindings"])
    
    async def get_connections_from(self, user, connection, socialMedia):
        connectionString = "?type rdfs:subPropertyOf* :RELATIONSHIP ."

        filterString = "?name = '"+user+"'"
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

            SELECT DISTINCT ?userConnectedName ?connectionSocialMedia ?userConnectedUsername
            WHERE {
                ?subject rdf:type :Person;
                    :Name ?name ;
                    :HAS	?social .
                """+connectionString+"""
                ?social :Name ?socialName	;
                    ?type	?conections ;
                    :Username ?username .
                ?userConnected :HAS ?conections ;
                    :Name	?userConnectedName .
                ?conections :Username ?userConnectedUsername ;
                    :Name	?connectionSocialMedia
                            
                FILTER ("""+filterString+""")
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

    async def get_influence_level_from(self, user, socialMedia):
        filterString = "?name = '"+user+"'"

        if(socialMedia != None):
            filterString = filterString + " && ?socialName = '"+socialMedia+"'"

        stringQuery = """
            PREFIX my: <http://www.mobile.com/model/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/11/meta-social-media.owl#>

            SELECT ?name (count ( distinct ?connections ) AS ?level)
            WHERE {
                ?subject rdf:type :Person;
                        :Name ?name ;
                        :HAS	?social .
                ?connections :INFLUENCE ?social .
                ?social :Name ?socialName .
                FILTER ("""+filterString+""")
            }GROUP BY ?name
        """
        results = self._runQuery(stringQuery)
        response = self._getLevel(results["results"]["bindings"], user)
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
    
    def _getLevel(self, results, name):
        if(len(results) == 0):
            return {
                "user" : name,
                "influence_score" : 0
            }

        result = results[0]
        response ={
            "user" : name,
            "influence_score" : result["level"]["value"]
        }
        return response