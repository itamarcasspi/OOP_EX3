import unittest

from src.DiGraph import DiGraph
from src.EdgeData import EdgeData
from src.GraphAlgo import GraphAlgo
from src.NodeData import NodeData


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
        graph.print_nodes()
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
        self.assertTrue(graph.remove_edge(1,2))
        graph.print_edges()
        print("edge removed ")
        self.assertTrue(graph.remove_edge(3,4))
        graph.print_edges()

    def test_load(self):
        algo = GraphAlgo()
        self.assertTrue(algo.load_from_json("A0.json"))
        algo.graph.print_nodes()
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
        algo.save_to_json("test.json")

    def test_savenload(self):
        algo = GraphAlgo()
        algo.load_from_json("A0.json")
        algo.save_to_json("New0.json")

    def test_shortest(self):
        algo = GraphAlgo()
        algo.graph.add_node(0,(1,1,1))
        algo.graph.add_node(1, (1, 1, 1))
        algo.graph.add_node(2, (1, 1, 1))
        algo.graph.add_node(3, (1, 1, 1))
        algo.graph.add_node(4, (1, 1, 1))
        algo.graph.add_node(5, (1, 1, 1))

        algo.graph.add_edge(0,1,4)
        algo.graph.add_edge(0, 2, 2)
        algo.graph.add_edge(1, 2, 5)
        algo.graph.add_edge(1, 3, 10)
        algo.graph.add_edge(2, 4, 3)
        algo.graph.add_edge(4, 3, 4)
        algo.graph.add_edge(3, 5, 11)
        print(algo.shortest_path(0,5))

    # def test_stams(self):
        # pos = "1,2,3"
        # pos_tuple = tuple(map(float, pos.split(',')))
        # print("pos is ", pos_tuple)
        # dic  = {}
        # dic[1] = 9
        # print(dic[1])
        # dic.pop(1)







if __name__ == '__main__':
    unittest.main()