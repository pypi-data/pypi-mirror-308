import numpy as np
from Bio import Phylo
import copy
from yxtree.src.tree import mid_unrooted_tree
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'Arial'

rcParams['mathtext.it'] = 'Arial'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.tt'] = 'Arial'
rcParams['mathtext.bf'] = 'Arial'
rcParams['mathtext.cal'] = 'Arial'
rcParams['mathtext.sf'] = 'Arial'
rcParams['mathtext.fontset'] = 'custom'

DEFAULT_STYLE_PARAMS = {
    # clade lines
    'bg_color': 'gray',
    'bg_lw': 0.5,
    'clade_colors': {},
    'clade_labels': {},
    'clade_lw': {},
    # tip labels
    'tip_label': False,
    'tip_fontsize': 6,
    'tip_color': {},
    'tip_bg_color': 'black',
    'tip_ha': 'right',
    'tip_va': 'center',
    # tree
    'rotate_tree': 0,
    'use_edge_length': True,
}


def count_leaves(clade):
    """Recursively count the number of leaves in a clade."""
    if not clade.clades:
        return 1
    return sum(count_leaves(child) for child in clade.clades)


def plot_clade(clade, style_params, ax, xx, yy):
    bg_color = style_params.get('bg_color', '#FFFFFF')
    bg_lw = style_params.get('bg_lw', 0.5)
    clade_colors = style_params.get('clade_colors', {})

    """Plot each clade and its connections recursively."""
    for child in clade.clades:
        color = clade_colors.get(child.name, bg_color)
        ax.plot([xx[clade], xx[child]], [
                yy[clade], yy[child]], color=color, lw=bg_lw)
        plot_clade(child, style_params, ax, xx, yy)


def calculate_coordinate(clade, angle, axis, xx, yy, node_angles, node_axes, use_edge_length):
    """Recursive function to calculate (x, y) coordinates for each clade."""
    children = clade.clades
    if not children:
        return

    num_leaves = count_leaves(clade)
    start = axis - angle / 2
    for i, child in enumerate(children):
        h = child.branch_length if (
            child.branch_length and use_edge_length) else 1  # branch length
        alpha = angle * count_leaves(child) / num_leaves
        beta = start + alpha / 2
        start += alpha

        xx[child] = h * np.cos(beta) + xx[clade]
        yy[child] = h * np.sin(beta) + yy[clade]

        node_angles[child] = alpha
        node_axes[child] = beta

        # Recursively calculate coordinates for child clade
        calculate_coordinate(child, alpha, beta, xx, yy,
                             node_angles, node_axes, use_edge_length)


def calculate_coordinates(tree, rotate_tree=0, use_edge_length=True):
    xx = {tree.root: 0}
    yy = {tree.root: 0}
    node_angles = {}
    node_axes = {}
    calculate_coordinate(tree.root, 2 * np.pi, rotate_tree,
                         xx, yy, node_angles, node_axes, use_edge_length)
    return xx, yy, node_angles, node_axes


class UnrootedTreePlotter:
    def __init__(self, tree, **kwargs):
        self.tree = copy.deepcopy(tree)

        # Set default style parameters
        self.style_params = DEFAULT_STYLE_PARAMS

        # Update style parameters
        self.style_params.update(kwargs)

    def plot(self, ax=None, save_file=None, **kwargs):
        # Set style parameters
        style_params = copy.deepcopy(self.style_params)
        style_params.update(kwargs)

        if not hasattr(self, 'xx'):
            self.mid_unrooted_tree()
            self.calculate_coordinates(style_params['rotate_tree'],
                                       style_params['use_edge_length'])

        # Plot the tree
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.set_aspect('equal')
            ax.axis('off')

        plot_clade(self.tree.root, style_params, ax, self.xx, self.yy)
        tip_label = style_params.get('tip_label', True)

        # Annotate the leaf nodes
        if tip_label == True:
            for clade in self.xx:
                if not clade.clades:  # Only label leaf nodes
                    tip_color = style_params['tip_color'].get(
                        clade.name, style_params['bg_color'])
                    ax.text(self.xx[clade], self.yy[clade], clade.name, ha=style_params['tip_ha'],
                            va=style_params['tip_va'], fontsize=style_params['tip_fontsize'], color=tip_color)

        if save_file:
            fig.savefig(save_file, format='pdf', facecolor='none',
                        edgecolor='none', bbox_inches='tight')
        else:
            plt.show()

    def mid_unrooted_tree(self):
        self.tree, self.node_dict = mid_unrooted_tree(self.tree)

    def calculate_coordinates(self, rotate_tree=0, use_edge_length=True):
        self.xx, self.yy, self.node_angles, self.node_axes = calculate_coordinates(
            self.tree, rotate_tree, use_edge_length)


if __name__ == '__main__':
    tree = Phylo.read('yxtree/data/tree.nwk', 'newick')
    plotter = UnrootedTreePlotter(tree)
    plotter.plot()
