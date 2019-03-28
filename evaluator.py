from __future__ import annotations
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from solutions.RouteUnit import RouteUnit

class Evaluator:

    def __init__(self, queue_in : mp.Queue, queue_out : mp.Queue):
        self.pool = mp.Pool()
        self.queue_in = queue_in
        self.queue_out = queue_out

        self.eval_foo = lambda x: x.fitness

    def work(self):
        task_id, routes = self.queue_in.get()
        fitnesses = self.pool.map()
        self.queue_out.put( (task_id, fitnesses) )
