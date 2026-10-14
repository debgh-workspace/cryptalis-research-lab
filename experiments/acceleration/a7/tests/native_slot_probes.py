"""Source-guarded observation probes in COPIES of two SQLAlchemy functions.

Research fork surface only. No product code, installed-file edit or crypto.
"""
import ast
from contextlib import contextmanager
from dataclasses import dataclass
import __future__
import inspect
import textwrap

from sqlalchemy.engine import default
from sqlalchemy.sql import compiler


class MissingNativeReceipt(Exception):
    pass


@dataclass
class DriverReceipt:
    context: object
    logical: object
    driver: object
    row: object
    slots: tuple


@dataclass
class BatchReceipt:
    context: object
    batch: object
    slots: tuple


class SlotProbe:
    def __init__(self, lineage):
        self.lineage = lineage
        self.bind_slots = []
        self.drivers = []
        self.imv_slots = []
        self.batches = []
        self.pending = None
        self.cursor_calls = []

    def bind_value(self, context, logical, source_key, output_slot, value):
        self.bind_slots.append((context, logical, source_key, output_slot, value))
        return value

    def driver_row(self, context, logical, driver):
        row = self.lineage.exact_compiled(logical)
        if row is None:
            raise MissingNativeReceipt('No exact native logical row')
        slots = tuple(item for item in self.bind_slots
                      if item[0] is context and item[1] is logical)
        if not slots:
            raise MissingNativeReceipt('No actual bind materialization slots')
        assert all(driver[item[3]] == item[4] for item in slots)
        self.bind_slots = [item for item in self.bind_slots
                           if not (item[0] is context and item[1] is logical)]
        self.drivers.append(DriverReceipt(context, logical, driver, row, slots))

    def exact_driver(self, driver):
        found = [item for item in self.drivers if item.driver is driver]
        if len(found) != 1:
            raise MissingNativeReceipt('Driver container lacks unique producer receipt')
        return found[0]

    def named_imv_value(self, sql_compiler, destination, source, source_slot, output_slot, value):
        self.exact_driver(source)
        self.imv_slots.append((sql_compiler, destination, source, source_slot, output_slot, value))
        return value

    def positional_imv_rows(self, sql_compiler, rows):
        # Called at native chain.from_iterable's actual input consumption.
        # Each input must be the exact native driver tuple, never a sliced copy.
        output_slot = 0
        for source in rows:
            self.exact_driver(source)
            if type(source) is not tuple:
                raise MissingNativeReceipt('Only native tuple positional rows are qualified')
            for source_slot, value in enumerate(source):
                self.imv_slots.append((sql_compiler, None, source, source_slot, output_slot, value))
                output_slot += 1
            yield source  # original chain.from_iterable still does materialization

    def batch_ready(self, sql_compiler, batch):
        if self.pending is not None:
            raise MissingNativeReceipt('Previous native batch was not consumed')
        driver_receipts = [self.exact_driver(row) for row in batch.batch]
        if not driver_receipts:
            raise MissingNativeReceipt('Empty native batch')
        context = driver_receipts[0].context
        assert all(item.context is context for item in driver_receipts)
        assert context.compiled is sql_compiler
        slots = tuple(item for item in self.imv_slots if item[0] is sql_compiler)
        self.imv_slots = [item for item in self.imv_slots if item[0] is not sql_compiler]
        if not slots:
            # Native downgrade yields do not pass through slot assembly probes.
            raise MissingNativeReceipt('Unqualified native IMV downgrade path')
        for _, destination, source, source_slot, output_slot, value in slots:
            assert any(source is row for row in batch.batch)
            assert destination is None or destination is batch.replaced_parameters
            assert batch.replaced_parameters[output_slot] == value
            assert source[source_slot] == value
        receipt = BatchReceipt(context, batch, slots)
        self.batches.append(receipt)
        self.pending = receipt
        return batch  # exact native NamedTuple, never rewritten

    def before_cursor(self, connection, cursor, statement, parameters, context, many):
        if not context.isinsert:
            return
        receipt = self.pending
        if (receipt is None or receipt.context is not context or
                receipt.batch.replaced_parameters is not parameters or
                receipt.batch.replaced_statement is not statement):
            raise MissingNativeReceipt('Cursor input differs from exact native producer receipt')
        for _, _, source, source_slot, output_slot, value in receipt.slots:
            driver = self.exact_driver(source)
            origin = [slot for slot in driver.slots if slot[3] == source_slot]
            assert len(origin) == 1
            assert origin[0][1] is driver.row.compiled
            # Values check integrity only AFTER source identity has been proved.
            assert parameters[output_slot] == value == origin[0][4]
        self.cursor_calls.append(receipt)
        self.pending = None


