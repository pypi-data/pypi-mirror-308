#%%
import rnx_3 as rnx
import numpy as np
import r3f
'''
Test the modifications to use RNX 3.0X obs and nav files with the following
files in the ./data directory:
- UrbanNav-HK-Medium-Urban-1.ublox.m8t.GEJ.obs (RNX 3.0X obs file)
- GUAM00GUM_R_20211370100_01H_JN.rnx (RNX 3.0X nav file)
- HKSL00HKG_R_20211370100_01H_GN.rnx (RNX 3.0X nav file)
- HKSL00HKG_R_20211370100_01H_EN.rnx (RNX 3.0X nav file)
'''
# UrbanNav
obs_file = './data/UrbanNav-HK-Medium-Urban-1.ublox.m8t.GEJ.obs'
nav_files = [
   './data/GUAM00GUM_R_20211370100_01H_JN.rnx',
    './data/HKSL00HKG_R_20211370100_01H_GN.rnx',
   './data/HKSL00HKG_R_20211370100_01H_EN.rnx',
]
c = 299792458.0             # speed of light [m/s] (p. 98)

def pos_rx(xh, yh, zh, pt, xs, ys, zs, ps,constellations=None):
    """
    Author: Dr. David Woodburn, AFIT
    Modified by Kyle Leland to accomodate multi-constellation data
    This function calculates the ECEF receiver position and clock error
    correction pseudorange using satellite positions, pseudoranges, and an
    initial guess for the receiver values.

    Parameters
    ----------
    xh : float
        Guess ECEF x-axis coordinate of receiver position [m].
    yh : float
        Guess ECEF y-axis coordinate of receiver position [m].
    zh : float
        Guess ECEF z-axis coordinate of receiver position [m].
    pt : float, list[float]
        Guess clock error correction(s) pseudorange of receiver [m]. If using
        multiple constellations, pt will be an array of clock error corrections.
    xs : (J,) np.ndarray
        Space vehicle ECEF x-axis coordinates [m].
    ys : (J,) np.ndarray
        Space vehicle ECEF y-axis coordinates [m].
    zs : (J,) np.ndarray
        Space vehicle ECEF z-axis coordinates [m].
    ps : (J,) np.ndarray
        Pseudoranges to space vehicles [m].
    constellations: (J,) np.ndarray; optional
        Constellation of each space vehicle encoded by integers. The constellation
        code corresponds to the index of the clock error in pt. E.g., if
        constellation[0] == 2, then the clock error for the first space vehicle
        corresponds to pt[2]. If not provided, the function will assume all space
        vehicles are in the same constellation.

    Returns
    -------
    xh : float
        Calculated ECEF x-axis coordinate of receiver position [m].
    yh : float
        Calculated ECEF y-axis coordinate of receiver position [m].
    zh : float
        Calculated ECEF z-axis coordinate of receiver position [m].
    pt : float; np.ndarray
        Calculated clock error correction pseudorange of receiver [m]. If solving
        for multiple constellations, pt will be an array of clock error corrections.

    Notes
    -----
    A positive receiver pseudorange clock error correction, `pt`, means that a
    more accurate pseudorange is actually smaller than the quantity given::

        ps -= pt

    It means that the receiver's clock is actually ahead::

        t_rx -= pt/c
    """

    # constants
    c = 299792458.0         # speed of light [m/s]
    wie = 7.292115e-5       # sidereal Earth rate [rad/s]

    # number of space vehicles
    J = len(ps)
    M = len(pt) # the number of constellations

    # ones vector
    if constellations is not None:
        O = np.zeros((J,M))
        for m in range(M):
            O[:,m] = 1*(constellations == m) # 1 if the satellite is in the constellation
            # 0 otherwise
    else:
        O = np.ones(J)

    # Initialize the rotated x and y coordinates of the space vehicles.
    xs_rot = xs + 0
    ys_rot = ys + 0

    # newton-raphson method
    for n in range(10):
        # geometric pseudorange
        Dx = xs_rot - xh
        Dy = ys_rot - yh
        Dz = zs - zh
        rh = np.sqrt(Dx**2 + Dy**2 + Dz**2)

        # expected pseudorange
        if constellations is not None:
            ph = rh + np.sum(O*pt,axis=1)
        else:
            ph = rh + pt

        # pseudorange error
        dp = ps - ph

        # Jacobian
        H = np.column_stack(( -Dx/rh, -Dy/rh, -Dz/rh, O ))

        # solution
        x = np.linalg.lstsq(H, dp, rcond=None)[0]
        xh += x[0]
        yh += x[1]
        zh += x[2]
        if constellations is not None:
            pt += x[3:]
        else:
            pt += x[3]

        # error norm check
        err = np.linalg.norm(x)
        if err < 1:
            break

        # earth rotation correction
        t_prop = rh/c
        co = np.cos(wie*t_prop)
        si = np.sin(wie*t_prop)
        xs_rot = co*xs + si*ys
        ys_rot = co*ys - si*xs

    return xh, yh, zh, pt


