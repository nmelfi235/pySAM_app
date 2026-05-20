from rich import print

import PySAM.Grid as grid
import PySAM.Battery as battery
import PySAM.Utilityrate5 as utilityrate5
import PySAM.Cashloan as cashloan

'''
TODO:
- This module will generate a SAM model which data will run through
'''

model_name = "StandaloneBatteryCommercial"

def run(data):
    battery_model = battery.default(model_name)
    grid_model = grid.from_existing(battery_model, model_name)
    utilityrate_model = utilityrate5.from_existing(grid_model, model_name)
    cashloan_model = cashloan.from_existing(utilityrate_model, model_name)

    print("[italic]Standalone Battery: Commercial Results[/italic]")
    print("Executing battery model...")
    battery_model.execute()
    print(f"[lightblue]Roundtrip Efficiency[/lightblue] = {battery_model.Outputs.average_battery_roundtrip_efficiency:.2f}%")

    print("\nExecuting grid model...")
    grid_model.execute()
    print(f"[orange]System Power Generated[/orange] = {grid_model.Outputs.gen[0]:.2f} kWh")

    print("\nExecuting utilityrate model...")
    utilityrate_model.execute()
    print(f"[yellow]Bill Peak Demand Charge[/yellow] = ${utilityrate_model.Outputs.monthly_tou_demand_charge_w_sys[1][1]:,.2f}")

    print("\nExecuting cashloan model...")
    cashloan_model.execute()
    print(f"[green]Cash Flow[/green] = ${cashloan_model.Outputs.cf_after_tax_cash_flow[1]:,.2f}")

    return {'battery': battery_model.Outputs.export(), 'grid': grid_model.Outputs.export(), 'utilityrate': utilityrate_model.Outputs.export(), 'cashloan': cashloan_model.Outputs.export()}

if __name__ == '__main__':
    run({'load': []})