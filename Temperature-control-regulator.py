import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


temp= ctrl.Antecedent(np.arange(0, 71), 'temperature')
hum = ctrl.Antecedent(np.arange(0, 101), 'humidity')


cmd = ctrl.Consequent(np.arange(15, 60), 'command')


temp['coldest'] = fuzz.trapmf(temp.universe, [-1, 0, 2,4])
temp['cold'] = fuzz.trapmf(temp.universe, [6, 8, 10, 12])
temp['normal'] = fuzz.trapmf(temp.universe, [12, 16, 18, 20])
temp['warm'] = fuzz.trapmf(temp.universe, [20, 22, 24, 26])
temp['hot'] = fuzz.trapmf(temp.universe, [26, 30, 32, 36])
temp['hottest'] = fuzz.trapmf(temp.universe, [36, 38, 40, 44])

hum['low'] = fuzz.gaussmf(hum.universe, 0, 45) 
hum['optimal'] = fuzz.gaussmf(hum.universe, 30, 60) 
hum['high'] = fuzz.gaussmf(hum.universe, 50, 100) 


cmd['cool'] = fuzz.trimf(cmd.universe,[15, 22, 30])
cmd['no change'] = fuzz.trimf(cmd.universe, [23, 34, 45])
cmd['warmup'] = fuzz.trimf(cmd.universe, [35,48,60])

rule1 = ctrl.Rule(
    (temp['coldest'] & hum['low']) |
    (temp['coldest'] & hum['optimal']) |
    (temp['coldest'] & hum['high']) |
    (temp['cold'] & hum['low']) |
    (temp['cold'] & hum['optimal']) |
    (temp['warm'] & hum['low']), cmd['warmup'])


rule2 = ctrl.Rule(
    (temp['warm'] & hum['optimal']) |
    (temp['warm'] & hum['high']) |
    (temp['hot'] & hum['low']) |
    (temp['hot'] & hum['optimal']) |
    (temp['hot'] & hum['high'])|
    (temp['hottest'] & hum['low']) |
    (temp['hottest'] & hum['optimal']) |
    (temp['hottest'] & hum['high']), cmd['cool'])
rule3=ctrl.Rule((temp['normal'] & hum['optimal']),cmd['no change'])
cmd_ctrl = ctrl.ControlSystem([rule1, rule2,rule3])
cmd_output = ctrl.ControlSystemSimulation(cmd_ctrl)


temperature_value = float(input("Enter temperature"))

while temperature_value < 0 or temperature_value > 70:
    try:
        temperature_value = float(input("Please choose a number between 0 and 70 "))
    except ValueError:
        print('We expect you to enter a valid integer')

humidity_value = float(input("Enter humidity"))

while humidity_value < 0 or humidity_value > 100:
    try:
        humidity_value = float(input("Please choose a number between 0 and 100 "))
    except ValueError:
        print('We expect you to enter a valid integer')

cmd_output.input['temperature'] = temperature_value
cmd_output.input['humidity'] = humidity_value

cmd_output.compute()


print("The working value thus obtained is : ")
print(cmd_output.output['command'])
if (cmd_output.output['command'] > 35):
    print('Warm Up')
elif (cmd_output.output['command'] < 45 and cmd_output.output['command'] > 23):
    print('No change')
else:
    print('Cool down')

cmd.view(sim=cmd_output)
temp.view()
hum.view()