def pos_sv(eph, th_sv, rm_GD=True):
    """
    Author: Dr. David Woodburn, AFIT
    This function calculates the ECEF position of a space vehicle and the space
    vehicle clock error correction pseudorange.

    Parameters
    ----------
    eph : EphG
        Ephemeris object for one GPS space vehicle with the following
        properties::
            t_oe        t_oc        sqrtA
            M_0         Delta_n     e
            omega       Omega_0     DOmega
            C_us        C_rs        C_is
            C_uc        C_rc        C_ic
            i_0         Di          T_GD
            a_f0        a_f1
    th_sv : float
        Approximate space-vehicle transmit time in GPS week seconds.
    rm_GD : boolean, default True
        Flag to remove group delay, `T_GD`.

    Returns
    -------
    xs : float
        Space vehicle ECEF x-axis coordinates [m].
    ys : float
        Space vehicle ECEF y-axis coordinates [m].
    zs : float
        Space vehicle ECEF z-axis coordinates [m].
    pts : float
        Clock error correction pseudorange of space vehicle [m].

    Notes
    -----
    The ECEF position is at the transmit time relative to the ECEF frame at
    transmit time.  In other words, the rotation of the earth during the
    propagation of the transmitted signal has not been accounted for yet in the
    space vehicle position.

    The return value `pts` is the speed of light times the space vehicle clock
    error correction.  A positive value of `pts` means that the space vehicle
    clock was ahead when calculating the pseudorange, which means the
    pseudorange is smaller than it should be.  To correct the pseudorange with
    this error correction, add this pseudorange clock error correction to the
    raw pseudorange value::

        ps += pts

    You can also subtract the clock error correction, `pts/c`, from the
    estimated space vehicle clock time, `th_sv`, to get a more accurate space
    vehicle clock time::

        t_sv = th_sv - pts/c
    """

    # constants
    c = 299792458.0         # speed of light [m/s]
    mu = 3.986005e14        # Earth gravitational constant [m^3/s^2]
    wie = 7.2921151467e-5   # sidereal Earth rate [rad/s]

    # time since reference time ephemeris [s]
    Dtw = th_sv - eph.t_oe
    if Dtw > 302400:
        Dtw -= 604800
    elif Dtw < -302400:
        Dtw += 604800

    # semi-major axis [m]
    A = eph.sqrtA**2

    # corrected mean motion [rad/s]
    n_0 = np.sqrt(mu/(A**3))

    # mean anomaly [rad]
    M = eph.M_0 + (n_0 + eph.Delta_n)*Dtw

    # eccentric anomaly [rad]
    E = M + eph.e*np.sin(M)/np.sqrt(1 - 2*eph.e*np.cos(M) + eph.e**2)
    E = E + (M - E + eph.e*np.sin(E))/(1 - eph.e*np.cos(E))

    # true anomaly [rad]
    f = np.arctan2(np.sqrt(1 - eph.e**2)*np.sin(E), np.cos(E) - eph.e)

    # uncorrected argument of latitude [rad]
    Phi = f + eph.omega

    # second harmonic corrections
    co = np.cos(2*Phi)
    si = np.sin(2*Phi)
    du = eph.C_us*si + eph.C_uc*co
    dr = eph.C_rs*si + eph.C_rc*co
    di = eph.C_is*si + eph.C_ic*co

    # corrected argument of latitude [rad], radius [m], and inclination [rad]
    u = Phi + du
    r = A*(1 - eph.e*np.cos(E)) + dr
    i = eph.i_0 + eph.Di*Dtw + di

    # position in orbital plane [m]
    xo = r*np.cos(u)
    yo = r*np.sin(u)

    # corrected longitude of ascending node [rad]
    Omega = eph.Omega_0 - wie*(Dtw + eph.t_oe) + eph.DOmega*Dtw

    # position at transmit time relative to the ECEF frame at transmit time [m]
    xs = np.cos(Omega)*xo - np.sin(Omega)*np.cos(i)*yo
    ys = np.sin(Omega)*xo + np.cos(Omega)*np.cos(i)*yo
    zs = np.sin(i)*yo

    # time since reference clock time [s]
    Dtcw = th_sv - eph.t_oc
    if Dtcw > 302400:
        Dtcw -= 604800
    if Dtcw < -302400:
        Dtcw += 604800

    # satellite clock error correction pseudorange [m]
    F = -2*np.sqrt(mu)/(c**2)
    Dtr = eph.e*F*eph.sqrtA*np.sin(E)
    dts = eph.a_f0 + eph.a_f1*Dtcw + Dtr
    pts = dts*c

    # Remove group delay.
    if rm_GD:
        pts -= c*eph.T_GD

    return xs, ys, zs, pts


