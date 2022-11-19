
def F_drag_descent(edl_system,planet,altitude,velocity):
    
    # Compute the net drag force. 
    
    
    # compute the density of planetary atmosphere at current altitude
    density, _, _ = get_local_atm_properties(planet, altitude)
    
    # This is the (1/2)*density*velocity^2 part of the drag model. The missing
    # bit is area*Cd, which we'll figure out below.
    rhov2=0.5*density*velocity**2
    
    
    # *************************************
    # Determine which part(s) of the EDL system are contributing to drag
    
    # If the heat shield has not been ejected, use that as our drag
    # contributor. Otherwise, use the sky crane.
    if not edl_system['heat_shield']['ejected']:
        ACd_body = np.pi*(edl_system['heat_shield']['diameter']/2.0)**2*edl_system['heat_shield']['Cd']
    else:
        ACd_body = edl_system['sky_crane']['area']*edl_system['sky_crane']['Cd']

    
    # if the parachute is in the deployed state, need to account for its area
    # in the drag calculation
    if edl_system['parachute']['deployed'] and not edl_system['parachute']['ejected']:
        ACd_parachute = np.pi*(edl_system['parachute']['diameter']/2.0)**2*edl_system['parachute']['Cd']
    else:
        ACd_parachute = 0.0
    

    # #Mach Effeciency Factor corrention
    mach = v2M_Mars(velocity,altitude)
    if 0.7<mach and mach <2.6:
        mach_ref = [0.25,0.5,0.65,0.7,0.8,0.9,0.95,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.8,1.9,2.0,2.2,2.5,2.6]
        MEF_ref = [1.0,1,1,.98,.9,.72,.66,.76,.9,.96,.99,.999,.992,.98,.9,.85,.82,.75,.65,.62]
        fun = interp1d(mach_ref, MEF_ref,kind='quadratic',) # Interpolate MEF data
        MEF = fun(mach) # Get MEF value for our parameters
        ACd_body *= MEF # Apply MEF factor
        ACd_parachute *= MEF


    # This computes the ultimate drag force
    F=rhov2*(ACd_body+ACd_parachute)
    
    return F