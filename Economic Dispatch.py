def economic_dispatch(demand, indian_link_price, month, hour):
    """
    Perform economic dispatch with monthly hydro capacities, seasonal constraints,
    and hourly solar power variation.
    Season is automatically determined based on month.
    Hour should be 1-24 (1 = 1am, 12 = noon, 24 = midnight).
    """
    # Validate hour input
    if hour < 1 or hour > 24:
        raise ValueError("Hour must be between 1 and 24")
    
    # Determine season based on month
    month = month.lower()
    dry_season_months = ['dec', 'jan', 'feb', 'mar', 'apr']
    if month in dry_season_months:
        season = 'dry'
    else:
        season = 'wet'
    
    monthly_data = {
        'jan': {
            'Victoria': 163.9554, 'Kotmale': 73.65121, 'Upper Kotmale': 67.05712, 'Randenigala': 95.95027,
            'Samanalawewa': 99.0373, 'New Laxapana': 67.03461, 'Kukule': 37.5541, 'Polpitiya': 54.6418,
            'Canyon': 20.78226, 'Rantambe': 46.10954, 'Wimalasurendra': 26.58165, 'Old Laxapana': 36.49227,
            'Bowathenna': 22.67977, 'Ukuwela': 15.6959, 'Broadlands': 11.68817, 'Uma Ora': 0
        },
        # ... (rest of the monthly_data dictionary remains the same)
        'feb': {
            'Victoria': 54.73, 'Kotmale': 33.27, 'Upper Kotmale': 30.25, 'Randenigala': 29.58,
            'Samanalawewa': 29.96, 'New Laxapana': 22.19, 'Kukule': 23.44, 'Polpitiya': 20.34,
            'Canyon': 19.23, 'Rantambe': 14.79, 'Wimalasurendra': 14.05, 'Old Laxapana': 13.68,
            'Bowathenna': 13.32, 'Ukuwela': 12.95, 'Broadlands': 11.83
        },
        'mar': {
            'Victoria': 52.49, 'Kotmale': 31.91, 'Upper Kotmale': 29.01, 'Randenigala': 28.37,
            'Samanalawewa': 28.72, 'New Laxapana': 21.28, 'Kukule': 22.49, 'Polpitiya': 19.50,
            'Canyon': 18.44, 'Rantambe': 14.18, 'Wimalasurendra': 13.48, 'Old Laxapana': 13.12,
            'Bowathenna': 12.77, 'Ukuwela': 12.41, 'Broadlands': 11.34
        },
        'apr': {
            'Victoria': 81.86, 'Kotmale': 49.78, 'Upper Kotmale': 45.25, 'Randenigala': 44.25,
            'Samanalawewa': 44.81, 'New Laxapana': 33.19, 'Kukule': 35.07, 'Polpitiya': 30.42,
            'Canyon': 28.76, 'Rantambe': 22.13, 'Wimalasurendra': 21.01, 'Old Laxapana': 20.47,
            'Bowathenna': 19.92, 'Ukuwela': 19.36, 'Broadlands': 17.69
        },
        'may': {
            'Victoria': 89.64, 'Kotmale': 54.52, 'Upper Kotmale': 49.54, 'Randenigala': 48.45,
            'Samanalawewa': 49.06, 'New Laxapana': 36.34, 'Kukule': 38.40, 'Polpitiya': 33.31,
            'Canyon': 31.49, 'Rantambe': 24.22, 'Wimalasurendra': 23.01, 'Old Laxapana': 22.41,
            'Bowathenna': 21.80, 'Ukuwela': 21.20, 'Broadlands': 19.38
        },
        'jun': {
            'Victoria': 85.71, 'Kotmale': 52.13, 'Upper Kotmale': 47.38, 'Randenigala': 46.33,
            'Samanalawewa': 46.90, 'New Laxapana': 34.75, 'Kukule': 36.71, 'Polpitiya': 31.85,
            'Canyon': 30.11, 'Rantambe': 23.17, 'Wimalasurendra': 22.00, 'Old Laxapana': 21.43,
            'Bowathenna': 20.85, 'Ukuwela': 20.26, 'Broadlands': 18.53
        },
        'jul': {
            'Victoria': 76.87, 'Kotmale': 46.75, 'Upper Kotmale': 42.49, 'Randenigala': 41.55,
            'Samanalawewa': 42.07, 'New Laxapana': 31.16, 'Kukule': 32.93, 'Polpitiya': 28.56,
            'Canyon': 27.00, 'Rantambe': 20.78, 'Wimalasurendra': 19.73, 'Old Laxapana': 19.22,
            'Bowathenna': 18.70, 'Ukuwela': 18.17, 'Broadlands': 16.61
        },
        'aug': {
            'Victoria': 81.65, 'Kotmale': 49.65, 'Upper Kotmale': 45.13, 'Randenigala': 44.14,
            'Samanalawewa': 44.69, 'New Laxapana': 33.10, 'Kukule': 34.97, 'Polpitiya': 30.35,
            'Canyon': 28.70, 'Rantambe': 22.07, 'Wimalasurendra': 20.97, 'Old Laxapana': 20.42,
            'Bowathenna': 19.87, 'Ukuwela': 19.31, 'Broadlands': 17.66
        },
        'sep': {
            'Victoria': 111.21, 'Kotmale': 67.63, 'Upper Kotmale': 61.46, 'Randenigala': 60.11,
            'Samanalawewa': 60.86, 'New Laxapana': 45.08, 'Kukule': 47.64, 'Polpitiya': 41.33,
            'Canyon': 39.07, 'Rantambe': 30.06, 'Wimalasurendra': 28.56, 'Old Laxapana': 27.81,
            'Bowathenna': 27.06, 'Ukuwela': 26.31, 'Broadlands': 24.04
        },
        'oct': {
            'Victoria': 80.39, 'Kotmale': 48.88, 'Upper Kotmale': 44.44, 'Randenigala': 43.46,
            'Samanalawewa': 44.00, 'New Laxapana': 32.59, 'Kukule': 34.44, 'Polpitiya': 29.88,
            'Canyon': 28.25, 'Rantambe': 21.73, 'Wimalasurendra': 20.65, 'Old Laxapana': 20.09,
            'Bowathenna': 19.56, 'Ukuwela': 19.02, 'Broadlands': 17.38
        },
        'nov': {
            'Victoria': 117.18, 'Kotmale': 71.26, 'Upper Kotmale': 64.76, 'Randenigala': 63.35,
            'Samanalawewa': 64.14, 'New Laxapana': 47.50, 'Kukule': 50.19, 'Polpitiya': 43.54,
            'Canyon': 41.17, 'Rantambe': 31.67, 'Wimalasurendra': 30.08, 'Old Laxapana': 29.29,
            'Bowathenna': 28.50, 'Ukuwela': 27.71, 'Broadlands': 25.33
        },
        'dec': {
            'Victoria': 187.5813, 'Kotmale': 101.0225, 'Upper Kotmale': 71.61324, 'Randenigala': 110.4694,
            'Samanalawewa': 41.79301, 'New Laxapana': 65.6912, 'Kukule': 34.41667, 'Polpitiya': 61.7621,
            'Canyon': 19.22917, 'Rantambe': 46.77184, 'Wimalasurendra': 27.97312, 'Old Laxapana': 47.39819,
            'Bowathenna': 21.23286, 'Ukuwela': 18.99126, 'Broadlands': 14.36492, 'Uma Ora': 53.02218
        }
    }
    
    if month not in monthly_data:
        raise ValueError("Invalid month. Use 3-letter month abbreviations (jan, feb, etc.)")
    
    # Rest of your function would continue here...

    # Calculate solar power based on hour of day
    def get_solar_power(hour, max_capacity=1470):
        """Returns solar power output based on hour of day (0 at night, max around noon)"""
        # Solar hours approximately 6am to 6pm (6 to 18)
        if hour < 6 or hour >= 18:
            return 0  # No solar at night
        
        # Create a bell curve for solar output
        # Peak at noon (hour = 12), zero at 6 and 18
        # Using a simple quadratic function for approximation
        normalized_hour = hour - 6  # Now ranges from 0 to 12
        # Quadratic that peaks at 6 (which is noon in normalized hours)
        # y = -a(x-6)^2 + max_capacity
        # At x=0 and x=12, y=0
        # So a = max_capacity / 36
        a = max_capacity / 36
        solar_output = -a * (normalized_hour - 6)**2 + max_capacity
        
        return max(0, solar_output)  # Ensure not negative

    solar_output = get_solar_power(hour)
    
    # Power plant data
    plants = [
        # Hydro plants (will be set to monthly values)
        {"name": "Victoria", "full_capacity": 140, "cost": 2.54, "type": "hydro"},
        {"name": "Kotmale", "full_capacity": 120, "cost": 2.54, "type": "hydro"},
        {"name": "Upper Kotmale", "full_capacity": 120, "cost": 2.54, "type": "hydro"},
        {"name": "Randenigala", "full_capacity": 120, "cost": 2.54, "type": "hydro"},
        {"name": "Samanalawewa", "full_capacity": 100, "cost": 2.54, "type": "hydro"},
        {"name": "New Laxapana", "full_capacity": 88, "cost": 2.54, "type": "hydro"},
        {"name": "Kukule", "full_capacity": 80, "cost": 2.54, "type": "hydro"},
        {"name": "Polpitiya", "full_capacity": 100, "cost": 2.54, "type": "hydro"},
        {"name": "Canyon", "full_capacity": 80, "cost": 2.54, "type": "hydro"},
        {"name": "Rantambe", "full_capacity": 48, "cost": 2.54, "type": "hydro"},
        {"name": "Wimalasurendra", "full_capacity": 72, "cost": 2.54, "type": "hydro"},
        {"name": "Old Laxapana", "full_capacity": 80, "cost": 2.54, "type": "hydro"},
        {"name": "Bowathenna", "full_capacity": 60, "cost": 2.54, "type": "hydro"},
        {"name": "Ukuwela", "full_capacity": 60, "cost": 2.54, "type": "hydro"},
        {"name": "Broadlands", "full_capacity": 100, "cost": 2.54, "type": "hydro"},
        
        # Mini Hydro (special treatment)
        {"name": "Minihydro Telemetered", "full_capacity": 60, "cost": 13.76, "type": "mini_hydro"},
        
        # Thermal plants
        {"name": "Biomass + W2E6", "full_capacity": 40, "cost": 39.48, "type": "thermal"},
        {"name": "KPS(GT7)", "full_capacity": 100, "cost": 65.47, "type": "thermal"},
        {"name": "KPS(GT)", "full_capacity": 100, "cost": 65.47, "type": "thermal"},
        {"name": "KCCP", "full_capacity": 100, "cost": 65.47, "type": "thermal"},
        
        # LVPS plants (coal)
        {"name": "LVPS 1", "full_capacity": 300, "cost": 25.00, "type": "lvps", "min_capacity": 180},
        {"name": "LVPS 2", "full_capacity": 300, "cost": 25.00, "type": "lvps", "min_capacity": 180},
        {"name": "LVPS 3", "full_capacity": 300, "cost": 25.00, "type": "lvps", "min_capacity": 180},
        
        # Other plants
     #   {"name": "Indian Link", "full_capacity": 500, "cost": indian_link_price, "type": "interconnect"},
        {"name": "ACE Matara", "full_capacity": 120, "cost": 65.47, "type": "thermal"},
        {"name": "Asia Power", "full_capacity": 120, "cost": 65.47, "type": "thermal"},
        {"name": "Sojitz Kelanitissa", "full_capacity": 160, "cost": 65.47, "type": "thermal"},
        {"name": "West Coast", "full_capacity": 200, "cost": 65.47, "type": "thermal"},
        {"name": "ACE-Embilipitiya", "full_capacity": 140, "cost": 65.47, "type": "thermal"},
        {"name": "Sapugaskanda Station - A", "full_capacity": 120, "cost": 65.47, "type": "thermal"},
        {"name": "Sapugaskanda Station - B", "full_capacity": 120, "cost": 65.47, "type": "thermal"},
        {"name": "Uthuru Janani", "full_capacity": 60, "cost": 65.47, "type": "thermal"},
        {"name": "Power Barge", "full_capacity": 80, "cost": 65.47, "type": "thermal"},
        {"name": "Solar", "full_capacity": 1470, "cost": 19.54, "type": "renewable"},
        {"name": "Wind", "full_capacity": 50, "cost": 17.25, "type": "renewable"}
    ]

    # Set hydro capacities based on month
    for plant in plants:
        if plant["type"] == "hydro" and plant["name"] in monthly_data[month]:
            plant["available_capacity"] = monthly_data[month][plant["name"]]
        
        elif plant["type"] == "mini_hydro":
            if season == "dry":
                plant["available_capacity"] = 0  # Mini hydro = 0 in dry season
            else:
                # 75% capacity in wet season (midpoint of 70-80%)
                plant["available_capacity"] = plant["full_capacity"] * 0.75
        
        elif plant["name"] == "Solar":
            # Set solar capacity based on hour of day
            plant["available_capacity"] = solar_output
        
        else:
            plant["available_capacity"] = plant["full_capacity"]

    # Separate LVPS plants
    lvps_plants = [p for p in plants if p["type"] == "lvps"]
    other_plants = [p for p in plants if p["type"] != "lvps"]
    
    # Sort other plants by cost (cheapest first)
    other_plants_sorted = sorted(other_plants, key=lambda x: x["cost"])
    
    dispatch = {}
    remaining_demand = demand
    total_cost = 0
    total_capacity = sum(p["available_capacity"] for p in plants)
    
    # Get time string for display
    if hour == 12:
        time_str = "12 noon"
    elif hour == 24:
        time_str = "12 midnight"
    elif hour < 12:
        time_str = f"{hour}am"
    else:
        time_str = f"{hour-12}pm"
    
    print(f"\nEconomic Dispatch for {demand} MW Demand at {time_str} ({season.capitalize()} season, {month.capitalize()}):")
    print(f"Solar Power Available: {solar_output:.2f} MW")
    print("="*100)
    print("{:<30} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
        "Power Plant", "Type", "Capacity (MW)", "Available (MW)", "Dispatched (MW)", "Cost (LKR/h)"))
    print("-"*100)
    
    # First handle LVPS plants (fixed at 600MW total, with each plant at least 180MW if running)
    lvps_demand = min(remaining_demand, 600)  # Fixed 600MW instead of random
    if lvps_demand > 0:
        # Distribute among LVPS plants (each gets 200MW when running)
        for plant in lvps_plants:
            if lvps_demand >= 180:  # Check if we can meet minimum capacity
                dispatched = min(200, lvps_demand)  # Each unit gets up to 200MW
                dispatch[plant["name"]] = dispatched
                hourly_cost = dispatched * plant["cost"] * 1000
                total_cost += hourly_cost
                remaining_demand -= dispatched
                lvps_demand -= dispatched
                
                print("{:<30} {:<15} {:<15.2f} {:<15.2f} {:<15.2f} {:<15,.2f}".format(
                    plant["name"], plant["type"].title(), plant["full_capacity"],
                    plant["available_capacity"], dispatched, hourly_cost))
            else:
                dispatch[plant["name"]] = 0
    
    # Then dispatch remaining demand to other plants
    for plant in other_plants_sorted:
        if remaining_demand <= 0:
            dispatch[plant["name"]] = 0
            continue
        
        # Dispatch as much as possible from this plant
        dispatched = min(plant["available_capacity"], remaining_demand)
        dispatch[plant["name"]] = dispatched
        hourly_cost = dispatched * plant["cost"] * 1000
        total_cost += hourly_cost
        remaining_demand -= dispatched
        
        if dispatched > 0:  # Only print plants that are actually dispatched
            print("{:<30} {:<15} {:<15.2f} {:<15.2f} {:<15.2f} {:<15,.2f}".format(
                plant["name"], plant["type"].replace("_", " ").title(),
                plant["full_capacity"], plant["available_capacity"],
                dispatched, hourly_cost))
    
    print("="*100)
    print(f"Total dispatched: {demand - remaining_demand:.2f} MW of {demand} MW demanded")
    print(f"Total system capacity: {total_capacity:.2f} MW (adjusted for season/month)")
    print(f"Total hourly cost: {total_cost:,.2f} LKR/h")
    print(f"Average cost per kWh: {(total_cost/(demand * 1000)):.2f} LKR/kWh")
    
    if remaining_demand > 0:
        print(f"\nWARNING: {remaining_demand:.2f} MW demand could not be met!")
        print("Consider adding more generation capacity or implementing load shedding.")
    
    return dispatch, total_cost, plants  # Return plants list for saving to file

