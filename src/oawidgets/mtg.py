from openalea.mtg import traversal
from pyvis.network import Network

try:
    import colorcet as cc
except ImportError:
    cc = None

from future.builtins import next
from future.builtins import object
import random
import numpy as np
def dict2html(args, properties=None):
    """Return a HTML element from a dictionary"""
    if properties is None:
        selection = ['index', 'parent', 'complex', 'label', 'edge_type', 'scale']
        properties =  []
        for k in args:
            if k not in selection:
                properties.append(k)
    elif isinstance(properties, str):
        properties = [properties]
    properties.sort()
    return '<br>'.join(['%s %s'%(k, args[k]) for k in properties])


def plot(g, properties=None, selection=None, hlayout=True, scale=None,clusters=None, labels=None, **kwds):
    """Plot a MTG in the Jupyter Notebook"""
    G = Network(notebook=True, directed=True,
                layout=hlayout,
                height='800px', width='900px')
    G.toggle_physics(False)
    G.toggle_drag_nodes(False)
    G.toggle_stabilization(False)
    if hlayout:
        G.hrepulsion()
        G.options.layout.hierarchical.direction='DU'
        G.options.layout.hierarchical.parentCentralization=True
        G.options.layout.hierarchical.levelSeparation=150
    else:
    	G.repulsion()

    if scale is None:
	    scale = g.max_scale()

    #Colors
    if cc is not None:
    	colors = cc.glasbey_light
    else:
        colors = ['#6e6efd', '#fb7e81', '#ad85e4', '#7be141', '#ffff00', '#ffa807', '#eb7df4', '#e6ffe3', '#d2e5ff', '#ffd1d9']

    #Data
    vids = g.vertices(scale=scale)
    edges = [(g.parent(vid), vid, 6 if g.edge_type(vid) == '<' else 1)
             for vid in vids if g.parent(vid) is not None]#, 'black' if g.edge_type(vid) == '<' else None
    pos = g.property('position')

    #Level determination
    levels = {}
    root = next(g.component_roots_at_scale_iter(g.root, scale=scale))
    for vid in traversal.pre_order(g, root):
        levels[vid] = 0 if g.parent(vid) is None else levels[g.parent(vid)]+1

    #Component roots
    component_roots = {}
    component_roots[root] = True
    for vid in traversal.pre_order(g, root):
        pid = g.parent(vid)
        if pid is None:
            component_roots[vid] = True
        elif g.complex(pid) != g.complex(vid):
            component_roots[vid] = True

    #Groups
    groups = {}
    for count, vid in enumerate(traversal.pre_order(g, g.complex(root))):
        nc = len(colors)
        groups[vid] = colors[count%nc]
        pid = g.parent(vid)
        if pid:
            if groups[vid] == groups[pid]:
                groups[vid] = colors[(1789*count+17)%nc]

    #Nodes adding
    for vid in vids:
        shape = 'box' if vid in component_roots else 'circle'
        if labels is None:
            label_node = g.label(vid)
        else:
            label_node = labels[vid]
        level = levels[vid]
        if selection is None:
	        color = groups[g.complex(vid)]
        else:
	        color = '#fb7e81' if vid in selection else '#97c2fc'
        title = dict2html(g[vid], properties=properties)
        #gap, mult = max(pos[1])-min(pos[1]), 20
        #x = mult*pos[g.parent(vid)][0] if g.parent(vid) else pos[vid][0]
	    #y = mult*(gap - pos[vid][1]) #if g.parent(vid) else None
	    #physics = False if ('edge_type' not in g[vid] or g[vid]['edge_type']=='<' or g.nb_children(vid)>0) else True
        G.add_node(vid, shape=shape,
                   label=label_node,
                   level=level,
                   color=color,
                   title=title,
                   borderWidth=3,
		           #x=x,
                   #y=y,
                   #physics=physics,
                   )

    #Cluster
    if False:
        for vid in traversal.pre_order(g, g.complex(root)):
            G.add_node(vid, hidden=True)
            if g.parent(vid):
                G.add_edge(g.parent(vid), vid, hidden=True)
            for cid in g.components(vid):
                G.add_edge(vid, cid, hidden=True)

    #Edges adding
    for edge in edges:
        label_edge = g.edge_type(edge[1])
        G.add_edge(edge[0], edge[1], label=label_edge, width=edge[2])

    return G.show('mtg.html')



