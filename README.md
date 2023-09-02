# Temperature-control-regulator
Fuzzy Logic implementation for controlling AC temperature using parameters of temperature and humidity.

IDE : Visual Studio Code / Google Colab (for viewing the plotted graphs)

 ## Temperature-control-regulator

### Step-by-Step Explanation

#### Importing the necessary libraries
```python
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
```

####  Defining the input variables
```python
temp= ctrl.Antecedent(np.arange(0, 71), 'temperature')
hum = ctrl.Antecedent(np.arange(0, 101), 'humidity')
```

#### Defining the output variable
```python
cmd = ctrl.Consequent(np.arange(15, 60), 'command')
```

#### Defining the membership functions for the input variables
```python
temp['coldest'] = fuzz.trapmf(temp.universe, [-1, 0, 2,4])
temp['cold'] = fuzz.trapmf(temp.universe, [6, 8, 10, 12])
temp['normal'] = fuzz.trapmf(temp.universe, [12, 16, 18, 20])
temp['warm'] = fuzz.trapmf(temp.universe, [20, 22, 24, 26])
temp['hot'] = fuzz.trapmf(temp.universe, [26, 30, 32, 36])
temp['hottest'] = fuzz.trapmf(temp.universe, [36, 38, 40, 44])

hum['low'] = fuzz.gaussmf(hum.universe, 0, 45) 
hum['optimal'] = fuzz.gaussmf(hum.universe, 30, 60) 
hum['high'] = fuzz.gaussmf(hum.universe, 50, 100) 
```

#### Defining the membership functions for the output variable
```python
cmd['cool'] = fuzz.trimf(cmd.universe,[15, 22, 30])
cmd['no change'] = fuzz.trimf(cmd.universe, [23, 34, 45])
cmd['warmup'] = fuzz.trimf(cmd.universe, [35,48,60])
```

![Title](<Humidity vs Membership.png>) ![Title](<Command vs Membership.png>) ![Title](<Temperature vs Membership.png>)