# Example usage
if __name__ == "__main__":
    print("Sri Lanka Power System Economic Dispatch")
    print("="*60)
    print("Note: LVPS plants will automatically handle 600MW (200MW per unit)")
    
    try:
        demand = float(input("\nEnter total electricity demand in MW: "))
        if demand <= 0:
            raise ValueError("Demand must be positive.")
            
        indian_link_price = float(input("Enter Indian Link price (LKR/kWh): "))
        month = input("Enter month (3-letter abbreviation, e.g., jan, feb): ").strip().lower()
        hour = int(input("Enter hour (1-24, where 1=1am, 12=noon, 24=midnight): "))
        
        dispatch_results, total_cost, plants = economic_dispatch(demand, indian_link_price, month, hour)
        
        # Option to save results to file
        save = input("\nSave results to file? (y/n): ").lower()
        if save == 'y':
            # Determine season for filename
            dry_season_months = ['dec', 'jan', 'feb', 'mar', 'apr']
            season = 'dry' if month in dry_season_months else 'wet'
            
            # Get time string for filename
            if hour == 12:
                time_str = "12noon"
            elif hour == 24:
                time_str = "12midnight"
            elif hour < 12:
                time_str = f"{hour}am"
            else:
                time_str = f"{hour-12}pm"
            
            filename = f"dispatch_{month}_{season}_{time_str}_{demand}MW.txt"
            with open(filename, "w") as f:
                f.write(f"Economic Dispatch Results\n")
                f.write(f"Date: {month.capitalize()} ({season.capitalize()} season)\n")
                f.write(f"Time: {time_str}\n")
                f.write(f"Demand: {demand} MW\n")
                f.write(f"Indian Link Price: {indian_link_price} LKR/kWh\n")
                f.write("="*70 + "\n")
                f.write("{:<30} {:<15} {:<15}\n".format("Power Plant", "Type", "Dispatched (MW)"))
                for plant, amount in dispatch_results.items():
                    if amount > 0:
                        plant_type = next(p["type"] for p in plants if p["name"] == plant)
                        f.write("{:<30} {:<15} {:<15.2f}\n".format(
                            plant, plant_type.replace("_", " ").title(), amount))
                f.write("\nTotal dispatched: {:.2f} MW\n".format(sum(dispatch_results.values())))
                f.write(f"Total hourly cost: {total_cost:,.2f} LKR/h\n")
                f.write(f"Average cost: {(total_cost/(demand * 1000)):.2f} LKR/kWh\n")
            print(f"Results saved to {filename}")
            
    except ValueError as e:
        print(f"Error: {e}")