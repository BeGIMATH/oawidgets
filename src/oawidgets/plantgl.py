from openalea.plantgl.all import *
import k3d

def tomesh(geometry, d=None):
    """Return a mesh from a geometry object"""
    if d is None:
        d = Tesselator()

    geometry.apply(d)
    idl = [tuple(index) for index in list(d.discretization.indexList)]
    pts = [(pt.x, pt.y, pt.z) for pt in list(d.discretization.pointList)]
    mesh = k3d.mesh(vertices=pts, indices=idl)
    return mesh

def PlantGL(pglobject, plot=None):
    """Return a k3d plot from PlantGL shape, geometry and scene objects"""
    if plot is None:
        plot = k3d.plot()

    if isinstance(pglobject, Geometry):
        mesh = tomesh(pglobject)
        plot += mesh
    elif isinstance(pglobject, Shape):
        mesh = tomesh(pglobject.geometry)
        mesh.color = pglobject.appearance.ambient.toUint()
        plot += mesh
    elif isinstance(pglobject, Scene):
        for sh in pglobject:
            PlantGL(sh,plot)
    return plot

def PlantGLscene(scene, plot=None):
    if plot is None:
        plot = k3d.plot()

    for obj in scene:
        if isinstance(obj, Geometry):
            mesh = tomesh(obj)
            plot += mesh
        elif isinstance(obj, Shape):
            mesh = tomesh(obj.geometry)
            mesh.color = obj.appearance.ambient.toUint()
            plot += mesh
        else:
            pass
    return plot
