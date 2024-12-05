import pickle
import pandas as pd
import os
from .tracetype import *

# import numpy as np
# import time


class Pipeline:
    # take position and return module

    def __init__(self, *argv):
        self._modulelist = []
        for arg in argv:
            if isinstance(arg, list):
                for x in arg:
                    self += x
            else:
                self += arg

    def _add(self, module):
        return self._append(module)

    def _append(self, module):
        # print(type(module))
        # print(isinstance(module, Pipeline))
        if isinstance(module, ModuleParent):  # TODO: work with reloading
            self._modulelist.append(module)
        elif isinstance(module, Pipeline):  # TODO: work with reloading
            self._modulelist.append(PipelineModule(module))
        else:
            assert callable(
                module
            ), "added module must be callable, try restarting kernel"
            self._modulelist.append(CodeTaskFunctionModule(module))
        return self

    def _prepend(self, module):
        # print(type(module))
        # print(isinstance(module, Pipeline))
        if isinstance(module, ModuleParent):  # TODO: work with reloading
            self._modulelist.insert(0, module)
        elif isinstance(module, Pipeline):  # TODO: work with reloading
            self._modulelist.insert(0, PipelineModule(module))
        else:
            assert callable(
                module
            ), "added module must be callable, try restarting kernel"
            self._modulelist.insert(0, CodeTaskFunctionModule(module))
        return self

    def __iadd__(self, module):
        return self._append(module)

    def _simplify(self):
        idx = 0
        seq = []
        while idx < len(self._modulelist):
            module = self._modulelist[idx]
            if isinstance(module, CodeTaskFunctionModule):
                if len(seq) > 0:
                    seq.append(module)
                    self._modulelist.pop(idx)
                    idx -= 1
                elif idx < len(self._modulelist) - 1:
                    if isinstance(self._modulelist[idx + 1], CodeTaskFunctionModule):
                        seq.append(module)
                        self._modulelist.pop(idx)
                        idx -= 1
            elif len(seq) > 0:
                self._modulelist.insert(idx, PayloadSequenceModule(seq))
                seq = []
            if isinstance(module, PipelineModule):
                module.pipeline._simplify()
            idx += 1
        if len(seq) > 0:
            self._modulelist.append(PayloadSequenceModule(seq))
            seq = []

    def _get_module_by_index(self, index):
        try:
            return self._modulelist[index]
        except BaseException:
            return None

    def __getattr__(self, name):
        return VariablePlaceholder(name)

    def __getitem__(self, key):
        assert callable(key), "must specify a callable object"
        return PipelineFunctionHelper(self, key)

    def __setattr__(self, key, value):
        if key == "_modulelist":
            super().__setattr__(key, value)
        elif isinstance(value, PipelineFunctionHelper):
            value.write_to(key)
        elif isinstance(value, VariablePlaceholder):
            self._modulelist.append(BasicCopyModule(key, value.varname))
        else:
            self._modulelist.append(BasicAssignmentModule(key, value))


class VariablePlaceholder:
    def __init__(self, varname):
        self.varname = varname


class ModuleParent:
    def __init__(self):
        pass

    def __add__(self, other):
        pl = Pipeline()
        pl += self
        pl += other
        return pl


class CodeTaskFunctionModule(ModuleParent):
    # return code taskfunction
    def __init__(self, bodyfunc):
        self.bodyfunc = bodyfunc

    def get_task_function(self):
        def payload(variables):
            env = EnvironmentHelper(variables)
            self.bodyfunc(env)
            return env.__dictionary__

        return payload


class EnvironmentHelper:
    def __init__(self, dictionary):
        self.__dictionary__ = dictionary

    def __getattr__(self, key):
        return self.__dictionary__[key]

    def __setattr__(self, key, value):
        if key == "__dictionary__":
            super().__setattr__(key, value)
        else:
            self.__dictionary__[key] = value

    def copy(self):
        return EnvironmentHelper(self.__dictionary__.copy())


class BasicAssignmentModule(CodeTaskFunctionModule):
    def __init__(self, varname, value):
        self.varname = varname
        self.value = value

    def get_task_function(self):
        def payload(variables):
            variables = variables.copy()
            variables[self.varname] = self.value
            return variables

        return payload


