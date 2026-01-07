import queue,time
log_queue=queue.Queue()
def log(m):log_queue.put(f"[{time.strftime('%H:%M:%S')}] {m}")
