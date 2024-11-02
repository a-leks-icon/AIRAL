import re
from datetime import datetime
from inspect import stack
from corflow.Transcription import Transcription

def get_segs(trans:Transcription,tier_re:str,*conditions,**options) -> dict:
    r'''Collects segments based on a number of conditions.

    Returns for a given transcription **trans** a dictionary with tiers, matching the regular expression **tier_re**, as keys and lists of segments as values, which get collected based on a number of **\*conditions** they meet.

    Args:
        trans: Transcription object (e.g. created with corflow.fromElan.fromElan)
        tier_re: Regular expression used to identify tiers in a given transcription, whose segments get collected.
        \*conditions: A number of tuples and/or lists defining, which conditions segments have to fulfill to get collected. The general format for every condition is [tier_re,relation,seg_re,bool]. /**tier_re**/: Regular expression used to identify tiers, whose segments are referenced and used to check, whether a condition is met by a segment to get collected. /**relation**/*optional*: Name (string) of a specific relation a segment to get collected has to be in with a referenced segment. If no argument is given, the relation defaults to 'time-aligned'. Call corflow_functions.relations() to print all supported relations. /**seg_re**/*optional*: Regular expression used to identify referenced segments. If no argument is given, every segment regardless of its content is referenced./**bool**/*optional*: Boolean expression determining whether seg_re is positively or negatively applied. Defaults to 'True', if not argument is given.
        \*\*options: Further options to apply as keys. **mode**: Decides how to evaluate conditions. By default, evaluates conditions as conjunctions. If defined as 'or', evaluates conditions as disjunctions. **log**: Boolean expression: Either prints a log file in the same directory of this script or not. Its default values is 'True'

    Returns:
        Dictionary, whose keys are Tier objects and whose values are lists either containing Segment objects or nothing.
    '''

    def get_relation(relations,rel_str):
        '''Returns the first relation found given a string.'''
        tokenizer = r"[a-zA-Z]+-?[a-zA-Z]+|[a-zA-Z]+"
        tokens = re.findall(tokenizer,rel_str)
        if tokens:
            for rel in relations:
                if all(tok in rel for tok in tokens):
                    return rel
        return None
    
    def sort_segs(segs:set):
        '''Returns a list with sorted segments based on their indeces given a set of segments.'''
        ind_segs = [(seg.index(),seg) for seg in segs]
        ind_segs = sorted(ind_segs,key=lambda x: x[0])
        segs_sorted = [seg for ind,seg in ind_segs]
        return segs_sorted

    def set_options(options:dict):
        '''Handles further options for the overall function.'''
        option_keys = options.keys()
        if not "mode" in option_keys:
            options["mode"] = "and"
        if not "log" in option_keys:
            options["log"] = False
        return options

    def create_log(log_settings,get_tiers,ref_tiers):
        '''Create and return a dictionary for the log file.'''
        if log_settings:
            now = datetime.now()
            day = f"{now.year}-{now.month}-{now.day}"
            time = f"{now.hour}-{now.minute}-{now.second}-{now.microsecond}"
            file_name = f"get_segs_{day}_{time}.log"
            get_tier_names = [tier.name for tier in get_tiers]
            ref_tier_names = [tier.name for tier in ref_tiers]
            log = {
            "file_name":file_name,
            "script":f"{stack()[2].filename}",
            "day":day,
            "time":time,
            "ref_tiers":set(),
            "conditions":{}
            }
            log["text"] = f"Logfile: {file_name}\nFunction: 'get_segs'\nScript: {log['script']}\nDay: {day}\nTime: {time}\n\nCollecting segments from the following tiers:\n{get_tier_names}\n\nThe '{settings['mode']}' conditions, their relations and referenced tiers:\n"
            return log
        return None

    relations = [["time", "aligned"], ["time", "start"], ["time", "end"], ["time", "next", "adjacent"], ["time", "previous", "adjacent"], ["time", "next", "non-adjacent"], ["time", "previous", "non-adjacent"], ["sequence", "next", "adjacent"], ["sequence", "previous", "adjacent"], ["sequence", "next", "non-adjacent"], ["sequence", "previous", "non-adjacent"], ["direct", "child"], ["direct", "parent"], ["distant", "child"], ["distant", "parent"], ["overlap", "next"], ["overlap", "previous"], ["time within"], ["time around"]]

    settings = set_options(options)

    conds = [list(c) for c in conditions]
    for c in conds:
        c[0] = trans.findAllName(c[0])
    get_tiers = [tier for tier in trans.findAllName(tier_re)]

    log = create_log(settings["log"],get_tiers,c[0])

    get_tier_segs = {}
    for get_tier in get_tiers:
        get_tier_segs[get_tier] = []
        get_segs = [seg for seg in get_tier]
        c_collected_segs = {}
        for n,c in enumerate(conds):
            c_collected_segs[n] = {}
            if log != None:
                log["conditions"][n] = {"rel":"","tiers":[]}
            for i,ref_tier in enumerate(c[0]):
                relation = None
                if len(c) == 1:
                    ref_segs = [seg for seg in ref_tier]
                    relation = relations[0]
                elif len(c) == 2:
                    ref_segs = [seg for seg in ref_tier]
                    relation = get_relation(relations,c[1])
                    if relation == None:
                        relation = relations[0]
                        if isinstance(c[1],str):
                            ref_segs = [seg for seg in ref_tier if re.search(c[1],seg.content)]
                elif len(c) == 3:
                    ref_segs = [seg for seg in ref_tier]
                    relation = get_relation(relations,c[1])
                    if isinstance(c[2],str):
                        ref_segs = [seg for seg in ref_tier if re.search(c[2],seg.content)]
                    if relation == None:
                        relation = relations[0]
                        if (isinstance(c[1],str)) & (isinstance(c[2],bool)):
                            if c[2] == False:
                                ref_segs = [seg for seg in ref_tier if not re.search(c[1],seg.content)]
                            else:
                                ref_segs = [seg for seg in ref_tier if re.search(c[1],seg.content)]
                        else:
                            continue
                elif len(c) == 4:
                    if (isinstance(c[2],str)) & (isinstance(c[3],bool)):
                        if c[3] == False:
                            ref_segs = [seg for seg in ref_tier if not re.search(c[1],seg.content)]
                        else:
                            ref_segs = [seg for seg in ref_tier if re.search(c[1],seg.content)]
                        relation = get_relation(relations,c[1])
                        if relation == None:
                            relation = relations[0]

                if log != None:
                    log["conditions"][n]["rel"] = relation
                    log["conditions"][n]["tiers"].append(ref_tier.name)

                c_collected_segs[n][i] = []
                #time aligned
                if relation == relations[0]:
                    for get_seg in get_segs:
                        for ref_seg in ref_segs:
                            if (get_seg.start == ref_seg.start) & (get_seg.end == ref_seg.end):
                                c_collected_segs[n][i].append(get_seg)
                #time start
                elif relation == relations[1]:
                    for get_seg in get_segs:
                        for ref_seg in ref_segs:
                            if get_seg.start == ref_seg.start:
                                c_collected_segs[n][i].append(get_seg)
                #time end
                elif relation == relations[2]:
                    for get_seg in get_segs:
                        for ref_seg in ref_segs:
                            if get_seg.end == ref_seg.end:
                                c_collected_segs[n][i].append(get_seg)
                #time next adjacent
                elif relation == relations[3]:
                    for get_seg in get_segs:
                        for ref_seg in ref_segs:
                            if get_seg.start == ref_seg.end:
                                c_collected_segs[n][i].append(get_seg)
                #time previous adjacent
                elif relation == relations[4]:
                    for get_seg in get_segs:
                        for ref_seg in ref_segs:
                            if get_seg.end == ref_seg.start:
                                c_collected_segs[n][i].append(get_seg)
                #time next non-adjacent
                elif relation == relations[5]:
                    for get_seg in get_segs:
                        for ref_seg in ref_segs:
                            if get_seg.start > ref_seg.end:
                                c_collected_segs[n][i].append(get_seg)
                #time previous non-adjacent
                elif relation == relations[6]:
                    for get_seg in get_segs:
                        for ref_seg in ref_segs:
                            if get_seg.end < ref_seg.start:
                                c_collected_segs[n][i].append(get_seg)
                #sequence next adjacent
                elif relation == relations[7]:
                    for get_seg in get_segs:
                        get_seg_ind = get_seg.index()
                        for ref_seg in ref_segs:
                            if get_seg_ind == ref_seg.index()+1:
                                c_collected_segs[n][i].append(get_seg)
                #sequence previous adjacent
                elif relation == relations[8]:
                    for get_seg in get_segs:
                        get_seg_ind = get_seg.index()
                        for ref_seg in ref_segs:
                            if get_seg_ind == ref_seg.index()-1:
                                c_collected_segs[n][i].append(get_seg)
                #sequence next non-adjacent
                elif relation == relations[9]:
                    for get_seg in get_segs:
                        get_seg_ind = get_seg.index()
                        for ref_seg in ref_segs:
                            if get_seg_ind > ref_seg.index()+1:
                                c_collected_segs[n][i].append(get_seg)
                #sequence previous non-adjacent
                elif relation == relations[10]:
                    for get_seg in get_segs:
                        get_seg_ind = get_seg.index()
                        for ref_seg in ref_segs:
                            if get_seg_ind < ref_seg.index()-1:
                                c_collected_segs[n][i].append(get_seg)
                #direct child
                elif relation == relations[11]:
                    for get_seg in get_tier:
                        for ref_seg in ref_tier:
                            if ref_seg.children():
                                if get_seg in ref_seg.children():
                                    c_collected_segs[n][i].append(get_seg)
                #direct parent
                elif relation == relations[12]:
                    for get_seg in get_tier:
                        for ref_seg in ref_tier:
                            if get_seg == ref_seg.parent():
                                c_collected_segs[n][i].append(get_seg)
                #distant child
                elif relation == relations[13]:
                    for get_seg in get_tier:
                        for ref_seg in ref_tier:
                            all_ch_segs = ref_seg.allChildren()
                            if all_ch_segs:
                                dist_ch_segs = set(all_ch_segs) - set(ref_seg.children())
                                if get_seg in dist_ch_segs:
                                    c_collected_segs[n][i].append(get_seg)
                #distant parent
                elif relation == relations[14]:
                    for get_seg in get_tier:
                        for ref_seg in ref_tier:
                            par = ref_seg.parent()
                            pars = ref_seg.parents()
                            if par in pars:
                                ind = pars.index(par)
                                pars.pop(ind)
                            if get_seg in pars:
                                c_collected_segs[n][i].append(get_seg)
                #overlap next
                elif relation == relations[15]:
                    for get_seg in get_tier:
                        for ref_seg in ref_tier:
                            if (get_seg.end > ref_seg.start) & (get_seg.end < ref_seg.end):
                                c_collected_segs[n][i].append(get_seg)
                #overlap previous
                elif relation == relations[16]:
                    for get_seg in get_tier:
                        for ref_seg in ref_tier:
                            if (get_seg.start < ref_seg.end) & (get_seg.end > ref_seg.end):
                                c_collected_segs[n][i].append(get_seg)
                #within
                elif relation == relations[17]:
                    for get_seg in get_tier:
                        for ref_seg in ref_tier:
                            if (get_seg.start > ref_seg.start) & (get_seg.end < ref_seg.end):
                                c_collected_segs[n][i].append(get_seg)
                #around
                elif relation == relations[18]:
                    for get_seg in get_tier:
                        for ref_seg in ref_tier:
                            if (get_seg.start < ref_seg.start) & (get_seg.end > ref_seg.end):
                                c_collected_segs[n][i].append(get_seg)

                c_collected_segs[n][i] = set(c_collected_segs[n][i])

        get_segs_sets = []
        if c_collected_segs[0]:
            for r_dict in c_collected_segs.values():
                for r_set in r_dict.values():
                    get_segs_sets.append(r_set)

            s = c_collected_segs[0][0]
            if settings["mode"] != "or":
                collected_get_segs = s.intersection(*get_segs_sets)
            else:
                collected_get_segs = s.union(*get_segs_sets)
            sorted_get_segs = sort_segs(collected_get_segs)
            get_tier_segs[get_tier] = sorted_get_segs

    if log != None:
        for c in log["conditions"]:
            log["text"] += f"condition {c} with relation '{log['conditions'][c]['rel']}'.\nReferenced tiers:\n{log['conditions'][c]['tiers']}\n\n"
        log["text"] += f"Collected segments per tier. Segments are listed and returned in order of their index. Their i) content, ii) index and iii) start and end time get printed:\n\n"
        for tier,segs in get_tier_segs.items():
            log["text"] += f"{tier.name}:\n"
            for seg in segs:
                log["text"] += f"'{seg.content}' | {seg.index()} | {seg.start}-{seg.end}\n"
            log["text"] += "\n"
        with open("./"+log["file_name"],"w") as log_file:
            log_file.write(log["text"])

    return get_tier_segs