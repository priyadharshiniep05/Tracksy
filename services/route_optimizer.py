from services.multimodal_router import MultimodalRouter

def optimize_route(orig_lat, orig_lng, dest_lat, dest_lng, priority, weight_kg, vehicle_type):
    router = MultimodalRouter()
    options = router.find_optimal_route((orig_lat, orig_lng), (dest_lat, dest_lng), weight_kg, 1000, priority)
    
    selected = options[0]  # default to fastest for demo output consistency
    
    # Transform to the JSON schema expected by legacy routes
    # build a waypoint list for frontend map rendering
    pts = 10
    waypoints = []
    for i in range(pts+1):
        lat = orig_lat + (dest_lat - orig_lat) * (i/pts)
        lng = orig_lng + (dest_lng - orig_lng) * (i/pts)
        waypoints.append([lat, lng])
        
    return {
        'eta': '48 hours',  # generic mock
        'cost': selected['total_cost_usd'],
        'carbon_kg': selected['total_carbon_kg'],
        'distance_km': 1000,
        'ai_explanation': selected['ai_explanation'],
        'waypoints': waypoints,
        'options': options
    }
