"""S-specific complete read diagnostics, calls, queue and ownership observations."""
import copy
import dataclasses
import json
from pathlib import Path
from types import SimpleNamespace
import native_primitives as native
import staged_read as reader
import fixture_support as support
from cryptalis.crypto import keys
from direct_runtime_v2 import exact

R=Path(__file__).resolve().parent
observations=[]
negative=None

def expire(prepared,purpose):
    for identity,material in list(prepared.mutable_materials.items()):
        if identity[0]==purpose:prepared.mutable_materials[identity]=dataclasses.replace(material,expires=0)

def observe(case,groups):
    fixture=json.loads((R/'reused-fixtures.json').read_text())
    spec=next(v for v in fixture['vectors'] if v['name']==case['fixture'])
    field,tenant,record=support.fields(spec)
    group=case['lifecycle_group']
    if group not in groups:groups[group]=support.make_keys(spec,field,tenant)
    prepared=groups[group];prepared.trace.clear()
    raw=bytes.fromhex(spec['frame']) if case['scenario']!='null' else None
    order=[];events=[];hook_count=0
    old=reader.native_primitives
    def route(name):
        def call(*args):
            nonlocal hook_count
            index=len(order);order.append(name)
            native._reset()
            selector=case.get('selector') if case.get('selected_call_index')==index else None
            try:
                value=(getattr(native,name+'_fault')(*args,selector) if selector is not None else getattr(native,name)(*args))
            finally:events.append(native._snapshot())
            if case.get('expiry_after_index')==index:
                expire(prepared,case['expire_purpose']);hook_count+=1
            return value
        return call
    reader.native_primitives=SimpleNamespace(**{name:route(name) for name in ('sha256','hkdf_sha256','decrypt','hmac_sha256')})
    native._queue_seed(case['queue_count'])
    try:
        try:value=reader.open_text_staged(raw,field,tenant,record,prepared)
        except keys.CryptoFailure as exc:
            actual={k:getattr(exc,k) for k in ('code','stage','retryable','effects','remedy')}
            actual.update(exception=type(exc).__name__,value=None,
                operation_present=type(exc.operation_id) is str and bool(exc.operation_id),
                args_safe=exc.args==(f'{exc.code} during {exc.stage}. {exc.remedy} Operation {exc.operation_id}.',),
                cause_none=exc.__cause__ is None,suppress_context=exc.__suppress_context__)
        else:actual={'value':value,'value_type':type(value).__name__}
    finally:reader.native_primitives=old
    return {'id':case['id'],'result':actual,'trace':copy.deepcopy(prepared.trace),
            'primitive_order':order,'ownership':events,'queue':native._queue_take(),'expiry_hook_count':hook_count}

def run(mode):
    global negative
    manifest=json.loads((R/'WRAPPER_CASES_v2.json').read_text())
    groups={}
    for case in manifest['cases']:
        actual=observe(case,groups);exact(actual,case['expected']);observations.append(actual)
        target=manifest['negative_controls'].get(mode)
        if target==case['id']:
            mutated=copy.deepcopy(actual)
            if mode=='text':mutated['result']['value']+='!wrong!'
            elif mode=='stage':mutated['result']['stage']='wrong-stage'
            elif mode=='trace':mutated['trace'].pop()
            elif mode=='order':mutated['primitive_order'].reverse()
            elif mode=='transfer':mutated['ownership'][-1]['transfer']+=1
            elif mode=='queue':mutated['queue'].append(999)
            else:raise RuntimeError('Unknown negative')
            negative={'original_verified':True,'original':actual,'mutated':mutated}
            exact(mutated,case['expected']);raise RuntimeError('Negative unexpectedly accepted')
    exact([o['id'] for o in observations],[c['id'] for c in manifest['cases']])
    if mode!='positive':raise RuntimeError('Negative target not reached')
