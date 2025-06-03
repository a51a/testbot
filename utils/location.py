from config.settings import COORDINATE_PRECISION

def round_coordinates(latitude: float, longitude: float) -> tuple[float, float]:
    """
    Round coordinates to specified precision to reduce unnecessary precision.
    
    Args:
        latitude (float): The latitude coordinate
        longitude (float): The longitude coordinate
        
    Returns:
        tuple[float, float]: Rounded latitude and longitude
    """
    return (
        round(latitude, COORDINATE_PRECISION),
        round(longitude, COORDINATE_PRECISION)
    ) 