class ProbeTransformer(ast.NodeTransformer):
    def __init__(self, kind):
        self.kind = kind
        self.counts = {}

    def hit(self, name):
        self.counts[name] = self.counts.get(name, 0) + 1

    def call(self, name, args):
        return ast.Call(func=ast.Name(id=name, ctx=ast.Load()), args=args, keywords=[])

    def name(self, value):
        return ast.Name(id=value, ctx=ast.Load())

    def visit_ListComp(self, node):
        self.generic_visit(node)
        if (self.kind == 'context' and len(node.generators) == 1 and
                isinstance(node.generators[0].iter, ast.Name) and
                node.generators[0].iter.id == 'positiontup'):
            self.hit('positional_bind')
            generator = node.generators[0]
            generator.target = ast.Tuple(elts=[ast.Name(id='_receipt_slot', ctx=ast.Store()),
                                               generator.target], ctx=ast.Store())
            generator.iter = self.call('enumerate', [generator.iter])
            node.elt = self.call('_receipt_bind', [self.name('self'), self.name('compiled_params'),
                                  self.name('key'), self.name('_receipt_slot'), node.elt])
        return node

    def visit_DictComp(self, node):
        self.generic_visit(node)
        if self.kind == 'context' and any(
                isinstance(g.iter, ast.Name) and g.iter.id == 'compiled_params' for g in node.generators):
            self.hit('named_bind')
            node.key = ast.NamedExpr(target=ast.Name(id='_receipt_key', ctx=ast.Store()), value=node.key)
            node.value = self.call('_receipt_bind', [self.name('self'), self.name('compiled_params'),
                                    self.name('key'), self.name('_receipt_key'), node.value])
        elif self.kind == 'imv' and any(
                isinstance(g.iter, ast.Name) and g.iter.id == 'keys_to_replace' for g in node.generators):
            self.hit('named_imv')
            node.key = ast.NamedExpr(target=ast.Name(id='_receipt_imv_key', ctx=ast.Store()), value=node.key)
            node.value = self.call('_receipt_named_imv', [self.name('self'), self.name('replaced_parameters'),
                                    self.name('param'), self.name('key'), self.name('_receipt_imv_key'), node.value])
        return node

    def visit_Expr(self, node):
        self.generic_visit(node)
        call = node.value
        if (self.kind == 'context' and isinstance(call, ast.Call) and
                isinstance(call.func, ast.Attribute) and call.func.attr == 'append' and
                isinstance(call.func.value, ast.Name) and call.func.value.id in (
                    'core_dict_parameters', 'core_positional_parameters')):
            self.hit('driver_append')
            observed = ast.Expr(value=self.call('_receipt_driver', [self.name('self'),
                self.name('compiled_params'), ast.Subscript(value=call.func.value,
                    slice=ast.UnaryOp(op=ast.USub(), operand=ast.Constant(value=1)), ctx=ast.Load())]))
            return [node, ast.copy_location(observed, node)]
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        if self.kind != 'imv':
            return node
        if (isinstance(node.func, ast.Attribute) and node.func.attr == 'from_iterable' and
                len(node.args) == 1 and isinstance(node.args[0], ast.Name) and
                node.args[0].id == 'batch_iterator'):
            self.hit('positional_imv')
            node.args[0] = self.call('_receipt_positional_rows', [self.name('self'), node.args[0]])
        if isinstance(node.func, ast.Name) and node.func.id == '_InsertManyValuesBatch':
            self.hit('batch_yield')
            return self.call('_receipt_batch', [self.name('self'), node])
        return node


def instrument_copy(function, module, kind, probe):
    source = textwrap.dedent(inspect.getsource(function))
    tree = ast.parse(source)
    definition = tree.body[0]
    assert isinstance(definition, ast.FunctionDef)
    definition.decorator_list = []
    transformer = ProbeTransformer(kind)
    tree = transformer.visit(tree)
    expected = ({'positional_bind': 1, 'named_bind': 2, 'driver_append': 2}
                if kind == 'context' else
                {'named_imv': 1, 'positional_imv': 1, 'batch_yield': 2})
    assert transformer.counts == expected, transformer.counts
    ast.fix_missing_locations(tree)
    namespace = dict(vars(module))
    namespace.update(_receipt_bind=probe.bind_value, _receipt_driver=probe.driver_row,
                     _receipt_named_imv=probe.named_imv_value,
                     _receipt_positional_rows=probe.positional_imv_rows,
                     _receipt_batch=probe.batch_ready)
    code = compile(tree, '<native-receipt-probes:' + kind + '>', 'exec',
                   flags=__future__.annotations.compiler_flag)
    exec(code, namespace)
    return namespace[function.__name__]


@contextmanager
def installed_probes(monkeypatch, lineage):
    # The owning lineage fixture already checked the exact installed source
    # hashes and version before any test-scoped patch is installed.
    probe = SlotProbe(lineage)
    context_function = default.DefaultExecutionContext._init_compiled.__func__
    imv_function = compiler.SQLCompiler._deliver_insertmanyvalues_batches
    context_copy = instrument_copy(context_function, default, 'context', probe)
    imv_copy = instrument_copy(imv_function, compiler, 'imv', probe)
    with monkeypatch.context() as patch:
        patch.setattr(default.DefaultExecutionContext, '_init_compiled', classmethod(context_copy))
        patch.setattr(compiler.SQLCompiler, '_deliver_insertmanyvalues_batches', imv_copy)
        try:
            yield probe
        finally:
            probe.pending = None
            probe.bind_slots.clear()
            probe.imv_slots.clear()
