# Creates celery worker and defines the benchmark task to do
import os
from celery import Celery
from oct2py import octave

# Create cellery worker   # 130.238.28.125 = server ip
env = os.environ
CELERY_BROKER_URL = env.get('CELERY_BROKER_URL','amqp://group_11:wearegroup_11@130.238.28.125/group_11_vhost')
CELERY_RESULT_BACKEND = env.get('CELERY_RESULT_BACKEND','amqp://')

celery = Celery('tasks',
                broker = CELERY_BROKER_URL,
                backend = CELERY_RESULT_BACKEND)

# Run octave benchmark test for a specific problem (enviroment)
# Returns dictionary ['solver': [time, relative_error]]
@celery.task(name = 'celery_tasks.benchmark')
def benchmark(problem_to_solve,sig):
	# Matlab: function [time, relerr, filepaths] = tablee(problem_to_solve), problem_to_solve = [1:6]
	time, relerr, filepaths = octave.tablee(problem_to_solve,sig)
	# Making time and relerr into normal list and then "flattining" (dont want list in list [[]])
	timearray = [item for sublist in time.tolist() for item in sublist]
	relerrarray = [item for sublist in relerr.tolist() for item in sublist]
	# Merge three lists into dictionary
	return  {z[0]:list(z[1:]) for z in zip(filepaths,timearray,relerrarray)}
