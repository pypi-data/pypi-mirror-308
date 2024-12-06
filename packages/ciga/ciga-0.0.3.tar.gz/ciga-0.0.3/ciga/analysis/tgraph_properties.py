import pandas as pd
from typing import Callable, Dict, Any, List, Optional
from ..ciga import TGraph
from .graph_properties import graph_density, graph_transitivity_undirected
from tqdm import tqdm
import igraph as ig


def sequential_analysis(
        tg: TGraph,
        analysis_func: Callable[..., Any],
        *,
        start: Optional[int] = None,
        end: Optional[int] = None,
        w_normalized: bool = False,
        property_name: str = None,
        **analysis_kwargs
) -> pd.DataFrame:
    """
    Perform analysis on a time-varying graph sequentially.
    :param w_normalized:
    :param tg:
    :param analysis_func:
    :param start:
    :param end:
    :param analysis_kwargs:
    :return:
    """
    results = pd.DataFrame()
    # add position columns to results
    for col in tg._position:
        results[col] = []
    results[property_name] = []

    # get time steps
    time_steps = tg.data.index.unique().tolist()
    if start:
        time_steps = [step for step in time_steps if step >= start]
    if end:
        time_steps = [step for step in time_steps if step <= end]

    for step in tqdm(time_steps, desc='Processing time steps', unit='step'):
        graph = tg.get_graph(step, normalized=w_normalized)
        measure = {
            property_name: analysis_func(graph, **analysis_kwargs)
        }
        for col, val in zip(tg._position, step):
            measure[col] = val
        results = pd.concat([results, measure], axis=0).reset_index(drop=True)

    return results


def tgraph_density(tgraph: TGraph, *,
                   start: Optional[int] = None,
                   end: Optional[int] = None,
                   loops=False) -> pd.DataFrame:
    return sequential_analysis(tgraph, analysis_func=graph_density, start=start, end=end, w_normalized=False,
                               loops=loops, property_name="density")


def tgraph_transitivity_undirected(tgraph: TGraph, *,
                        start: Optional[int] = None,
                        end: Optional[int] = None,
                        mode='nan'
                        ) -> pd.DataFrame:
    if tgraph.is_directed():
        raise Warning("The graphs are directed. They will be converted to undirected.")
    return sequential_analysis(tgraph, analysis_func=graph_transitivity_undirected, start=start, end=end,
                               mode=mode, property_name="transitivity")