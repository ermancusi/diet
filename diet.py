import json
#from reportlab.lib import colors
#from reportlab.lib.pagesizes import letter, landscape
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
#from reportlab.lib.styles import getSampleStyleSheet
#from prettytable import PrettyTable

class Food:
    def __init__(self, name: str, proteins: float, fat: float, carbs: float, url: str):
        self.name = name
        self.proteins = proteins
        self.fat = fat
        self.carbs = carbs
        self.url = url
    
    def __str__(self):
        return (f"Food: {self.name}\n"
                f"Proteins: {self.proteins}g\n"
                f"Fat: {self.fat}g\n"
                f"Carbohydrates: {self.carbs}g\n")
                #f"More info: {self.url}")
 
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
        self.meal=set()
   
    def conversion(self, x1,x2):
        return (round(x1/100*x2,2))
    
    def computeMeal(self):
        s=""
        for k,v in self.ingredients.items():         
            ingredient=self.listOfIngredients[k]
            self.totalProteins+= self.conversion(v,ingredient.proteins) 
            self.totalFat+=self.conversion(v,ingredient.fat) 
            self.totalCarbs+=self.conversion(v,ingredient.carbs) 
            self.totalQuantity+=v
            self.meal.add(ingredient)            
            s+=f"{ingredient.name}, Quantità:{v}g, Proteine:{self.conversion(v,ingredient.proteins) }g, Grassi:{self.conversion(v,ingredient.fat) }g, Carboidrati:{self.conversion(v,ingredient.carbs)}g"
            s+="\n"
             
   
        self.totalProteins=round(self.totalProteins,2)
        self.totalFat=round(self.totalFat,2)
        self.totalCarbs=round(self.totalCarbs,2)
        self.totalQuantity=round(self.totalQuantity,2)

        s+=f"Total Quantity:{self.totalQuantity}g, Total Proteins:{self.totalProteins}g, Total Fat:{self.totalFat}g, Total Carbs:{self.totalCarbs}g"
        return(s)


    def __str__(self):
        return (self.computeMeal())
      

def import_food(filename):
    food={}
    with open(filename, "r", encoding="utf-8") as file:        
        for line in file:            
            if line.startswith("#"):
                continue
            fields = line.strip().split(",") 
            if len(fields) >= 5:
                name = fields[0]
                url = fields[1]
                proteins = fields[2]
                fat = fields[3]
                carbs = fields[4]
                
                food[name]=Food(name, float(proteins), float(fat), float(carbs),url)                

            else:                
                print("Invalid line format:", line.strip())
    return food
            
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


listOfIngredients=import_food("Assets\\food.txt" )
workout= read_json("Assets\\workout.json")
rest= read_json("Assets\\rest.json")

diet=workout
days={} 

for name in diet:
    meals={} 
    for meal in diet[name]:
        temp_ingredients={}       
        for ingredient in diet[name][meal]:            
            temp_ingredients[ingredient]=diet[name][meal][ingredient]["Quantità"]            
        meals[meal] = Meal(meal, temp_ingredients, listOfIngredients) 
          
        
    days[name]=Day(name, False, meals)


days_names=["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì","Sabato","Domenica"]

for x in days_names:    
    print(days[x])
    print ("====================")



