from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path
from .locks import FileLease, LockBusy
from .model import TaskResult, TaskSpec, CommandSpec
from .process_adapter import run_task
from .util import write_json_atomic

class SchedulerError(RuntimeError): pass

def blocked_result(task:TaskSpec,status:str,issue:str)->TaskResult:
    from datetime import datetime,timezone
    from hashlib import sha256
    now=datetime.now(timezone.utc).isoformat(); empty=sha256(b"").hexdigest()
    return TaskResult(task.task_id,task.command_id,status,None,list(task.expected_exit_codes),False,True,now,now,empty,empty,[],[],"NONE",{"kind":task.outcome_assertion.get("kind"),"failures":[],"errors":[]},[issue])

def run_dag(repo:Path,evidence:Path,tasks:dict[str,TaskSpec],commands:dict[str,CommandSpec],max_parallel:int,stop_policy:str)->dict[str,TaskResult]:
    pending=set(tasks); running={}; results={}; locks_root=evidence/'locks'
    def persist_blocked(result:TaskResult):
        task_dir=evidence/'tasks'/result.task_id; task_dir.mkdir(parents=True,exist_ok=True)
        (task_dir/'stdout.txt').write_text('',encoding='utf-8'); (task_dir/'stderr.txt').write_text('',encoding='utf-8')
        write_json_atomic(task_dir/'result.json',result.as_dict())
        return result
    def launch(pool,tid):
        task=tasks[tid]
        def worker():
            leases=[]
            try:
                for key in sorted(task.exclusivity_keys):
                    lease=FileLease(locks_root,key,tid); lease.__enter__(); leases.append(lease)
                return run_task(repo,evidence,task,commands[task.command_id])
            except LockBusy as exc:
                return persist_blocked(blocked_result(task,"BLOCKED_LOCK",f"LOCK_BUSY:{exc}"))
            finally:
                for lease in reversed(leases): lease.__exit__(None,None,None)
        running[pool.submit(worker)]=tid; pending.remove(tid)
    with ThreadPoolExecutor(max_workers=max_parallel) as pool:
        while pending or running:
            progressed=False
            for tid in sorted(list(pending)):
                task=tasks[tid]
                if any(dep not in results for dep in task.depends_on): continue
                bad=[dep for dep in task.depends_on if results[dep].status!="PASS"]
                if bad:
                    results[tid]=persist_blocked(blocked_result(task,"BLOCKED_DEPENDENCY","DEPENDENCY_NOT_PASS:"+",".join(bad))); pending.remove(tid); progressed=True; continue
                if stop_policy=="fail_fast_global" and any(r.status=="FAIL" and tasks[k].required for k,r in results.items()):
                    results[tid]=persist_blocked(blocked_result(task,"BLOCKED_DEPENDENCY","GLOBAL_FAIL_FAST")); pending.remove(tid); progressed=True; continue
                if len(running)<max_parallel:
                    launch(pool,tid); progressed=True
            if running:
                done,_=wait(running,return_when=FIRST_COMPLETED)
                for fut in done:
                    tid=running.pop(fut); results[tid]=fut.result(); progressed=True
            if not progressed and pending and not running: raise SchedulerError("DAG_STALLED")
    return results