class BasicCopyModule(CodeTaskFunctionModule):
    def __init__(self, destvar, srcvar):
        self.destvar = destvar
        self.srcvar = srcvar

    def get_task_function(self):
        def payload(variables):
            variables = variables.copy()
            variables[self.destvar] = variables[self.srcvar]
            return variables

        return payload


class FunctionModule(CodeTaskFunctionModule):
    def __init__(self, bodyfunc):
        self.bodyfunc = bodyfunc
        self.arrayargs = []
        self.dictargs = {}
        self.outputvarmap = {}

    def set_array_args(self, array):
        self.arrayargs = array

    def set_dict_args(self, dictionary):
        self.dictargs = dictionary

    def add_output_var(self, varname, idxpath):
        self.outputvarmap[varname] = idxpath

    def get_task_function(self):
        def payload(variables):
            array = [
                variables[arg.varname] if isinstance(arg, VariablePlaceholder) else arg
                for arg in self.arrayargs
            ]
            dictionary = {
                key: (
                    variables[val.varname]
                    if isinstance(val, VariablePlaceholder)
                    else val
                )
                for key, val in self.dictargs.items()
            }

            result = self.bodyfunc(*array, **dictionary)
            variables = variables.copy()

            for varname, idxpath in self.outputvarmap.items():
                value = result
                for idx in idxpath:
                    value = value[idx]
                variables[varname] = value

            return variables

        return payload


class PayloadSequenceModule(CodeTaskFunctionModule):
    def __init__(self, modseq):
        self.payloadseq = []
        for mod in modseq:
            self.payloadseq.append(mod.get_task_function())

    def get_task_function(self):
        def payload(variables):
            variables = variables.copy()
            for func in self.payloadseq:
                variables = func(variables)
            return variables

        return payload


def expand_tuple_shape(tup):
    if isinstance(tup, int):
        if tup == 1:
            return 0
        return [0] * tup
    if len(tup) == 1:
        return expand_tuple_shape(tup[0])
    return [expand_tuple_shape(x) for x in tup]


class PipelineFunctionHelper:
    def __init__(
        self,
        pipeline,
        appliedfunction,
        arrayargs=None,
        dictargs=None,
        module=None,
        shapearray=[],
        idxpath=[],
    ):
        self.pipeline = pipeline
        self.appliedfunction = appliedfunction
        self.arrayargs = arrayargs
        self.dictargs = dictargs
        self.module = module
        self.shapearray = shapearray
        self.idxpath = idxpath

    def __call__(self, *array, **dictionary):
        assert (
            self.arrayargs is None and self.dictargs is None
        ), "function arguments specified more than once"
        # print(array)
        # print(dictionary)
        self.arrayargs = array
        self.dictargs = dictionary

        self.module = FunctionModule(self.appliedfunction)
        self.module.set_array_args(self.arrayargs)
        self.module.set_dict_args(self.dictargs)

        self.pipeline._add(self.module)

        return self

    def __getitem__(self, key):
        assert (
            self.arrayargs is not None and self.dictargs is not None
        ), "function arguments not specified"

        valid = True
        try:
            self.shapearray[key]
        except BaseException:
            valid = False
        if not valid:
            raise IndexError("incorrect shape for function result")

        newshapearray = self.shapearray[key]
        newidxpath = self.idxpath.copy()
        newidxpath.append(key)

        return PipelineFunctionHelper(
            self.pipeline,
            self.appliedfunction,
            self.arrayargs,
            self.dictargs,
            self.module,
            newshapearray,
            newidxpath,
        )

    def shape(self, *args):
        # print(args)
        self.shapearray = expand_tuple_shape(args)
        # print(self.shapearray)
        return self

    def write_to(self, varname):
        self.module.add_output_var(varname, self.idxpath)


class PipelineModule(ModuleParent):
    def __init__(self, pipeline):
        self.pipeline = pipeline
        print(self.pipeline.par)

    def get_pipeline(self):
        return self.pipeline


# class ParallelModule(ModuleParent):
#
#    def __init__(self):
#        pass
#
#    def getControlPipeline(self):
#        return ...


