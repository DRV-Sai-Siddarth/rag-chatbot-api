import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph

load_dotenv()

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

def get_graph_context(query):
    # Custom Cypher query — improve as per your graph schema
    cypher = f"""
    CALL db.index.fulltext.queryNodes('your_index', '{query}')
    YIELD node, score
    RETURN node LIMIT 5
    """
    results = graph.query(cypher)
    return "\n".join(str(r["node"]) for r in results)
