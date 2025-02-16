from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfMerger
import json
import os


class Food:
    def __init__(self, name: str, proteins: float, fat: float, carbs: float, url: str, coeff: float):
        self.name = name
        self.proteins = proteins
        self.fat = fat
        self.carbs = carbs
        self.url = url
        self.coeff = coeff     
    
    def __str__(self):
        return (f"Food: {self.name}\n"
                f"Proteins: {self.proteins}g\n"
                f"Fat: {self.fat}g\n"
                f"Carbohydrates: {self.carbs}g\n")
                #f"More info: {self.url}"

class Day:
    def __init__(self, name: str, workout: bool, meals:dict):
        self.name = name
        self.workout = workout
        self.meals = meals
   
    
    def __str__(self):
        meal_strings = []   
        for meal_name, meal_object in self.meals.items():                
            meal_strings.append(f"{meal_name}:\n{meal_object}")

        
       
        return (f"Day: {self.name}\n"
                f"Workout: {self.workout}\n"
                f"Meals:\n" + 
                "\n\n\n".join(meal_strings)) 
        
class Meal:
    def __init__(self, name: str, ingredients: dict, listOfIngredients:dict):
        self.name = name
        self.ingredients = ingredients
        self.listOfIngredients = listOfIngredients
        self.totalProteins=0.0
        self.totalFat=0.0
        self.totalCarbs=0.0
        self.totalQuantity=0.0
        self.totalWater=0.0
        self.meal=set()
   
    def conversion(self, x1,x2):
        return (round(x1/100*x2,2))
    
    def computeMeal(self):
        s1=""
        s2=""
        for k,v in self.ingredients.items():         
            ingredient=self.listOfIngredients[k]
            self.totalProteins+= self.conversion(v,ingredient.proteins) 
            self.totalFat+=self.conversion(v,ingredient.fat) 
            self.totalCarbs+=self.conversion(v,ingredient.carbs) 
            self.totalQuantity+=v*ingredient.coeff
            if ingredient.coeff>1:
               self.totalWater+= v*(ingredient.coeff-1)
            if ingredient.name=="Latte di Mucca Scremato":
               self.totalWater+=v*0.9
            self.meal.add(ingredient)            
            s1=f"{ingredient.name}, Quantità:{v}g, Proteine:{self.conversion(v,ingredient.proteins) }g, Grassi:{self.conversion(v,ingredient.fat) }g, Carboidrati:{self.conversion(v,ingredient.carbs)}g"
            
             
   
        self.totalProteins=round(self.totalProteins,2)
        self.totalFat=round(self.totalFat,2)
        self.totalCarbs=round(self.totalCarbs,2)
        self.totalQuantity=round(self.totalQuantity,2)

        s2=f"Total Quantity:{self.totalQuantity}g, Total Water Assumed:{round(self.totalWater,2)}, Total Proteins:{self.totalProteins}g, Total Fat:{self.totalFat}g, Total Carbs:{self.totalCarbs}g"
        return(s1,s2, round(self.totalWater,2))


    def __str__(self):
        return (self.computeMeal())
      
def import_food(filename):
    food={}
    with open(filename, "r", encoding="utf-8") as file:        
        for line in file:            
            if line.startswith("#"):
                continue
            fields = line.strip().split(",") 
            if len(fields) >= 6:
                name = fields[0]
                url = fields[1]
                proteins = fields[2]
                fat = fields[3]
                carbs = fields[4]
                coeff = fields[5]
                
                food[name]=Food(name, float(proteins), float(fat), float(carbs),url, float(coeff))                

            else:                
                print("Invalid line format:", line.strip())
    return food
            
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
    
weight=66.7
listOfIngredients=import_food("Assets\\food.txt" )
workout= read_json("Assets\\workout.json")
rest= read_json("Assets\\rest.json")

days_names=["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

diet=workout

is_rest = diet == rest 

days={} 

for name in diet:
    meals={} 
    for meal in diet[name]:
        temp_ingredients={}       
        for ingredient in diet[name][meal]:            
            temp_ingredients[ingredient]=diet[name][meal][ingredient]["Quantità"]            
        meals[meal] = Meal(meal, temp_ingredients, listOfIngredients) 
          
        
    days[name]=Day(name, False, meals)


waterToAssume=round(0.03*weight*1000,2)


"""
print_flag=True

if print_flag:
    for x in days_names:    
        day=days[x]
        meals=day.meals
        waterFromFood=0.0
        print(day.name)
        for k, v in meals.items():
            s1,s2,totalWater=v.computeMeal()
            waterFromFood+=totalWater
            print(s2)
        s=f"To drink from water: {round((waterToAssume-waterFromFood)/1000,2)} L"  
        print(s)
        print("\n\n")    


if not print_flag:
    for x in days_names:    
        day=days[x]
        meals=day.meals
        waterFromFood=0.0
        print(day.name)
        for k, v in meals.items():
            s1,s2,totalWater=v.computeMeal()
            waterFromFood+=totalWater
            print(s1)
        s=f"To drink from water: {round((waterToAssume-waterFromFood)/1000,2)} L"  
        print(s)
        print("\n\n")   
"""


class PDFReport:
    def __init__(self, filename):
        self.filename = filename

    def generate_table(self, data, day_name, water_to_drink, is_rest):
        pdf = SimpleDocTemplate(self.filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        title_suffix = "REST" if is_rest else "WORKOUT"
        elements.append(Paragraph(f"Diet Plan for {day_name} - {title_suffix}", styles['Title']))
        elements.append(Spacer(1, 12))
        
        for meal_name, meal in data.items():
            elements.append(Paragraph(f"Meal: {meal_name}", styles['Heading2']))
            table_data = [["Ingredient", "Quantity (g)", "Proteins (g)", "Fat (g)", "Carbohydrates (g)","Water Quantity (ml)"]]
            
            for ingredient in meal.meal:
                water_quantity = (
                    round(meal.ingredients[ingredient.name] * (ingredient.coeff-1),2) if ingredient.coeff > 1 else
                    round(meal.ingredients[ingredient.name]*0.9,2) if ingredient.name.startswith("Latte") else
                    0
                 )
                table_data.append([
                    ingredient.name,
                    meal.ingredients[ingredient.name],                   
                    round(meal.conversion(meal.ingredients[ingredient.name], ingredient.proteins), 2),
                    round(meal.conversion(meal.ingredients[ingredient.name], ingredient.fat), 2),
                    round(meal.conversion(meal.ingredients[ingredient.name], ingredient.carbs), 2),
                    water_quantity
                ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 12))
        
        elements.append(Paragraph(f"Total Water to Drink: {water_to_drink} L", styles['Heading2']))
        pdf.build(elements)

pdf_files = []

for x in days_names:
    day = days[x]
    meals = day.meals
    waterFromFood = 0.0
    
    for meal in meals.values():
        _, _, totalWater = meal.computeMeal()
        waterFromFood += totalWater
    
    water_to_drink = round((waterToAssume - waterFromFood) / 1000, 2)
    pdf_filename = f"diet_{x}.pdf"
    pdf_report = PDFReport(pdf_filename)
    pdf_report.generate_table(meals, x, water_to_drink,is_rest)
    pdf_files.append(pdf_filename)

merger = PdfMerger()
for pdf_file in pdf_files:
    merger.append(pdf_file)

if not is_rest:
    merger.write("Workout Diet.pdf")
else: 
    merger.write("Rest Diet.pdf")
merger.close()

for pdf_file in pdf_files:
    try:
        os.remove(pdf_file)
    except Exception as e:
        print(f"Error deleting {pdf_file}: {e}")