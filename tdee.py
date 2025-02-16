#https://youtu.be/AMWJgXgx-XM

#https://tdeecalculator.net/result.php?s=metric&g=male&age=25&kg=65&cm=178&act=1.2&bf=20&f=1

surplus=200     #Cal
sedentary_maintenance=1792 #Cal
weight=65          #kg
height=178         #cm
carbo_Cal=4        #1g carboidrati = 4Cal
protein_Cal=4      #1g protein = 4Cal
fat_Cal=9          #1g fat = 9Cal

print ("Weight: ", weight, "kg")
print ("Height: ", height, "cm")
print ("TDEE with no fitness: ", sedentary_maintenance, "Cal")

print()

def compute_All(sedentary_maintenance=1792):
    workout=[0,400] #Cal
    for w in workout:
        daily_requirement=sedentary_maintenance+w+surplus
        
        protein_factor=2.2  #2 or 2.2 #32%
        daily_protein=protein_factor*weight #g
         
        fat_factor=(20)/100 #Body Fat Percentage #20%
        daily_fat=(fat_factor*daily_requirement)/fat_Cal #g
         
        daily_carbo=(daily_requirement-(daily_protein*protein_Cal) - (daily_fat*fat_Cal))/carbo_Cal
        #48% 
        print("==========================================================")
        if w !=0:
            print ("Diet with", surplus, "Cal of surplus and with workout (",w,") Cal")
        else:
            print ("Diet with", surplus, "Cal of surplus and without workout (",w,") Cal")
        print()
        print ("Dailiy Proteins: ", round(daily_protein,2), "g")
        print ("Dailiy Fat: ", round(daily_fat,2), "g")
        print ("Dailiy Carbo: ", round(daily_carbo,2), "g")
        
        print()
        
        print ("Proteins Percentage: ",round(daily_protein*protein_Cal/daily_requirement*100,2),"%")
        print ("Fat Percentage: ",round(daily_fat*fat_Cal/daily_requirement*100,2),"%")
        print ("Carbo Percentage: ",round(daily_carbo*carbo_Cal/daily_requirement*100,2),"%")
        
        print()
        print("==========================================================")
    
    
  
compute_All(sedentary_maintenance=1792)

#1kg=7700Cal
theoric_monthly_kg=surplus*30/7700 #kg gained in a month
print()
print("Theoretic kg gained in a month: ", round(theoric_monthly_kg,2),"kg")
    

real_monthly_kg=0.68
print("Real kg gained in a month ",real_monthly_kg,"kg")

delta=abs(real_monthly_kg-theoric_monthly_kg)
new_sedentary_maintenance=0

if (real_monthly_kg!=theoric_monthly_kg):
    extra_calories=delta*7700/30
    if (real_monthly_kg>theoric_monthly_kg):
        real_surplus=surplus+extra_calories
        print()
        print("The real surplus is:", round(real_surplus,2),"Cal")
        new_sedentary_maintenance=sedentary_maintenance-extra_calories
        print("The real sedentary maintenance is: ", round(new_sedentary_maintenance,2),"Cal")
    else:
        real_surplus=surplus-extra_calories
        print()
        print("The real surplus is:", round(real_surplus,2),"Cal")
        new_sedentary_maintenance=sedentary_maintenance+extra_calories
        print("The real sedentary maintenance is: ", round(new_sedentary_maintenance,2),"Cal")
