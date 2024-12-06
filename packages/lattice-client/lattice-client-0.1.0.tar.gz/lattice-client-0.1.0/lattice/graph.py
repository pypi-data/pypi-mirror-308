from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional, Union
from uuid import uuid4

import networkx as nx

from .execution import Execution
from .factory import Factory
from .types import Runners
from .utils import generate_id

if TYPE_CHECKING:
    from .storage import File


class Graph:
    nodes: list[Node]
    edges: list[Edge]

    def __init__(self, *, nodes: list[Node], edges: list[Edge]):
        self.nodes = nodes
        self.edges = edges

    @classmethod
    def empty(cls):
        return cls(nodes=[], edges=[])

    @classmethod
    def start(
        cls,
        node: Node,
        initializer=None,
        use: Runners = Runners.Lambda,
        override_type=None,
    ):
        graph = cls.empty()
        start_node = Node(type=override_type, graph=graph)
        graph.nodes = [start_node, node]
        graph.edges = [Single.connect(start_node, node, method=initializer, use=use)]
        return graph

    def end(self):
        end_node = Node.end()
        self.edges.append(Edge.connect(self.nodes[-1], end_node, override_type="END"))
        self.nodes.append(end_node)

    def copy(self):
        return self.__class__(nodes=self.nodes, edges=self.edges)

    def join_edge(self, edge: Edge, node: Node):
        edge.target = node
        self.nodes.append(node)
        self.edges.append(edge)


class Node:
    id: str
    type: str
    graph: Graph
    requirements: list[str]

    def __init__(
        self,
        initializer: Optional[Any] = None,
        type: Optional[str] = None,  # noqa
        graph: Graph = None,
    ):
        self.id = str(uuid4())
        self.type = type
        self.graph = graph or Graph.start(
            self,
            initializer=initializer,
            override_type=self.type,
        )
        self.requirements = []

    @classmethod
    def end(cls):
        return cls()

    def _extend(self, entity: Union[Scalar, Vector], edge: Edge):
        graph_copy = self.graph.copy()
        graph_copy.join_edge(edge, entity)
        entity.graph = graph_copy
        return entity

    def _map_to_scalar(self, edge: Edge) -> Scalar:
        scalar = Scalar()
        return self._extend(scalar, edge)

    def _map_to_vector(self, edge: Edge) -> Vector:
        vector = Vector()
        return self._extend(vector, edge)

    def apply(self, method: Callable, use: Runners = Runners.Lambda) -> Scalar:
        return self._map_to_scalar(Single(self, method=method, use=use))

    def map(self, predicate: Callable, use: Runners = Runners.Lambda) -> Vector:
        return self._map_to_vector(Map(self, method=predicate, use=use))

    def starmap(self, predicate: Callable, use: Runners = Runners.Lambda) -> Vector:
        return self._map_to_vector(StarMap(self, method=predicate, use=use))

    def filter(self, predicate: Callable, use: Runners = Runners.Lambda) -> Vector:
        return self._map_to_vector(Filter(self, method=predicate, use=use))

    def run(
        self,
        method: Callable,
        use: Runners = Runners.Lambda,
    ) -> Scalar:
        return self.apply(method, use=use)

    def run_for(
        self,
        method: Callable,
        use: Runners = Runners.Lambda,
        time: Union[str, int] = None,
        cost: int = None,
    ) -> Scalar:
        raise NotImplementedError()

    def run_while(
        self,
        method: Callable,
        use: Runners = Runners.Lambda,
        condition: Callable[[Any], bool] = None,
    ) -> Scalar:
        raise NotImplementedError()

    def run_until(
        self,
        method: Callable,
        use: Runners = Runners.Lambda,
        condition: Callable[[Any], bool] = None,
    ) -> Scalar:
        raise NotImplementedError()

    def first(
        self,
        method: Callable,
        use: Runners = Runners.Lambda,
        condition: Callable[[Any], bool] = None,
        count: int = 1,
    ) -> Scalar:
        raise NotImplementedError()

    def custom(self, setup_method):
        ...

    def get_graph(self):
        graph = nx.DiGraph()
        for node in self.graph.nodes:
            graph.add_node(node.id, **node.serialize())
        for edge in self.graph.edges:
            graph.add_edge(edge.source.id, edge.target.id, **edge.serialize())
        return graph

    def get_line_graph(self) -> nx.Graph:
        graph = self.get_graph()
        line_graph = nx.line_graph(graph)
        line_graph.add_nodes_from((node, graph.edges[node]) for node in line_graph)
        line_graph.add_edges_from(
            (*edge, graph.nodes[edge[0][0]]) for edge in line_graph.edges
        )
        return line_graph

    def serialize_line_graph(self):
        line_graph = self.get_line_graph()
        line_graph_nodes = line_graph.nodes(data=True)
        line_graph_edges = line_graph.edges(data=True)

        node_id_map = {
            "".join(node_id_tuple): node_data["id"]
            for node_id_tuple, node_data in line_graph_nodes
        }

        nodes = [
            {
                "id": node_data["id"],
                "type": node_data["type"],
                "use": node_data["use"] if node_data["use"] is not None else "",
                "method": node_data["method"]
                if node_data["method"] is not None
                else "",
            }
            for _, node_data in line_graph_nodes
        ]

        edges = [
            {
                "id": generate_id(),
                "type": edge_data.get("type", "Scalar"),
                "source": node_id_map["".join(source_pair)],
                "target": node_id_map["".join(target_pair)],
            }
            for source_pair, target_pair, edge_data in line_graph_edges
        ]

        return {"nodes": nodes, "edges": edges}

    def serialize(self):
        return {"id": self.id, "type": self.type}

    def evaluate(
        self,
        *,
        name: Optional[str] = None,
        api_key: str,
        requirements: list[str] = None,
        files: Optional[list[File]] = None,
        overwrite: bool = False,
    ):
        import cloudpickle
        import lattice

        cloudpickle.register_pickle_by_value(lattice)

        self.graph.end()
        self.requirements = requirements or []

        execution = Execution.create(
            self.serialize_line_graph(),
            name=name,
            overwrite=overwrite,
            api_key=api_key,
        )

        if execution.is_new:
            if files is not None:
                for file in files:
                    file.upload(execution_id=execution.id, api_key=api_key)

            execution = execution.submit()

        try:
            if execution.immediate:
                print("Execution completed. Returning results...")
                return execution.get_result()
            if execution.rejoined:
                print("Rejoined execution. Waiting for results...")
            else:
                print("Submitted execution. Waiting for results...")
            return execution.poll_for_completion()
        except KeyboardInterrupt:
            print(
                "Disconnected from execution. Your execution "
                "will continue to run in the background."
            )


