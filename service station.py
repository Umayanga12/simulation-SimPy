import random
import simpy
import numpy

NUMBER_EM_INSIDE_CLEAN = 4
NUMBER_EM_OUTSIDE_CLEAN = 6
NUMBER_EM_DRYING_FINAL = 3
AVERAGE_IN_CLEAN_TIME = 10
AVERAGE_OUT_CLEAN_TIME = 15
AVERAGE_FIANL_CLEAN_TIME = 10
INTERVAL = 5
SIM_TIME = 100
COMPLETE_CAR = 0

class CarWash:

    def __init__(self,env,num_em_in_clean,num_em_out_clean,num_em_final,out_clean_time,in_clean_time,final_time) -> None:
        self.env = env
        self.em_in_clean = simpy.Resource(env,num_em_in_clean)
        self.em_out_clean = simpy.Resource(env,num_em_out_clean)
        self.em_fianl = simpy.Resource(env,num_em_final)
        self.in_clean_time = in_clean_time
        self.out_clean_time = out_clean_time
        self.final_clean_time = final_time
    
    def in_clean(self,car_num) -> None:
        random_in_clean_time = max(1, numpy.random.normal(self.in_clean_time,9))
        yield self.env.timeout(random_in_clean_time)
        print(f"car {car_num} is leaving the inside cleaning unit at {self.env.now:.2f}")

    def out_clean(self,car_num) -> None:
        random_out_clean_time = max(1,numpy.random.normal(self.out_clean_time,14))
        yield self.env.timeout(random_out_clean_time)
        print(f"car {car_num} is leaving the outside cleaning unit at {self.env.now:.2f}")

    def final_clean(self,car_num) -> None:
        random_final_clean_time = max(1, numpy.random.normal(self.final_clean_time,9))
        yield self.env.timeout(random_final_clean_time)
        print(f"car {car_num} is leaving the final cleaning unit at {self.env.now:.2f}")


def car(env,car_num,car_wash) -> None:
    global COMPLETE_CAR
    print(f"car {car_num} is waiting at the queue {env.now:.2f}")
    with car_wash.em_in_clean.request() as request:
        yield request
        print(f"car {car_num} is enterd to the in clean at {env.now:.2f}")
        yield env.process(car_wash.in_clean(car_num))
        print(f"car {car_num} is leaving the in clean at {env.now:.2f}")
        COMPLETE_CAR += 1

def setup_process(env, num_in_em, num_out_em, num_final_em,interval,in_clean_time,out_clean_time,final_time) -> None:
    Car_Wash = CarWash(env,num_in_em,num_out_em,num_final_em,out_clean_time,in_clean_time,final_time)

    for i in range(1,6):
        env.process(car(env,i, Car_Wash))
    
    while True:
        yield env.timeout(random.randint(interval-1, interval+1))
        i +=1
        env.process(car(env, i, Car_Wash))

print("Car wash simulator started")
env = simpy.Environment()
env.process(setup_process(env,NUMBER_EM_INSIDE_CLEAN,NUMBER_EM_OUTSIDE_CLEAN,NUMBER_EM_DRYING_FINAL,INTERVAL,AVERAGE_IN_CLEAN_TIME,AVERAGE_OUT_CLEAN_TIME,AVERAGE_FIANL_CLEAN_TIME))
env.run(until=SIM_TIME)
print("-----------------------")
print(f"Total car completed {COMPLETE_CAR}")