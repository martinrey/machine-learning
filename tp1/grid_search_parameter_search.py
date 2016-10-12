def grid_search_params_for_decision_tree_classifier():
    grid_param = {"max_depth": [1, 3, 5, 10, 15, 50, 100], "min_samples_split": [1, 3, 5, 10, 15], }
    return grid_param


def grid_search_params_for_multinomial_nb():
    grid_param = {"alpha": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
    return grid_param


def grid_search_params_for_k_neighbors_classifier():
    grid_param = {"n_neighbors": [1, 3, 5, 7, 10, 15], "weights": ["uniform", "distance"]}
    return grid_param


def grid_search_params_for_svc():
    grid_param = {"kernel": ['linear'], "degree": [2, 3, 4], "probability": [True, False]}
    return grid_param


def grid_search_params_for_random_forest_classifier():
    grid_param = {"n_estimators": [2, 5, 10, 15, 40, 100], "max_features": [2, 5, 10, 20],
                  "max_depth": [3, 5, 20, None]}
    return grid_param
