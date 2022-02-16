#-*- encoding:UTF-8 -*-
'''
Created on 2021/2/20

@author: xcKev
'''

from multiprocessing import Process

def execute_thread_pool(thread_pool,task_list,func,*args):
    future=thread_pool.submit(func,*args)
    task_list.append(future)
    return task_list

def execute_thread_pool_task(thread_pool,func,*args):
    future=thread_pool.submit(func,*args)
    return future

def run_with_limited_second(func,args,kwargs,seconds):
    """Runs a function with time limit

    :param func: The function to run
    :param args: The functions args, given as tuple
    :param kwargs: The functions keywords, given as dict
    :param seconds: The time limit in seconds
    :return: True if the function ended successfully. False if it was terminated.
    """
    p=Process(target=func,args=args,kwargs=kwargs)
    p.start()
    p.join(seconds)
    if p.is_alive():
        p.terminate()
        return False
    return True