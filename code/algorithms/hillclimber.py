from classes.model import Model

def hillClimber(model, env, iteraties):
    curModel = model
    batteries = curModel.modelBatteries

    # create list of costs
    # do random
    # get randommodel.cost
    # create model (copy of random model)
    # for iterations
    #   do function(model)
    #       switch two houses in model
    #       calculate costs
    #       compare model.cost to random.cost
    #       return the cheapest
    #       append cheapest to list
    #   if cheapest < random.cost
    #       model = cheapest model