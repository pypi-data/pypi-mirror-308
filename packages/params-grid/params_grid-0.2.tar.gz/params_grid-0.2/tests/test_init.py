from params_grid import ParamGrid, SearchSpace


def test_ok():
    ParamGrid(
        name="sklearn.tree.ExtraTreeClassifier",
        search_spaces=[
            SearchSpace(name="criterion", space=dict(choices=["gini", "entropy"])),
            SearchSpace(name="splitter", space=dict(choices=["random", "best"])),
            SearchSpace(name="max_depth", space=dict(low=1, high=3, log=False, step=2)),
            SearchSpace(name="max_features", space=dict(low=0.1, high=1.0, log=True, step=None)),
        ]
    )
