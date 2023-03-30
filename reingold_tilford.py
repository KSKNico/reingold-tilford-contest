import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# node of a binary tree
class Node:
    left = None
    right = None
    data = None
    left_contour = [0]
    right_contour = [0]
    height : int = 0
    depth : int = 0
    relative_x : int= 0
    x : int = 0

    def insert(self, left, right):
        self.left = left
        self.right = right
        return self

    def __init__(self, data):
        self.data = data

# prints tree in preorder
def print_tree(root_node : Node):
    if root_node == None:
        return
    print(root_node.data)
    print_tree(root_node.left)
    print_tree(root_node.right)

def calculate_all_depths(node):
    depth_counter = 0
    current_layer = [node]
    next_layer = []
    while current_layer != []:
        for n in current_layer:
            if n.left != None:
                next_layer.append(n.left)
            if n.right != None:
                next_layer.append(n.right)
            n.depth = depth_counter
        current_layer = next_layer
        next_layer = []
        depth_counter += 1

def reingold_tilford_postorder(node):
    # search the tree in postorder
    if node == None:
        return
    reingold_tilford_postorder(node.left)
    reingold_tilford_postorder(node.right)
    if node.left == None and node.right == None:
        pass

    elif node.left != None and node.right == None:
        node.left.relative_x = -1
        node.left_contour = [0] + [x + node.left.relative_x for x in node.left.left_contour]
        node.right_contour = [0] + [x + node.left.relative_x for x in node.left.right_contour]

    elif node.right != None and node.left == None:
        node.right.relative_x = +1
        node.left_contour = [0] + [x+node.right.relative_x for x in node.right.left_contour]
        node.right_contour = [0] + [x+node.right.relative_x for x in node.right.right_contour]
    else:
        minimum_height = min(len(node.right.left_contour), len(node.left.right_contour))
        distances = []
        minimal_distance = 0
        for i in range(minimum_height):
            distances.append(node.right.left_contour[i] - node.left.right_contour[i])
        
        if abs(min(distances)) % 2 == 0:
            minimal_distance = abs(min(distances)) + 2
        else:
            minimal_distance = abs(min(distances)) + 1
        
        node.left.relative_x = -minimal_distance//2
        node.right.relative_x = +minimal_distance//2

        # calculate new contours
        if len(node.right.left_contour) > len(node.left.left_contour): 
            node.left_contour =  [0] + [x+node.left.relative_x for x in node.left.left_contour] + [x+node.right.relative_x for x in node.right.left_contour[len(node.left.left_contour):]] 
        else:
            node.left_contour = [0] + [x+node.left.relative_x for x in node.left.left_contour]

        if len(node.left.right_contour) > len(node.right.right_contour): 
            node.right_contour =  [0] + [x+node.right.relative_x for x in node.right.right_contour] + [x+node.left.relative_x for x in node.left.right_contour[len(node.right.right_contour):]]  
        else:
            node.right_contour = [0] + [x+node.right.relative_x for x in node.right.right_contour]

def reingold_tilford_preorder(node):
    if node == None:
        return
    if node.left != None:
        node.left.x = node.left.relative_x + node.x
    if node.right != None:
        node.right.x = node.right.relative_x + node.x
    reingold_tilford_preorder(node.left)
    reingold_tilford_preorder(node.right)

def reingold_tilford(node):
    reingold_tilford_postorder(node)
    reingold_tilford_preorder(node)


def draw_tree(node):
    calculate_all_depths(node)
    fig, ax = plt.subplots()
    draw_tree_recursive(node, ax)
    plt.grid()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(5)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(8)
    # plt.show()

def draw_tree_recursive(node, ax):
    if node == None:
        return
    if node.left != None:
        ax.plot([node.x, node.left.x], [-node.depth, -node.left.depth], color="black", linewidth=0.05)
    if node.right != None:
        ax.plot([node.x, node.right.x], [-node.depth, -node.right.depth], color="white", linewidth=0.05)
    draw_tree_recursive(node.left, ax)
    draw_tree_recursive(node.right, ax)

def read_binary_tree_from_tgf(file_name):
    all_nodes = {}
    with open(file_name) as f:
        for line in f:
            if line.strip() == "#":
                break
            index = int(line.strip().split(" ")[0])
            all_nodes[index] = Node(index)
        for line in f:
            id_l = int(line.strip().split(" ")[0])
            id_r = int(line.strip().split(" ")[1])
            if all_nodes[id_l].right == None:
                all_nodes[id_l].right = all_nodes[id_r]
            elif all_nodes[id_l].left == None:
                all_nodes[id_l].left = all_nodes[id_r]

    return all_nodes[1]

def save_tree_for_contest():
    plt.axis('off')
    plt.savefig('out.svg', bbox_inches='tight',transparent=True, pad_inches=0)

if __name__ == "__main__":
    #root = Node("k")
    #root.insert(Node("e").insert(Node("d").insert(None, Node("c").insert(Node("a"), Node("b"))), None), Node("j").insert(Node("h").insert(Node("f"), Node("g")), Node("i")))
    tree = read_binary_tree_from_tgf("binary_tree.tgf")
    reingold_tilford(tree)
    draw_tree(tree)
    save_tree_for_contest()