class ThreadManager:
    # ID number
    # location
    # variable mapping
    # other state

    def __init__(self, ID, variables={}):
        self.ID = ID
        self.location = 0
        self.variables = variables
        self.writtentofile = False

    def run(self, pipeline, taskfunctionresult=None, childresults=None):

        if taskfunctionresult is not None:
            self.variables = taskfunctionresult
            self.location += 1

        if childresults is not None:
            module = pipeline._get_module_by_index(self.location)
            if isinstance(module, PipelineModule):
                self.variables = childresults[0]
                self.location += 1

        module = pipeline._get_module_by_index(self.location)

        if module is None:
            return {
                "status": "finished",
            }

        if isinstance(module, CodeTaskFunctionModule):
            return {
                "status": "waitingfortaskfunction",
                "taskfunction": module.get_task_function(),
                "configuration": self.variables,
            }

        if isinstance(module, PipelineModule):
            return {
                "status": "waitingforchildren",
                "pipelines": [module.get_pipeline()],
                "configurations": [self.variables],
            }


class ExecutionManager:
    # mapping from ThreadManager ID to pipeline

    import_pool = None
    import_ray = None
    worker = None

    def __init__(
        self, use=None, cores=1, address="auto", _redis_password=None, runtime_env=None
    ):
        if use is not None:
            use = use.lower()
            if use == "none":
                use = None
        assert use is None or use == "pathos" or use == "ray"
        self.use = use

        self.idtothreadmanager = {}
        self.HIDcounter = 0
        self.idtopipeline = {}
        self.idtostatus = {}
        self.idtowaiting = {}

        self.QIDcounter = 0
        self.qidqueue = []
        self.funcqueue = []
        self.envqueue = []

        self.taskfunctionresults = {}

        self.rootidstatus = []
        self.partialresults = []

        assert cores > 0 and isinstance(cores, int), "cores must be > 0"
        self.maxchildren = cores
        self.workerrefs = {}

        self.mp_initialized = False

        if use == "pathos":
            if ExecutionManager.import_pool is None:
                from pathos.multiprocessing import Pool

                ExecutionManager.import_pool = Pool
                self.mp_initialized = True

        if use == "ray":
            if ExecutionManager.import_ray is None:
                import ray

                if not ray.is_initialized():
                    # cwd = os.getcwd()
                    # cwd = os.path.dirname(cwd)
                    # py_module_list = [
                    #     cwd+"/common",
                    #     cwd+"/nchoice",
                    #     cwd+"/stopsignal",
                    #     cwd+"/notebooks",
                    #     cwd+"/sr",
                    # ]
                    # ray.init(address='auto', _redis_password='cbgt2', include_dashboard=False, runtime_env={"py_modules":py_module_list})
                    ray.init(
                        address=address,
                        _redis_password=_redis_password,
                        include_dashboard=False,
                        runtime_env=runtime_env,
                    )

                assert ray.is_initialized(), "ray not initialized"

                @ray.remote
                def workerFunc(module, configuration):
                    return module(configuration)

                ExecutionManager.import_ray = ray
                ExecutionManager.worker = workerFunc

    def spawn_thread_manager(self, pipeline, configuration):
        newid = self.HIDcounter
        self.HIDcounter += 1
        threadmanager = ThreadManager(newid, configuration)
        self.idtothreadmanager[newid] = threadmanager
        self.idtopipeline[newid] = pipeline
        self.idtostatus[newid] = "new"
        return newid

    def spawn_thread_managers(self, pipelines, configurations):
        newids = []
        for p, e in zip(pipelines, configurations):
            newids.append(self.spawn_thread_manager(p, e))
            print("spawn_thread_managers", p)

        return newids

    def cycle_through(self):
        items = list(self.idtothreadmanager.keys())
        for HID in items:

            if HID not in self.idtothreadmanager.keys():
                continue

            if self.idtostatus[HID] == "new":
                request = self.idtothreadmanager[HID].run(self.idtopipeline[HID])
                self.process_thread_manager_request(HID, request)

            if self.idtostatus[HID] == "waitingfortaskfunction":
                if self.idtowaiting[HID] in self.taskfunctionresults.keys():
                    taskfunctionresult = self.taskfunctionresults[self.idtowaiting[HID]]
                    request = self.idtothreadmanager[HID].run(
                        self.idtopipeline[HID], taskfunctionresult=taskfunctionresult
                    )
                    self.taskfunctionresults.pop(self.idtowaiting[HID], None)
                    self.idtowaiting.pop(HID, None)
                    self.process_thread_manager_request(HID, request)

            if self.idtostatus[HID] == "waitingforchildren":
                childresults = []
                for childid in self.idtowaiting[HID]:
                    if self.idtostatus[childid] != "finished":
                        break
                    childresults.append(self.idtothreadmanager[childid].variables)
                else:  # LOL
                    request = self.idtothreadmanager[HID].run(
                        self.idtopipeline[HID], childresults=childresults
                    )
                    for childid in self.idtowaiting[HID]:
                        self.idtothreadmanager.pop(childid, None)
                        self.idtopipeline.pop(childid, None)
                        self.idtostatus.pop(childid, None)
                        self.idtowaiting.pop(childid, None)
                    self.idtowaiting.pop(HID, None)
                    self.process_thread_manager_request(HID, request)

    def process_thread_manager_request(self, HID, request):
        self.idtostatus[HID] = request["status"]
        if request["status"] == "finished":
            pass
        if request["status"] == "waitingfortaskfunction":
            qid = self.add_to_queue(request["taskfunction"], request["configuration"])
            self.idtowaiting[HID] = qid
        if request["status"] == "waitingforchildren":
            hids = self.spawn_thread_managers(
                request["pipelines"], request["configurations"]
            )
            self.idtowaiting[HID] = hids

    def add_to_queue(self, taskfunction, variables):
        newid = self.QIDcounter
        self.QIDcounter += 1
        self.qidqueue.append(newid)
        self.funcqueue.append(taskfunction)
        self.envqueue.append(variables)
        return newid

    def consume_queue_one(self):

        if self.use is None:
            taskfunctionresult = self.funcqueue[0](self.envqueue[0])
            qid = self.qidqueue[0]

        elif self.use == "pathos":
            for i in range(
                len(self.workerrefs), min(self.maxchildren, len(self.qidqueue))
            ):
                wid = self.pool.apply_async(self.funcqueue[i], (self.envqueue[i],))
                # wid = worker.remote(self.funcqueue[i], self.envqueue[i])
                self.workerrefs[wid] = self.qidqueue[i]

            readywid = None
            while readywid is None:
                for wid in list(self.workerrefs.keys()):
                    if wid.ready():
                        readywid = wid
                        break

            taskfunctionresult = readywid.get()
            qid = self.workerrefs.pop(readywid)

        elif self.use == "ray":
            for i in range(
                len(self.workerrefs), min(self.maxchildren, len(self.qidqueue))
            ):
                wid = ExecutionManager.worker.remote(
                    self.funcqueue[i], self.envqueue[i]
                )
                #             print("spawning workers")
                #             print("worker id",wid)
                #             print("queue ids",self.qidqueue[i],self.funcqueue[i], "thread_id:"+str(self.envqueue[i]['thread_id'])+",")
                self.workerrefs[wid] = self.qidqueue[i]

            #         print(self.workerrefs.keys())
            ready_ids, _remaining_ids = ExecutionManager.import_ray.wait(
                list(self.workerrefs.keys()), num_returns=1
            )
            # print(ready_ids)
            taskfunctionresult = ExecutionManager.import_ray.get(ready_ids[0])
            qid = self.workerrefs.pop(ready_ids[0])

        self.taskfunctionresults[qid] = taskfunctionresult
        index = self.qidqueue.index(qid)
        self.qidqueue.pop(index)
        self.funcqueue.pop(index)
        self.envqueue.pop(index)

    def consume_queue(self):
        if len(self.qidqueue) == 0:
            return

        self.consume_queue_one()

        # while len(self.qidqueue) >= self.maxchildren:
        #     self.consume_queue_one()

    def run(
        self,
        pipelines,
        configurations={},
        simplify=True,
        savepath=None,
        gen_config_id=False,
    ):

        listform = True
        if not isinstance(pipelines, list) and not isinstance(configurations, list):
            listform = False
        if not isinstance(pipelines, list):
            pipelines = [pipelines]
        if not isinstance(configurations, list):
            configurations = [configurations]

        if len(pipelines) == 1:
            pipelines = pipelines * len(configurations)
        if len(configurations) == 1:
            configurations = configurations * len(pipelines)

        configurations = [config.copy() for config in configurations]

        if gen_config_id:
            for i, configuration in enumerate(configurations):
                configuration["config_id"] = i

        if simplify:
            for pipeline in pipelines:
                pipeline._simplify()

        rootids = []

        if self.use is None:  # run single-threaded batches in sequence
            for i in range(len(pipelines)):
                rootids.append(self.spawn_thread_manager(pipelines[i], configurations[i]))
                self.cycle_through()
                self.display_status_update(rootids)
                self.save_and_clear(rootids, savepath)
                while not self.all_finished(rootids):
                    self.consume_queue()
                    self.cycle_through()
                    self.display_status_update(rootids)
                    self.save_and_clear(rootids, savepath)
        else:
            for i in range(len(pipelines)):
                rootids.append(self.spawn_thread_manager(pipelines[i], configurations[i]))

            if self.use == "pathos":
                self.pool = ExecutionManager.import_pool(processes=self.maxchildren)

            self.cycle_through()
            self.display_status_update(rootids)
            self.save_and_clear(rootids, savepath)
            while not self.all_finished(rootids):
                self.consume_queue()
                self.cycle_through()
                self.display_status_update(rootids)
                self.save_and_clear(rootids, savepath)

            if self.use == "pathos":
                self.pool.close()

        results = [self.idtothreadmanager[rootid].variables for rootid in rootids]
        if listform:
            return results
        else:
            return results[0]

    def all_finished(self, rootids):
        for rootid in rootids:
            if self.idtostatus[rootid] != "finished":
                return False
        return True

    def display_status_update(self, rootids):
        newstatus = [self.idtostatus[rootid] for rootid in rootids]
        if newstatus != self.rootidstatus:
            self.rootidstatus = newstatus
            statuscounts = {}
            for item in newstatus:
                if item in statuscounts:
                    statuscounts[item] += 1
                else:
                    statuscounts[item] = 1
            print("thread status: ", statuscounts)
            self.partialresults = [
                self.idtothreadmanager[rootid].variables
                for rootid in rootids
                if self.idtostatus[rootid] == "finished"
            ]

    def save_and_clear(self, rootids, savepath):
        if savepath is None:
            return
        for rootid in rootids:
            if self.idtostatus[rootid] == "finished":
                threadm = self.idtothreadmanager[rootid]
                if threadm.writtentofile == False:
                    if not os.path.exists(savepath):
                        os.makedirs(savepath)
                    resultsavepath = (
                        savepath + "/" + str(threadm.variables["config_id"]) + ".pkl"
                    )
                    save_results_smart([threadm.variables], resultsavepath)
                    threadm.variables.clear()
                    threadm.writtentofile = True


