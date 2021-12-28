import unittest

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class test(unittest.TestCase):

    # def test_edgedata(self):
    #     edge_a = EdgeData(0,1,5)
    #     edge_b = EdgeData(0,1, 5)
    #     edge_c = EdgeData(0, 2, 7)
    #     self.assertTrue(edge_a.is_equal(edge_b))
    #     self.assertFalse(edge_a.is_equal(edge_c))
    #
    #     self.assertEqual(edge_a.get_src(),0)
    #     self.assertEqual(edge_a.get_dest(),1)
    #     self.assertEqual(edge_a.get_weight(),5)

    # def test_nodedata(self):
    #     node_a = NodeData(0,(1,1,0))
    #
    #     self.assertEqual(node_a.get_location(),(1,1,0))

    def test_DiGraph(self):
        graph = DiGraph()
        self.assertTrue(graph.add_node(0, (1, 1, 0)))
        self.assertTrue(graph.add_node(1, (1, 1, 0)))
        self.assertTrue(graph.add_node(2, (1, 1, 0)))
        self.assertTrue(graph.add_node(3, (1, 1, 0)))
        self.assertTrue(graph.add_node(4, (1, 1, 0)))
        graph.printnode_map()
        self.assertTrue(graph.add_edge(0, 1, 9))
        self.assertTrue(graph.add_edge(1, 2, 9))
        self.assertTrue(graph.add_edge(0, 2, 9))
        self.assertTrue(graph.add_edge(3, 4, 9))
        self.assertTrue(graph.add_edge(1, 0, 9))
        graph.print_edges()
        print("node removed ")
        self.assertTrue(graph.remove_node(0))
        graph.print_edges()
        print("edge removed ")
        self.assertTrue(graph.remove_edge(1, 2))
        graph.print_edges()
        print("edge removed ")
        self.assertTrue(graph.remove_edge(3, 4))
        graph.print_edges()

    def test_load(self):
        algo = GraphAlgo()
        self.assertTrue(algo.load_from_json("../data/A0.json"))
        algo.graph.printnode_map()
        algo.graph.print_edges()



    def test_save(self):
        algo = GraphAlgo()
        self.assertTrue(algo.graph.add_node(0, (1, 1, 0)))
        self.assertTrue(algo.graph.add_node(1, (1, 1, 0)))
        self.assertTrue(algo.graph.add_node(2, (1, 1, 0)))
        self.assertTrue(algo.graph.add_node(3, (1, 1, 0)))
        self.assertTrue(algo.graph.add_node(4, (1, 1, 0)))
        self.assertTrue(algo.graph.add_edge(0, 1, 9))
        self.assertTrue(algo.graph.add_edge(1, 2, 9))
        self.assertTrue(algo.graph.add_edge(0, 2, 9))
        self.assertTrue(algo.graph.add_edge(3, 4, 9))
        self.assertTrue(algo.graph.add_edge(1, 0, 9))
        self.assertTrue(algo.save_to_json("test.json"))

    def test_savenload(self):
        algo = GraphAlgo()
        self.assertTrue(algo.load_from_json("data/A0.json"))
        self.assertTrue(algo.save_to_json("New0.json"))

    def test_shortest(self):
        algo = GraphAlgo()
        algo.graph.add_node(0, (1, 1, 1))
        algo.graph.add_node(1, (1, 1, 1))
        algo.graph.add_node(2, (1, 1, 1))
        algo.graph.add_node(3, (1, 1, 1))
        algo.graph.add_node(4, (1, 1, 1))
        algo.graph.add_node(5, (1, 1, 1))

        algo.graph.add_edge(0, 1, 4)
        algo.graph.add_edge(0, 2, 2)
        algo.graph.add_edge(1, 2, 5)
        algo.graph.add_edge(1, 3, 10)
        algo.graph.add_edge(2, 4, 3)
        algo.graph.add_edge(4, 3, 4)
        algo.graph.add_edge(3, 5, 11)
        print(algo.shortest_path(3, 1)[0])

    def test_tsp(self):
        algo = GraphAlgo()
        algo.graph.add_node(0, (1, 1, 1))
        algo.graph.add_node(1, (1, 1, 1))
        algo.graph.add_node(2, (1, 1, 1))
        algo.graph.add_node(3, (1, 1, 1))
        algo.graph.add_node(4, (1, 1, 1))
        algo.graph.add_node(5, (1, 1, 1))

        algo.graph.add_edge(0, 1, 4)
        algo.graph.add_edge(0, 2, 2)
        algo.graph.add_edge(1, 2, 5)
        algo.graph.add_edge(1, 3, 10)
        algo.graph.add_edge(2, 4, 3)
        algo.graph.add_edge(4, 3, 4)
        algo.graph.add_edge(3, 5, 11)

        self.assertTrue(algo.TSP([0, 5]), ([0, 2, 4, 3, 5], 20))
        algo.graph.remove_edge(3,5)
        self.assertTrue(algo.TSP([0, 5]), ([], -1))

        g = DiGraph()  # creates an empty directed graph

        for n in range(5):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 4, 5)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(1, 3, 1.9)
        g.add_edge(2, 3, 1.1)
        g.add_edge(3, 4, 2.1)
        g.add_edge(4, 2, .5)
        algo = GraphAlgo(g)
        print(algo.TSP([1,2,4]))


    def test_center(self):
        g = DiGraph()  # creates an empty directed graph
        for n in range(5):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 4, 5)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(1, 3, 1.9)
        g.add_edge(2, 3, 1.1)
        g.add_edge(3, 4, 2.1)
        g.add_edge(4, 2, .5)
        algo = GraphAlgo(g)
        print("center is ",algo.centerPoint())

        # algo.load_from_json("../data/A1.json")
        # self.assertTrue(algo.centerPoint(), 3)

if __name__ == '__main__':
    unittest.main()