class Edge:
    id: str
    source: Node
    target: Node
    type: str = "noop"

    def __init__(
        self,
        source: Node,
        target: Node = None,
        method: Callable = None,
        use: Runners = None,
        override_type: str = None,
    ):
        self.id = generate_id()
        self.source = source
        self.target = target
        self.method = Factory(method)
        self.use = use

        if override_type is not None:
            self.type = override_type

    @classmethod
    def connect(
        cls,
        source: Node,
        target: Node,
        method: Callable = None,
        use: Runners = None,
        override_type: str = None,
    ):
        return cls(
            source,
            target=target,
            method=method,
            use=use,
            override_type=override_type,
        )

    def serialize(self):
        return {
            "id": self.id,
            "source": self.source.id,
            "target": self.target.id,
            "type": self.type,
            "use": self.use.value if self.use is not None else None,
            "method": self.method.serialize() if self.method is not None else None,
        }


class Single(Edge):
    type = "SINGLE"


class Map(Edge):
    type = "MAP"


class StarMap(Edge):
    type = "STARMAP"


class Filter(Edge):
    type = "FILTER"


class Scalar(Node):
    """
    Represents a single, non-proxy, data object.
    """

    def __init__(
        self,
        initializer: Optional[Any] = None,
        graph: Graph = None,
    ):
        super().__init__(
            type="SCALAR",
            graph=graph,
            initializer=initializer,
        )


class Vector(Node):
    """
    Represents a proxy data object with many children.
    """

    def __init__(
        self,
        initializer: Optional[Any] = None,
        graph: Graph = None,
    ):
        super().__init__(
            type="VECTOR",
            graph=graph,
            initializer=initializer,
        )
