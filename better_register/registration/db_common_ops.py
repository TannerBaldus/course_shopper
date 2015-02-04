__author__ = 'tanner'


def update_simple_fields(model_instance, field_names, **kwargs):
    count = 0
    for attr_name in field_names:
        attribute = getattr(model_instance, attr_name)
        new_attr = kwargs[attr_name]
        if new_attr != attribute:
            setattr(model_instance, attr_name, new_attr)
            count += 1
    return count


def _filter_model_pk_mapping(models, pk_field, pk_value_lst):
    """

    :param models:
    :param pk_field:
    :param pk_value_lst:
    :param lst_good:
    :return:
    """
    pair_pk_model = lambda model, pk_field: (getattr(model ,pk_field), model)
    check_pk_field = lambda model, pk_field, lst: getattr(model,pk_field) not in lst

    return dict(pair_pk_model(m, pk_field) for m in models if check_pk_field(m, pk_field, pk_value_lst))


def _get_new_old(m2m_field, model_class, pk_field, model_kwargs_list):
    """
      Takes a list of kwargs defining the value of fields of the new models to add to relation.
      Goes through the m2m field and finds the old models that needs to be removed.


    :param m2m_field:a many_to_many manager
    :param model_class: the class of the model that the many to many is relation uses.
    :param pk_field: the field_name that is the primary key
    :param model_kwargs_list: a list of dicts mapping model_class fieldnames to values
    :return: the number of relationships changed
    """

    new_pk_values = [i.get(pk_field) for i in model_kwargs_list]
    all_models = m2m_field.all()
    to_be_removed = _filter_model_pk_mapping(all_models, pk_field, new_pk_values)

    # keep the good models already in the relation
    current_good_pks = [getattr(i, pk_field) for i in all_models if i not in to_be_removed.values()]
    updated_models = []

    for model_dict in model_kwargs_list:
        if model_dict.get(pk_field) not in current_good_pks:
            new_model = model_class.objects.get_or_create(**model_dict)
            updated_models.append(new_model)

    return updated_models, to_be_removed.values()


def update_m2m(m2m_field, model_class, pk_field, model_kwargs_list):
    """

    :param m2m_field:
    :param model_class:
    :param pk_field:
    :param model_kwargs_list:
    :return: number of relationships changed
    """

    new_models, old_models = _get_new_old(m2m_field, model_class,pk_field, model_kwargs_list)

    if not new_models and not old_models:
        return 0

    m2m_field.remove(*old_models)
    m2m_field.add(*new_models)

    return len(new_models)+len(old_models)