def plot_clusters_dict(g, properties=None, selection=None, hlayout=True,buttons=False, scale=None,nb_cluster=None, labels=None,file_name = None, **kwds):
    """Plot an at highest scale with nodes colored based on the cluster they belong to"""
     
    G = Network(notebook=True, directed=True,
                layout=hlayout,
                height='800px', width='900px')


    G.toggle_physics(False)
    G.toggle_drag_nodes(False)
    G.toggle_stabilization(False)
    if buttons:
        G.show_buttons(True)
    if hlayout:
        G.hrepulsion()
        G.options.layout.hierarchical.direction='DU'
        G.options.layout.hierarchical.parentCentralization=True
        G.options.layout.hierarchical.levelSeparation=200
    else:
        G.repulsion()
    

    if scale is None:
	    scale = g.max_scale()

    #Colors
    if nb_cluster is not None:
        number_of_colors = nb_cluster
        colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
    
    else:
        colors = ['#6e6efd', '#fb7e81', '#ad85e4', '#7be141', '#ffff00', '#ffa807', '#eb7df4', '#e6ffe3', '#d2e5ff', '#ffd1d9']

    
    
    #Data
    vids = g.vertices(scale=scale)
    edges = [(g.parent(vid), vid, 6 if g.edge_type(vid) == '<' else 1)
             for vid in vids if g.parent(vid) is not None]#, 'black' if g.edge_type(vid) == '<' else None
    pos = g.property('position')
    
    #Level determination
    levels = {}
    root = next(g.component_roots_at_scale_iter(g.root, scale=scale))
    for vid in traversal.pre_order(g, root):
        levels[vid] = 0 if g.parent(vid) is None else levels[g.parent(vid)]+1

    #Component roots
    component_roots = {}
    component_roots[root] = True
    for vid in traversal.pre_order(g, root):
        pid = g.parent(vid)
        if pid is None:
            component_roots[vid] = True
        elif g.complex(pid) != g.complex(vid):
            component_roots[vid] = True
   
    #Groups
    groups = g.property('color')
    cluster = g.property('cluster')
    for i in range(nb_cluster):
        for j in [k for k,v in cluster.items() if v == i]:
            groups[j] = colors[i]
  
    
    weight = g.property('weight')
    for v in traversal.post_order(g,root):
        weight[v] = 1 + sum([weight[v_id] for v_id in g.children(v)])

    #Nodes adding
    for vid in vids:
        shape = 'box' if vid in component_roots else 'circle'
        if labels is None:
            label_node = g.label(vid)
        else:
            label_node = labels[vid]
        level = levels[vid]
        if selection is None:
	        color = groups[vid]
        else:
	        color = '#fb7e81' if vid in selection else '#97c2fc'
        title = dict2html(g[vid], properties=properties)
       
        G.add_node(vid, shape=shape,
                   label=label_node,
                   level=level,
                   color=color,
                   title=title,
                   borderWidth=3,
		           )

    #Cluster
    if False:
        for vid in traversal.pre_order(g, g.complex(root)):
            G.add_node(vid, hidden=True)
            if g.parent(vid):
                G.add_edge(g.parent(vid), vid, hidden=True)
            for cid in g.components(vid):
                G.add_edge(vid, cid, hidden=True)

    #Edges adding
    for edge in edges:
        label_edge = g.edge_type(edge[1])
        G.add_edge(edge[0], edge[1], label=label_edge, width=edge[2])
    if file_name == None:
        return G.show('mtg.html')
    else:
        return G.show('../data/plots/' + file_name + '.html')

def plot_clusters_dependecy(g, properties=None, selection=None, hlayout=True,buttons=False, scale=None,nb_cluster=None,file_name = None, labels=None, **kwds):
    """Plot the dependecies between clusters created with clustering algorithm"""
     
    G = Network(notebook=True, directed=True,
                layout=False,
                height='800px', width='900px')


    G.toggle_physics(False)
    G.toggle_drag_nodes(True)
    G.toggle_stabilization(False)
    if buttons:
        G.show_buttons(False)
   
    G.repulsion()
    

  

    #Colors
    if nb_cluster is not None:
        number_of_colors = nb_cluster
        colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
    
    else:
        colors = ['#6e6efd', '#fb7e81', '#ad85e4', '#7be141', '#ffff00', '#ffa807', '#eb7df4', '#e6ffe3', '#d2e5ff', '#ffd1d9']

    
    #Data
    sub_tree = g.property('sub_tree')
    c_luster = g.property('cluster')
    g.insert_scale(g.max_scale(), lambda vid: g.property('sub_tree').get(vid,None) != None)
    vids = [i for i in range(nb_cluster)]
    edges = [(c_luster[g.parent(g.component_roots(vid)[0])],c_luster[g.component_roots(vid)[0]],6) for vid in g.vertices(scale=g.max_scale()-1) if g.parent(vid) is not None]
    pos = g.property('position')
 
    #Nodes adding
    for vid in vids:
        shape = 'circle' 
       
        if selection is None:
	        color = colors[vid]
        else:
	        color = '#fb7e81' if vid in selection else '#97c2fc'
        title = dict2html(g[vid], properties=properties)
       
        G.add_node(vid, shape=shape,
                   color=color,
                   title=title,
                   borderWidth=3,
                   )

    #Edges adding
    for edge in edges:

        G.add_edge(edge[0], edge[1], label=" ", width=edge[2])
    

    g.remove_scale(g.max_scale()-1)
    if file_name == None:
        return G.show('mtg.html')
    else:
        return G.show('../data/plots/' + file_name + '.html')