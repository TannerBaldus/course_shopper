__author__ = 'tanner'


def update_simple_fields(model_instance, field_names, **kwargs):
    """

    :param model_instance:
    :param field_names:
    :param kwargs:
    :return:
    """
    count = 0
    for attr_name in field_names:
        attribute = getattr(model_instance, attr_name)
        new_attr = kwargs[attr_name]
        if new_attr != attribute:
            setattr(model_instance, attr_name, new_attr)
            count += 1
    return count

def _get_pk_fields(model, pk_fields):
    """
    Using getattr gets all of the values of the pk

    :param model:
    :param pk_fields: a list of pk_fields
    :return:
    """
    return [getattr(model,pk_field) for pk_field in pk_fields]


def _filter_models_by_pk(models, pk_fields, good_pk_values_lst):
    """

    :param models:
    :param pk_field:
    :param pk_value_lst:
    :return:
    """

    bad_pk_values = []
    bad_models = []
    for model in models:
        pk_values = _get_pk_fields(model, pk_fields)
        if pk_values not in good_pk_values_lst:
            bad_pk_values.append(pk_values)
            bad_models.append(model)

    return bad_pk_values, bad_models




def _get_new_old(current_models, model_cls, pk_fields, new_model_kwargs_lst):
    """
      Takes a list of kwargs defining the value of fields of the new models to add to relation.
      Goes through the m2m field and finds the old models that needs to be removed.



    :param model_cls: the class of the model that the many to many is relation uses.
    :param pk_field: the field_names that is the primary key can be just one or a list of field_names
    :param new_model_kwargs_lst: a list of dicts mapping model_class fieldnames to values
    :return: the number of relationships changed
    """

    if not isinstance(pk_fields, list):
        pk_fields = [pk_fields]

    get_pk_fields_dict = lambda in_dict: [in_dict.get(field) for field in pk_fields]
    new_pk_values = [get_pk_fields_dict(i) for i in new_model_kwargs_lst]
    to_be_removed_pk_values, to_be_removed_models = _filter_models_by_pk(current_models, pk_fields, new_pk_values)

    # keep the good models already in the relation
    current_good_pks = [_get_pk_fields(i, pk_fields) for i in current_models  if i not in to_be_removed_pk_values]
    updated_models = []

    for model_dict in new_model_kwargs_lst:
        if get_pk_fields_dict(model_dict) not in current_good_pks:
            new_model = model_cls.objects.get_or_create(**model_dict)[0]
            updated_models.append(new_model)

    return updated_models, to_be_removed_models


def update_m2m(m2m_field, model_cls, pk_field, model_kwargs_list):
    """

    :param m2m_field:
    :param model_cls:
    :param pk_field:
    :param model_kwargs_list:
    :return: number of relationships changed
    """

    if not model_kwargs_list:
        relations_count = len(m2m_field.all())
        if relations_count == 0:
            return 0
        else:
            m2m_field.clear()
            return relations_count

    new_models, old_models = _get_new_old(m2m_field.all(), model_cls,pk_field, model_kwargs_list)

    if not new_models and not old_models:
        return 0

    m2m_field.remove(*old_models)
    m2m_field.add(*new_models)

    return len(new_models)+len(old_models)



def add_kwargs_to_m2m(m2m_field, get_or_create_fn, kwargs_list):
    """

    """
    if not kwargs_list:
        return 0
    for count, kwargs in enumerate(kwargs_list):
        m2m_field.add(get_or_create_fn(**kwargs)[0])
    return count
