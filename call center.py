import numpy as np
import simpy as sp
import random as rand

NUM_EMPLOYEE = 2
AVERAGE_HANDL_TIME = 5 
INTERVAL = 2
SIM_TIME = 120
HANDLED_COU = 0


#creating the call center as the class - environment
#employees at the call center are resources 
#when ititiate the perametres at the class need to comnsider environment, resources and the time durations for the process
class callcenter:

    def __init__(self,env,num_employee,support_time) -> None:
        self.env = env
        self.staff = sp.Resource(env, num_employee)
        self.support_time = support_time

    def support(self,customer):
        random_time = max(1, np.random.normal(self.support_time,4)) # support time is not a constant value. in here have use 1 as the minimal time and to get the ranom value for the time have use normal distribution with standerd deviation of 4 
        yield self.env.timeout(random_time)
        print(f"support fineshed for {customer} at {self.env.now:.2f}")


def customer(env, name, call_center) -> None:
    global HANDLED_COU
    print(f"customner {name} is waiting at the queue {env.now:.2f}")
    with call_center.staff.request() as request:
        yield request
        print(f"customer {name} is enterd to the call at {env.now:.2f}")
        yield env.process(call_center.support(name))
        print(f"customer {name} is leaving at {env.now:.2f}")
        HANDLED_COU += 1


def setup(env, num_employee, support_time, customer_interval) -> None:
    call_center = callcenter(env, num_employee,support_time)

    for i in range(1,6):
        env.process(customer(env,i, call_center))
    
    while True:
        yield env.timeout(rand.randint(customer_interval-1, customer_interval+1))
        i +=1
        env.process(customer(env, i, call_center))
        
print("Call center simiuation started")
env = sp.Environment()
env.process(setup(env, NUM_EMPLOYEE, AVERAGE_HANDL_TIME, INTERVAL))
env.run(until=SIM_TIME)
print("-----------------------")
print(f"Total customer handled {HANDLED_COU}")