from pathlib import Path
import json,hashlib
R=Path(__file__).parent;U=R.parent/'candidate-native-backend-observation-20261014'
s=(U/'native_cf1.c').read_text()
if hashlib.sha256(s.encode()).hexdigest()!='277ce47a7507a53b6aaf9286de2459a6201ea5c2e885f12f4a6e6321ad24d75a':raise RuntimeError('Unmarked source mismatch')
extra=r'''
/* Public semantic mark operations on this test's own queue only. */
static PyObject *mark_set(PyObject *self,PyObject *args) {
 (void)self;(void)args;return PyLong_FromLong(ERR_set_mark());
}
static PyObject *mark_pop(PyObject *self,PyObject *args) {
 (void)self;(void)args;return PyLong_FromLong(ERR_pop_to_mark());
}
static PyObject *mark_count(PyObject *self,PyObject *args) {
 (void)self;(void)args;return PyLong_FromLong(ERR_count_to_mark());
}
static PyObject *queue_append(PyObject *self,PyObject *arg) {
 (void)self;long i=PyLong_AsLong(arg);if(PyErr_Occurred())return NULL;
 if(i<1||i>2){PyErr_SetString(PyExc_ValueError,"Public append index 1..2");return NULL;}
 ERR_new();ERR_set_debug("public-sentinel.c",700+(int)i,"public_sentinel");
 ERR_set_error(ERR_LIB_USER,100+(int)i,"public-sentinel-%d",(int)i);Py_RETURN_NONE;
}
'''
s=s.replace('static PyMethodDef methods[]={',extra+'\nstatic PyMethodDef methods[]={\n {"mark_set",mark_set,METH_NOARGS,"Set public mark."},\n {"mark_pop",mark_pop,METH_NOARGS,"Consume public mark."},\n {"mark_count",mark_count,METH_NOARGS,"Public distance to mark."},\n {"queue_append",queue_append,METH_O,"Append public sentinel B or C."},')
with (R/'native_cf1.c').open('x') as f:f.write(s)
u=json.loads((U/'cases.json').read_text());cases=[]
# Independently prescribed public-operation outcomes, not runtime-derived.
def ent(i):return [(128<<23)|(100+i),'public-sentinel.c',700+i,'public_sentinel',f'public-sentinel-{i}',3]
A,B=ent(0),ent(1)
steps={
 'top-once':[(1,1,[A,B]),(3,0,[])],
 'top-twice':[(1,1,[A,B]),(1,1,[A,B]),(3,0,[])],
 'lower-once':[(2,1,[A]),(2,0,[])],
 'lower-plus-top':[(1,1,[A,B]),(2,1,[A]),(2,0,[])]}
for config,trace in steps.items():
 expected={'initial_endpoints':[A,B],'steps':[{'distance':d,'pop':p,'endpoints':([] if not q else [q[0],q[-1]])} for d,p,q in trace],'drained':[]}
 for variant in ['baseline','consume-one','add-one']:
  cases.append(dict(id=f'control-{config}-{variant}',kind='control',configuration=config,variant=variant,expected=expected,expect_equal=variant=='baseline'))
 for old in u['cases']:
  if old['sentinels']!=0:continue
  cases.append(dict(id=f"{config}-{old['rep']}-{old['action']}",kind='helper',configuration=config,rep=old['rep'],action=old['action'],expected_outcome=old['expected'],expected=expected,expect_equal=True))
with (R/'cases.json').open('x') as f:json.dump({'fixtures':u['fixtures'],'cases':cases},f,indent=2)
with (R/'build.py').open('x') as f:f.write((U/'build.py').read_text())

# Freeze independent exact negative-control traces as well as inequality.
mutations={
 ('top-once','consume-one'):([A,B],[(3,0,[]),(1,0,[])],[]),
 ('top-twice','consume-one'):([A,B],[(1,1,[A,B]),(3,0,[]),(1,0,[])],[]),
 ('lower-once','consume-one'):([A,A],[(2,0,[]),(1,0,[])],[]),
 ('lower-plus-top','consume-one'):([A,B],[(2,1,[A]),(2,0,[]),(1,0,[])],[]),
 ('top-once','add-one'):([A,B],[(1,1,[A,B]),(1,1,[A,B])],[A,B]),
 ('top-twice','add-one'):([A,B],[(1,1,[A,B]),(1,1,[A,B]),(1,1,[A,B])],[A,B]),
 ('lower-once','add-one'):([A,B],[(1,1,[A,B]),(2,1,[A])],[A]),
 ('lower-plus-top','add-one'):([A,B],[(1,1,[A,B]),(1,1,[A,B]),(2,1,[A])],[A])}
for c in cases:
 if c['kind']=='control' and c['variant']!='baseline':
  initial,seq,drain=mutations[(c['configuration'],c['variant'])]
  c['expected_mutated']={'initial_endpoints':initial,'steps':[{'distance':d,'pop':p,'endpoints':([] if not q else [q[0],q[-1]])} for d,p,q in seq],'drained':drain}
# Preparation only, before freeze/review; update generated manifest once.
(R/'cases.json').write_text(json.dumps({'fixtures':u['fixtures'],'cases':cases},indent=2))
