import random
import simpy
import numpy

num_step = int(input("Enter the number of steps of the simulation : "))
intervel = float(input("Enter the Intervel in between the entrance of two units : "))
weiting_q = int(input("Enter How many units are at the weiting queue : "))
sim_time = int(input("Enter the Simulation Time : "))
num_vars = num_step  
COMPLETE_UNIT = 0

args = []
for i in range(num_vars):
    var_name = "resource_" + str(i + 1)
    var_value = input("Enter the value for " + var_name + ": ")
    globals()[var_name] = var_value
    args.append(var_value)


arg_time = []
for i in range(num_vars):
    time_var_name = "Avg_time_step_" + str(i + 1)
    avg_time = int(input("Enter the average time for " + time_var_name +" : "))
    globals()[time_var_name] = avg_time
    arg_time.append(avg_time)

fun_name = []

for i in range(num_step):
    fun_name.append("Step_"+str(i+1))

def generate_step_functions(self):
    for n in fun_name:
        function_code = f"""
        def {fun_name}(self, unit_num) -> None:
            time = max(1, numpy.random.normal(self.{arg_time[n]}, 9))
            yield self.env.timeout(time)
            print(f"Unit {{unit_num}} is leaving the step at {{self.env.now:.2f}}")
        """

        exec(function_code, globals(), locals())

class sim:

    def __init__(self,env,args,arg_time) -> None:
        self.args = args
        self.env = env
        self.arg_time = arg_time    
        self.generate_step_functions()

def unit(env, unit_num,simulation) -> None:
    global COMPLETE_UNIT
    print("Unit {unit_num} is waiting at  the queue {env.now:.2f}")
    with simulation.Step_1.request() as request:
        yield  request
        print(f"{unit_num} is enterd to the step_1 at {env.now: .2f}")
        yield env.process(simulation.Step_1(unit_num))
        print(f"unit {unit_num} is leaving the step_1 at {env.noe: .2f}")
        COMPLETE_UNIT += 1

def setup_process(env,*args,arg_time,intervel) -> None:
    simulation = sim(env ,*args,*arg_time,intervel)
    for i in range(1,weiting_q):
        env.process(unit(env,i,simulation))

    while True:
        yield env.timeout(random.randint(intervel-1,intervel+1))
        i +=1
        env.process(unit(env,i,simulation))


print("Simulation Started ")
env = simpy.Environment()
env.process(setup_process(env,*args,arg_time,intervel))
env.run(until=sim_time)
print("-------------------------------")
print(f"Total {COMPLETE_UNIT} are Completed !!!!")
