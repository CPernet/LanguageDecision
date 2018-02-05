import hddm


def gen_model(csv_path, out_path=None, samples=8000, burn=20, *args, **kwargs):
    """
    Diffusion decision model generator
    """
    data = hddm.load_csv(str(csv_path))
    model = hddm.HDDM(data, *args, **kwargs)
    model.find_starting_values()
    if out_path:
        model.sample(samples, burn, dbname=out_path, db='sqlite')
    else:
        model.sample(samples, burn)
    return model


def gen_models(csv_path, out_path=None, num=5, samples=8000, burn=200, *args, **kwargs):
    """
    Generate lots of models
    """
    models = []
    for i in range(int(num)):
        models.append(gen_model(csv_path, out_path, samples, burn, *args, **kwargs))
    return models


def load_model(model_data, model_db, depends_on=None, bias=True, db_type='sqlite'):
    """
    Get model from database
    :param model_data: path to derivative data csv
    :param model_db: path to model database
    :param depends_on: model parameter dependencies (e.g v: stim)
    :return: loaded model
    """
    csv_data = hddm.load_csv(model_data)
    model = hddm.HDDM(csv_data, depends_on=depends_on, bias=bias)
    return model.load_db(dbname=model_db, db=db_type)


def check_convergence(models):
    gelman_rubin = hddm.analyze.gelman_rubin(models)

    for key, value in gelman_rubin.items():
        if (value > 1.02) or (value < 0.98):
            print("Convergence error at " + str(key))
            return False
    print("\nNo convergence problems detected!")
    return True