def save_results(results, prefix, varnames):

    saveddatas = []

    for result in results:
        saveddata = {}
        for varname in varnames:
            saveddata[varname] = result[varname]
        saveddatas.append(saveddata)

    pickle.dump(saveddatas, open(prefix, "wb"))


def save_results_smart(results, savepath):
    savingresults = []
    for resultsdict in results:
        filtereddict = {}
        for key in resultsdict:
            try:
                pickle.dump(resultsdict[key], open("pickletest.pkl", "wb"))
                filtereddict[key] = resultsdict[key]
            except:
                try:
                    pickle.dump(untrace(resultsdict[key]), open("pickletest.pkl", "wb"))
                    filtereddict[key] = untrace(resultsdict[key])
                except:
                    print("unable to pickle: ", key)
        savingresults.append(filtereddict)
    pickle.dump(savingresults, open(savepath, "wb"))


def load_results(prefix):
    return pickle.load(open(prefix, "rb"))


def comparison_table(results, varnames):

    if not isinstance(results, list):
        results = [results]

    table = pd.DataFrame([], columns=varnames)

    for result in results:
        row = pd.DataFrame(
            [[result[varname] for varname in varnames]], columns=varnames
        )
        table = pd.concat([table, row], ignore_index=True)
    return table


def collate_variable(results, varname):
    if not isinstance(results, list):
        results = [results]
    return [result[varname] for result in results]


def concat_lists(lists):
    return [x for sublist in lists for x in sublist]
