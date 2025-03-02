#https://youtu.be/AMWJgXgx-XM

# [04/02/2025 - 02/03/2025] https://tdeecalculator.net/result.php?s=metric&age=25&g=male&cm=178&kg=67.3&act=1.2&bf=20&f=1
# [03/02/2025 - xx/03/2025] https://tdeecalculator.net/result.php?s=metric&g=male&age=25&kg=65&cm=178&act=1.2&bf=20&f=1

import math

surplus =200                     #Cal
estimated_rest_tdee=1946         #Cal

weight=67.3                      #kg
height=178                       #cm

carbo_Cal=4                      #1g carboidrati = 4Cal
protein_Cal=4                    #1g protein = 4Cal
fat_Cal=9                        #1g fat = 9Cal

protein_factor=2.2              
fat_factor=(20)/100              #fats in the diet
one_kg_in_Cal=7000               #1kg of mass= 7000 Cal
monthly_muscles=0.8              #1 month = 0.8kg of muscles

def compute_macro(tdee):
    workout=[0,300] #Cal
    for w in workout:
        daily_requirement=tdee+surplus+w        
       
        # the following quantities are in grams
        daily_protein=round(protein_factor*weight,2)  
        
        daily_fat=round((fat_factor*daily_requirement)/fat_Cal,2)
         
        daily_carbo=round((daily_requirement-(daily_protein*protein_Cal) - (daily_fat*fat_Cal))/carbo_Cal,2)
        

        total_calories= (round((daily_protein+daily_carbo)*4+daily_fat*9,1)) #math.ceil(round((daily_protein+daily_carbo)*4+daily_fat*9,2))

        if w==0:
            print ("REST", end="===> ")
        else:
            print("WORKOUT", end="===> ")

        print("TDEE: {}, surplus: {}, workout: {}, Total Cal: {}".format(tdee, surplus, w, total_calories))
         
        print ("\nDailiy Proteins: ", daily_protein, "g")
        print ("Dailiy Fat: ", daily_fat, "g")
        print ("Dailiy Carbo: ", daily_carbo, "g")

        
                
        #print ("\nProteins Percentage: ",round(daily_protein*protein_Cal/daily_requirement*100,2),"%")
        #print ("Fat Percentage: ",round(daily_fat*fat_Cal/daily_requirement*100,2),"%")
        #print ("Carbo Percentage: ",round(daily_carbo*carbo_Cal/daily_requirement*100,2),"%")
               
        if w==0:
            print("\n==========================================================\n")
    

def compute_new_TDEE(measured_weight, surplus, estimated_tdee, days_under_test):
    new_estimated_rest_tdee=0
    initial_weight=66.6
    
    expected_weight= round((initial_weight) + (surplus*days_under_test/one_kg_in_Cal) + (monthly_muscles/30*days_under_test),2)
       
    delta_weight=round(measured_weight-expected_weight,2)
    
    delta_calories_daily= (delta_weight*7000)/days_under_test
         
    new_estimated_rest_tdee=round(estimated_tdee-delta_calories_daily,2)

    
    real_surplus= round((estimated_tdee+surplus) - new_estimated_rest_tdee,2)
    real_kg_from_diet=real_surplus*days_under_test/7000
    real_kg_gained= round(initial_weight + real_kg_from_diet + monthly_muscles/30*days_under_test,2)

    print("Expected kg gained in {} days: {} kg".format(days_under_test,expected_weight))    
    print("Real kg gained in {} days: {} kg".format(days_under_test,measured_weight))

    print("New Estimated Rest TDEE: {}".format(new_estimated_rest_tdee)) 

    """
    print("Real surplus in the test {}".format(real_surplus)) 
    print("Real kg from the diet {}".format(real_kg_from_diet)) 
    print("Real kg gained {}".format(real_kg_gained)) 
    """
    



compute_macro(estimated_rest_tdee)

#compute_new_TDEE(67.3, surplus, estimated_rest_tdee, 21)