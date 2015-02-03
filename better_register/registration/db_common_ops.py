__author__ = 'tanner'



def update_nonkey_fields(model_instance, field_names, **kwargs):
    count = 0
    for attr_name in field_names:
        attribute = getattr(model_instance,attr_name)
        new_attr = kwargs[attr_name]
        if new_attr != attribute:
            setattr(model_instance,attr_name, new_attr)
            count += 1
    return count


def update_m2m(m2m_field, model_class, pk_field, model_kwargs_list):
    """
      Takes a list of kwargs defining the value of fields and updates the, m2m _field to have relationships to models
      of type model_class with the fields.


    :param m2m_field:a many_to_many manager
    :param model_class: the class of the model that the many to many is relation uses.
    :param pk_field: the field_name that is the primary key
    :param model_kwargs_list: a list of dicts mapping model_class fieldnames to values
    :return: the number of relationships changed
    """
    old_models = {getattr(i, pk_field):i for i in m2m_field.all() if i.pk_field not in model_kwargs_list}

    if not model_kwargs_list and m2m_field.all():
        m2m_field.clear()
        return 1

    else:
        new_relations = 0
        updated_models = []

        for model_dict in model_kwargs_list:

            if model_dict.get(pk_field) not in old_models:
                new_model = model_class.objects.get_or_create(**model_dict)
                updated_models.append(new_model)
                new_relations += 1

        if new_relations > 0:
            m2m_field.remove(*old_models.values())
            m2m_field.add(*updated_models)

        return new_relations

