
from collections import OrderedDict
from datetime import datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy

# database models and helper functions

db = SQLAlchemy()


class EnergyUsage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    avgElectricityBill = db.Column(db.Float, default = 0)
    naturalGasBill = db.Column(db.Float, default = 0)
    avgFuelBill = db.Column(db.Float, default = 0)
    
    def __init__(self, form) -> None:
        self.avgElectricityBill = form['avgElectricityBill']
        self.naturalGasBill = form['naturalGasBill']
        self.avgFuelBill = form['avgFuelBill']
    
    def calculate(self):
        total =  self.avgElectricityBill * 12 * 0.0005 + self.naturalGasBill * 12* 0.0053 + self.avgFuelBill * 12 * 2.32
        return total

class Waste(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    wasteGenerated = db.Column(db.Double, default = 0)
    wasteRecycled = db.Column(db.Double, default = 0)
    
    def __init__(self, form) -> None:
        self.wasteGenerated = form['wasteGenerated']
        self.wasteRecycled = (form['wasteRecycled']/self.wasteGenerated)
    
    def calculate(self):
        total = self.wasteGenerated * 12 * (0.57 - self.wasteRecycled)
        return total

class BusinessTravel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=datetime.now(UTC))
    travelPerYear = db.Column(db.Double, default = 0)
    fuelEfficiency = db.Column(db.Double, default = 0)
    
    def __init__(self, form) -> None:
        self.travelPerYear = form['travelPerYear']
        self.fuelEfficiency = form['fuelEfficiency']
    
    def calculate(self):
        total = self.travelPerYear * (1/ self.fuelEfficiency) * 2.31
        return total

columns = ['Record No', 
               'Date (mm/dd/YYYY)', 
               'Avergae Electricity Bill (euros/month)',
               'Average Gas Bill (euros/month)',
               'Average Fuel Bill (euros/month)',
               'CO2 Footprint for Energy Usage (kgCO2)',
               'Waste Generated (kg/month)',
               'Waste Recycled (in Percentage)',
               'CO2 Footprint for Waste (kgCO2) ',
               'Travel (km/year)',
               'Fuel Efficiency (Liters/100 km)',
               'CO2 Footprint For Travel (kgCO2)',
               'Total CO2 Footprint (kgCO2)']   

def getRecord(energy_usage, waste, travel):
    record = OrderedDict()
    record[columns[0]] = energy_usage.id
    record[columns[1]] = energy_usage.date_created.strftime("%x")+ " " + energy_usage.date_created.strftime("%X")
    record[columns[2]] = "{:.2f}".format(energy_usage.avgElectricityBill)
    record[columns[3]] = "{:.2f}".format(energy_usage.naturalGasBill)
    record[columns[4]] = "{:.2f}".format(energy_usage.avgFuelBill)
    record[columns[5]] = "{:.2f}".format(energy_usage.calculate())
    record[columns[6]] = "{:.2f}".format(waste.wasteGenerated)
    record[columns[7]] = str("{:.2f}".format(waste.wasteRecycled * 100)) + '%'
    record[columns[8]] = "{:.2f}".format(waste.calculate())
    record[columns[9]] = "{:.2f}".format(travel.travelPerYear)
    record[columns[10]] = "{:.2f}".format(travel.fuelEfficiency)
    record[columns[11]] = "{:.2f}".format(travel.calculate())
    record[columns[12]] = "{:.2f}".format(energy_usage.calculate() + waste.calculate() + travel.calculate())
    return record

def getHistory():

    energy_usage_list: List[EnergyUsage] = EnergyUsage.query.order_by(EnergyUsage.date_created).all()

    data = []

    for energy_usage in energy_usage_list:
        waste: Waste = Waste.query.get_or_404(energy_usage.id)
        business_travel: BusinessTravel = BusinessTravel.query.get_or_404(energy_usage.id)
        record = getRecord(energy_usage, waste, business_travel)
        data.append(record)
        
    return (columns, data)

def saveData(energy_usage, waste, travel):
    db.session.add_all([energy_usage, waste, travel])
    db.session.commit()
    

