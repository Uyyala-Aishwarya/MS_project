from neo4j import GraphDatabase
import ast


class Neo4jHandler:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="Login123$%"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_nodes_and_relationships(self, parsed_data):
        """
        Creates nodes and relationships in Neo4j based on the parsed data.
        """
        with self.driver.session() as session:
            nodes = {}
            for data in parsed_data:
                file_name = data["file"]
                for node in ast.walk(data["tree"]):
                    if isinstance(node, ast.FunctionDef):
                        session.run(
                            "MERGE (f:Function {name: $name, file: $file, type: 'Function'})",
                            name=node.name, file=file_name
                        )
                        nodes[node] = node.name
                        print(f"Created Function node: {node.name} in file {file_name}")
                    elif isinstance(node, ast.ClassDef):
                        session.run(
                            "MERGE (c:Class {name: $name, file: $file, type: 'Class'})",
                            name=node.name, file=file_name
                        )
                        nodes[node] = node.name
                        print(f"Created Class node: {node.name} in file {file_name}")

            # Create relationships between classes and functions
            for data in parsed_data:
                file_name = data["file"]
                for node in ast.walk(data["tree"]):
                    if isinstance(node, ast.FunctionDef):
                        for child in ast.iter_child_nodes(node):
                            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                                called_function_name = child.func.id
                                if called_function_name in nodes.values():
                                    session.run(
                                        "MATCH (f:Function {name: $from_name, file: $from_file}), "
                                        "(t:Function {name: $to_name}) "
                                        "MERGE (f)-[:CALLS]->(t)",
                                        from_name=node.name, from_file=file_name, to_name=called_function_name
                                    )
                                    print(f"Created relationship: {node.name} CALLS {called_function_name}")
                    elif isinstance(node, ast.ClassDef):
                        for child in ast.iter_child_nodes(node):
                            if isinstance(child, ast.FunctionDef):
                                session.run(
                                    "MATCH (c:Class {name: $class_name, file: $class_file}), "
                                    "(f:Function {name: $function_name}) "
                                    "MERGE (c)-[:CONTAINS]->(f)",
                                    class_name=node.name, class_file=file_name, function_name=child.name
                                )
                                print(f"Created relationship: {node.name} CONTAINS {child.name}")

    def query_knowledge_graph(self, query):
        """
        Queries the Neo4j knowledge graph to extract relevant information.
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]