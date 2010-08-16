from amuse.support.data import core
from amuse.support.units import generic_unit_system

import numpy



def fill_grid_with_cloud_and_medium(
        grid, 
        center = None,
        radius = None,
        rho_medium = 1.0 | generic_unit_system.mass / generic_unit_system.length**3,
        rho_cloud = 0.1 | generic_unit_system.mass / generic_unit_system.length**3,
        gamma = 5.0 / 3.0,
    ):
    pass



def fill_grid_with_spherical_cloud(
        grid, 
        center = None,
        radius = None,
        rho = 1.0 | generic_unit_system.mass / generic_unit_system.length**3,
        rhovx = 0.0 | generic_unit_system.mass / (generic_unit_system.time * generic_unit_system.length**2),
        rhovy = 0.0 | generic_unit_system.mass / (generic_unit_system.time * generic_unit_system.length**2),
        rhovz = 0.0 | generic_unit_system.mass / (generic_unit_system.time * generic_unit_system.length**2),
        energy = 1.0 | generic_unit_system.mass / (generic_unit_system.time**2 * generic_unit_system.length),
        subgridsize = 4,
    ):
    radii = (grid.position - center).lengths()
    
    if subgridsize <= 1:
        selection = radii <= radius
    else:
        dr = grid.cellsize().length()
        selection = radii < (radius - dr)
        
    grid.rho[selection] = rho
    grid.rhovx[selection] = rhovx
    grid.rhovy[selection] = rhovy
    grid.rhovz[selection] = rhovz
    grid.energy[selection] = energy
    
    if subgridsize <= 1:
        return
    
    selection = numpy.logical_and( radii >= (radius-dr) , radii <= (radius+dr))
    subgrid = core.Grid.create((subgridsize, subgridsize, subgridsize), grid.cellsize())
    subgrid.x -= grid.cellsize()[0] / 2.0
    subgrid.y -= grid.cellsize()[1] / 2.0
    subgrid.z -= grid.cellsize()[2] / 2.0
    x_indices, y_indices, z_indices = grid.indices()
    x_indices = x_indices[selection]
    y_indices = y_indices[selection]
    z_indices = z_indices[selection]
    print len(x_indices)
    
    position = subgrid.position
    centers = center - grid.position[selection]
    
    subgrid_rho = rho * numpy.ones_like(subgrid.x)
    subgrid_rhovx = rhovx * numpy.ones_like(subgrid.x)
    subgrid_rhovy = rhovy * numpy.ones_like(subgrid.x)
    subgrid_rhovz = rhovz * numpy.ones_like(subgrid.x) 
    subgrid_energy = energy * numpy.ones_like(subgrid.x)
    
    update_grid_rho = grid.rho[selection]
    update_grid_rhovx = grid.rhovx[selection]
    update_grid_rhovy = grid.rhovy[selection]
    update_grid_rhovz = grid.rhovz[selection]
    update_grid_energy = grid.energy[selection]
    
    for i in range(len(x_indices)):
        x_index = x_indices[i]
        y_index = y_indices[i]
        z_index = z_indices[i]
            
        center_of_cloud_for_subgrid = centers[i]
        radii = (position - center_of_cloud_for_subgrid).lengths()
         
        
        subgrid_rho[...] = update_grid_rho[i]
        subgrid_rhovx[...] = update_grid_rhovx[i]
        subgrid_rhovy[...] = update_grid_rhovy[i]
        subgrid_rhovz[...] = update_grid_rhovz[i]
        subgrid_energy[...] = update_grid_energy[i]
        
        subgrid_selection = radii <= radius
        
        subgrid_rho[subgrid_selection] = rho
        subgrid_rhovx[subgrid_selection] = rhovx
        subgrid_rhovy[subgrid_selection] = rhovy
        subgrid_rhovz[subgrid_selection] = rhovz
        subgrid_energy[subgrid_selection] = energy
        
        update_grid_rho[i] =  subgrid_rho.mean()
        update_grid_rhovx[i] = subgrid_rhovx.mean()
        update_grid_rhovy[i] = subgrid_rhovy.mean()
        update_grid_rhovz[i] = subgrid_rhovz.mean()
        update_grid_energy[i] = subgrid_energy.mean()

    
    grid.rho[selection] = update_grid_rho
    grid.rhovx[selection] = update_grid_rhovx
    grid.rhovy[selection] = update_grid_rhovy
    grid.rhovz[selection] = update_grid_rhovz
    grid.energy[selection] = update_grid_energy


