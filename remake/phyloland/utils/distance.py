"""Geographic distance calculations for phylogeographic analysis."""

from math import pi, sin, cos, acos


def geographic_distance_km(lat1, lat2, lon1, lon2):
    """
    Calculate great circle distance between two points in kilometers.
    
    This function exactly replicates the distkm() function from the original
    Phyloland C code to ensure identical distance calculations.
    
    Parameters
    ----------
    lat1, lat2 : float
        Latitude coordinates in decimal degrees
    lon1, lon2 : float  
        Longitude coordinates in decimal degrees
        
    Returns
    -------
    float
        Distance in kilometers
        
    Notes
    -----
    Uses the great circle distance formula with Earth radius = 6378.137 km
    Formula: d = acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon2-lon1)) * R
    """
    # Convert degrees to radians
    lat1r = (lat1/180) * pi
    lat2r = (lat2/180) * pi
    lon1r = (lon1/180) * pi
    lon2r = (lon2/180) * pi
    
    # Calculate cosine of angle between points
    cos_angle = sin(lat1r)*sin(lat2r) + cos(lat1r)*cos(lat2r)*cos(lon2r-lon1r)
    
    # Clamp to [-1, 1] to handle numerical precision issues
    cos_angle = max(-1.0, min(1.0, cos_angle))
    
    # Calculate distance using Earth radius from original C code
    d = acos(cos_angle) * 6378.137
    
    return d


# Alias for compatibility
distkm = geographic_distance_km
