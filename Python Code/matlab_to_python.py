# Heart Rate
age = 22
max_HR = 220 - age
HR = 190
HR_weight = 0.50
HR_score = 1

lowest_nonfatigue_HR = max_HR * 0.64
highest_nonfatigue_HR = max_HR * 0.77
lowest_fatigue_HR = max_HR * 0.77
highest_fatigue_HR = max_HR

print(" ")
print("HR:", HR)
if HR < lowest_nonfatigue_HR:
    print('Error on Data (HR too low)')
elif lowest_nonfatigue_HR <= HR <= highest_nonfatigue_HR:
    print('Non-fatigued')
    print("HR Score Weight:", HR_score)
    print("HR Score:", HR_score * HR_weight)
elif lowest_fatigue_HR <= HR <= max_HR:
    print('Fatigued')
    HR_score = (1 - (HR - lowest_fatigue_HR) / (max_HR - lowest_fatigue_HR)) * 100
    print("HR Score Weight:", HR_score)
    print("HR Score (50%): ", HR_score * HR_weight)
else:
    print('Error on Data (HR too high)')

# Temperature
max_temp = 46.5
temp_fatigue = 38
temp_weight = 0.10
temp_score = 1
temp = 40

print(" ")
print("Temp:", temp, "C")
if temp < temp_fatigue:
    print('Non-fatigued')
    print("Temp Score Weight:", temp_score)
    print("HR Score:", temp_score * temp_weight)
elif temp > temp_fatigue:
    print('Fatigued')
    temp_score = (1 - (temp - temp_fatigue) / (max_temp - temp_fatigue)) * 100
    print("Temp Score Weight:", temp_score)
    print("Temp Score (10%): ", temp_score * temp_weight)