if __name__ == '__main__':
    # Read the RNX 3.0X obs file
    obs, navs = rnx.read_multiple_navs(obs_file,nav_files)


    obs, navs = rnx.read_multiple_navs(obs_file,nav_files)
    constellation_list = []
    for nav in navs:
        constellation_list.append(nav.system)
    constellation_list = list(set(constellation_list))

    xr = 0.0    # -2418181.49940663 - true
    yr = 0.0    #  5385962.29162558 - true
    zr = 0.0    #  2405305.18223442 - true
    ptr = np.zeros(len(constellation_list))

    K = len(obs.t)
    xr_t = np.zeros(K)
    yr_t = np.zeros(K)
    zr_t = np.zeros(K)
    ptr_t = np.zeros((K,len(constellation_list)))

    # For each point in time
    for k in range(1):
        # Get the data for this point in time
        tr = obs.t[k]
        rhos = obs.C1C[k]
        ephs = obs.ephs[k]

        constellations_k = []

        # Process each space vehical
        xs_j = []
        ys_j = []
        zs_j = []
        ps_j = []
        for j in range(len(obs.svs)):
            # skip missing data
            if np.isnan(rhos[j]) or ephs[j] is None:
                continue
        
            this_eph = ephs[j]
            # Get the space vehicle position and pseudorange according to the user
            ps = rhos[j]
            ths = tr - ps/rnx.c
            xs, ys, zs, pts = pos_sv(ephs[j], ths)
            ps += pts
            
            # Save the results.
            xs_j.append(xs)
            ys_j.append(ys)
            zs_j.append(zs)
            ps_j.append(ps)

            # Save the constellation
            constellations_k.append(
                constellation_list.index(obs.svs[j][0])) # the first character of the SV
            # is the constellation/system code ('G' for GPS, 'E' for Galileo, 'J' for QZ)

        # Skip if there are not enough space vehicles
        if len(xs_j) < 4:
            continue

        # Convert to numpy arrays
        xs_j = np.array(xs_j)
        ys_j = np.array(ys_j)
        zs_j = np.array(zs_j)
        ps_j = np.array(ps_j)
        constellations_k = np.array(constellations_k)

        # Get the receiver position
        xr, yr, zr, ptr = pos_rx(xr, yr, zr, ptr, xs_j, ys_j, zs_j, ps_j,constellations_k) 
        
        # Save the results
        xr_t[k] = xr
        yr_t[k] = yr
        zr_t[k] = zr
        ptr_t[k] = ptr


    # Compare the estimate for the first position to the true position
    print("First step position estimate: ", xr_t[0], yr_t[0], zr_t[0])

    clock_error_str = "  ".join("{}: {:f} ".format(constellation_list[i],ptr_t[0][i]) for i in range(len(constellation_list)))
    print("First step clock error estimate: ")
    print(clock_error_str)

    lla = r3f.ecef_to_geodetic((xr_t[0], yr_t[0], zr_t[0]), degs=True)
    print('First position lat lon alt: ', lla)

    # UrbanNav truth from online dataset
    true_lat = 22+18/60+4.31949/3600 
    true_lon = 114+10/60+44.60559/3600
    true_elev = 3.472
    true_ecef = r3f.geodetic_to_ecef((true_lat, true_lon, true_elev), degs=True)
    estimated_ned = r3f.ecef_to_tangent((xr_t[0], yr_t[0], zr_t[0]), true_ecef)

    # print errors
    print('True ECEF: ', true_ecef)
    print('NED Error: ', estimated_ned)
    print('||NED error||: ', np.linalg.norm(np.array(estimated_ned)))
