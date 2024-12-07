import re

from collections import defaultdict
from copy import deepcopy
from itertools import chain


def get_units(
    ent_type, doc, doc_id=None, enrich_container=[], relation_layer="Scholarly", annotator=None
):
    doc = deepcopy(doc)
    lines = generate_line_annos(doc["text"])
    doc["annotations"]["Line"] = lines
    units = list(get_ents(ent_type, doc["text"], doc["annotations"], doc_id, annotator))
    for unit in units:
        # reformat begin and end
        unit["begin"] = unit["begin_in_doc"]
        unit["end"] = unit["end_in_doc"]
        del unit["begin_in_doc"]
        del unit["end_in_doc"]
        container_dict = {}
        for container in unit["container"]:
            if container["type"] in enrich_container:
                begin = container["begin_in_doc"]
                end = container["end_in_doc"]
                container["text"] = doc["text"][begin:end]
            if container["type"] in container:
                raise Exception("More than one container of one type")
            container_dict[container["type"]] = container
        unit["container"] = container_dict
    add_relations(units, doc.get("relations", {}).get(relation_layer))
    return units


def add_relations(units, relations):
    if not relations:
        return
    # match with annotations of units
    source_ent_relations = defaultdict(list)
    target_ent_relations = defaultdict(list)
    for relation_idx, relation in enumerate(relations):
        relation["idx"] = relation_idx
        source_ent_relations[relation["source_id"]].append(relation_idx)
        target_ent_relations[relation["target_id"]].append(relation_idx)

    for unit in units:
        ent_ids = {a.get("ref_id") for a in unit["annotations"] if "ref_id" in a}

        relations_idxs_source = set(
            chain(*[source_ent_relations[e_id] for e_id in ent_ids])
        )
        relations_idxs_target = set(
            chain(*[target_ent_relations[e_id] for e_id in ent_ids])
        )
        relations_idxs_inner = relations_idxs_source & relations_idxs_target
        units_relations = [
            deepcopy(relations[i])
            for i in list(relations_idxs_source | relations_idxs_target)
        ]
        for rel in units_relations:
            rel["source_in_unit"] = rel["idx"] in relations_idxs_source
            rel["target_in_unit"] = rel["idx"] in relations_idxs_target
            rel["inner"] = rel["idx"] in relations_idxs_inner
        unit["relations"] = units_relations
    # match with unit itself
    # @todo


def _get_ents(filter_span_type, text, annos, doc_id=None, annotator=None):
    # other_ents = [k for k in annos.keys() if k != ent_type]
    # save all spans of different span_type
    spans_other = []
    spans_to_select = []
    for span_type, spans in annos.items():
        if span_type == filter_span_type:
            spans_to_select.extend(spans)
        else:
            for span in spans:
                span = deepcopy(span)
                span["type"] = span_type
                spans_other.append(span)
    overlap_matcher = OverlappMatcher(spans_other)
    for span in spans_to_select:
        # find overlapps:
        overlapping_spans = overlap_matcher(span)
        span["overlapping"] = overlapping_spans


class OverlappMatcher:
    def __init__(self, spans):
        self.spans = spans
        self.spans_begin = sorted([(span["begin"], idx) for idx, span in enumerate(spans)])
        self.spans_end = sorted([(span["end"], idx) for idx, span in enumerate(spans)])

    def get_overlapping(self, span):
        # all annos with smaller end as begining of query anno
        anno_idx_end_max = bisect_right(self.spans_end, span["begin"], key=lambda x:x[0])
        # all annos with smaller beginning as ending of query anno
        anno_idx_begin_min = bisect_left(self.spans_begin, span["end"], key=lambda x:x[0])
        #anno_idx_begin_min, anno_idx_end_max
        matches = {a[1] for a in self.spans_end[anno_idx_end_max:]} &\
                  {a[1] for a in self.spans_begin[:anno_idx_begin_min]}
        for overlapping in matches:
            overlapping_type = self.get_label(span, overlapping)
            overlapping = deepcopy(overlapping)
            return matches
    def get_label(self, ent, ent_overlapping):
        pass

