__author__ = 'tanner'

from model_mommy import mommy
import unittest
import course_search.db_common_ops as db_common_ops
import course_search.models as models
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "better_courses.settings")

class DB_Common_Ops_Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.gen_eds = mommy.make('gened', _quantity=2)
        cls.course_no_geneds = mommy.make('course')
        cls.course_gen_eds = mommy.make('course')

        cls.gen_ed_kwargs = [dict(code='>3', gen_ed='science'), dict(code='AC', gen_ed='american culture')]
        cls.gen_ed_objs =  [mommy.make('gened',**i) for i in cls.gen_ed_kwargs]
        cls.course_gen_eds.geneds.add(*cls.gen_eds[2:])


    def test_new_old_no_cur_relations(self):
        new_models, old_models = db_common_ops._get_new_old(self.course_no_geneds.geneds, models.GenEd, 'code',
                                                            self.gen_ed_kwargs)

        self.assertEqual([], old_models)
        self.assertItemsEqual(self.gen_ed_objs, new_models)