def get_ents(span_type, text, annos, doc_id=None, annotator=None):
    # other_ents = [k for k in annos.keys() if k != ent_type]
    # save all spans of different span_type
    other_spans = deepcopy({k: v[::-1] for k, v in annos.items() if k != span_type})
    for span in annos.get(span_type, []):
        # create new dict based on span info
        ent_info = deepcopy(span)  # {k: v for k, v in ent.items()}
        ent_info["type"] = span_type
        ent_info["text"] = text[span["begin"] : span["end"]]
        begin, end = span["begin"], span["end"]
        # find container, overlapping and sub spans
        found_ents = update_other_spans(other_spans, begin, end)
        found_ents = list(found_ents)
        container_ents = [
            e for e, ent_flag in found_ents if ent_flag == "container_span"
        ]
        # sort container by size (biggest (most general) first)
        container_ents.sort(key=lambda x: -x["end_in_doc"] + x["begin_in_doc"])
        ent_info["container"] = container_ents
        sub_ents = [e for e, ent_flag in found_ents if ent_flag == "sub_span"]
        ent_info["annotations"] = sub_ents
        overlapping_ents = [
            e for e, ent_flag in found_ents if ent_flag == "overlapping_span"
        ]
        if overlapping_ents:
            ent_info["annotations_overlap"] = overlapping_ents

        ent_info["begin_in_doc"] = ent_info["begin"]
        del ent_info["begin"]
        ent_info["end_in_doc"] = ent_info["end"]
        del ent_info["end"]
        if doc_id is not None:
            ent_info["doc_id"] = doc_id
        if annotator is not None:
            ent_info["annotator"] = annotator
        yield ent_info


def update_other_spans(left_other_spans, begin, end):
    """
    begin: int begin of base span
    end: int end of base span
    """
    # @todo: rename to update
    for span_type, spans in left_other_spans.items():
        while True:
            if not spans:
                break
            next_span = spans[-1]
            if next_span["end"] <= begin:
                # current span is before base span
                # base:     .....|---|...
                # current:  .|---|.......
                spans.pop()  # do not treat current span for other base spans anymore
                # look at next:
                continue
            elif next_span["begin"] >= end:
                # current span is after the base span: Maybe interesting for next base spans
                # base:     .....|---|......
                # current:  .........|---|..
                break
            elif next_span["begin"] <= begin and next_span["end"] >= end:
                # current span is container of base span
                # base:     .....|---|......
                # current:  ..|------|......
                # collect all infos interesting for the base span (incl. relative position)
                span_info = deepcopy(next_span)
                span_info["begin_in_doc"] = span_info["begin"]
                del span_info["begin"]
                span_info["end_in_doc"] = span_info["end"]
                del span_info["end"]
                span_info["offset_to_container"] = begin - span_info["begin_in_doc"]
                span_info["type"] = span_type
                yield span_info, "container_span"
                # only return one span by span_type
                break
            elif next_span["begin"] >= begin and next_span["end"] <= end:
                # span is sub span of base span
                # base:     ..|------|......
                # current:  ..|----|......
                next_span = spans.pop()  # Why pop?
                next_span["begin_in_doc"] = next_span["begin"]
                next_span["end_in_doc"] = next_span["end"]
                next_span["begin"] -= begin
                next_span["end"] -= begin
                next_span["type"] = span_type
                yield next_span, "sub_span"
            else:
                # no container and no subspan => span has an overlap!
                # ...|-----|......
                # .......|----|...
                # I think the next lines do not work
                #if end >= next_span["end"]:
                #    spans.pop()
                yield next_span, "overlapping_span"
                break


line_pattern = re.compile("[^\n]*[\n$]")


def generate_line_annos(text):
    lines = []
    for idx, line in enumerate(line_pattern.finditer(text)):
        if line.group().strip():
            lines.append(dict(begin=line.start(), end=line.end(), idx=idx))
    return lines
