import os
import unittest
from random import shuffle

from .rl_sheduler import Parser, Env, Schedule, Activity, Agent, RandomAgent
from .time import Time


class TestParser(unittest.TestCase):

    def setUp(self):
        self.wd = r'D:\DigitalAwayDay\python'
        self.data_file = os.path.join(self.wd, 'data.txt')
        self.p = Parser(self.data_file)
        self.activities = self.p.read_data_file()

    def test_1_entry(self):
        self.assertTrue(self.activities['Laser Clay Shooting'], 60)

    def test_correct_size(self):
        self.assertEqual(20, len(self.activities))


class TimeTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_instantiation(self):
        t = Time(9, 0, 0)
        self.assertIsInstance(t, Time)

    def test_000(self):
        t = Time(0, 0, 0)
        self.assertIsInstance(t, Time)

    def test_add(self):
        t1 = Time(9, 0, 0)
        t2 = Time(0, 45, 0)
        sum = t1 + t2
        expected = Time(9, 45, 0)
        self.assertEqual(expected, sum)

    def test_sub(self):
        t1 = Time(9, 0, 0)
        t2 = Time(0, 45, 0)
        diff = t1 - t2
        expected = Time(8, 15, 0)
        self.assertEqual(expected, diff)

    def test_sub2(self):
        t1 = Time(9, 0, 15)
        t2 = Time(9, 0, 14)
        diff = t1 - t2
        expected = Time(0, 0, 1)
        self.assertEqual(expected, diff)

    def test_sub3(self):
        t1 = Time(9, 0, 15)
        t2 = Time(0, 0, 24)
        diff = t1 - t2
        expected = Time(8, 59, 51)
        self.assertEqual(expected, diff)

    def test_normalise_time1(self):
        t1 = Time(9, 30, 65)
        expected = Time(9, 31, 5)
        self.assertEqual(expected, t1)

    def test_normalise_time2(self):
        t1 = Time(9, 63, 35)
        expected = Time(10, 3, 35)
        self.assertEqual(expected, t1)

    def test_normalise_time3(self):
        t1 = Time(9, 0, -5)
        expected = Time(8, 59, 55)
        self.assertTrue(expected, t1)

    def test_normalise_time4(self):
        t1 = Time(9, -6, 0)
        expected = Time(8, 54, 00)
        self.assertTrue(expected, t1)

    def test_gt(self):
        t1 = Time(9, 0, 0)
        t2 = Time(10, 0, 0)
        self.assertGreater(t2, t1)

    def test_gt2(self):
        t1 = Time(9, 0, 0)
        t2 = Time(9, 1, 0)
        self.assertGreater(t2, t1)

    def test_gt3(self):
        t1 = Time(9, 0, 0)
        t2 = Time(9, 0, 1)
        self.assertGreater(t2, t1)

    def test_gt4(self):
        t1 = Time(9, 45, 0)
        t2 = Time(12, 0, 0)
        self.assertGreater(t2, t1)

    def test_lt(self):
        t1 = Time(9, 0, 0)
        t2 = Time(9, 0, 1)
        self.assertLess(t1, t2)


class ActivityTests(unittest.TestCase):

    def setUp(self):
        self.a1 = Activity(name='Buggy Driving',
                           duration=Time(0, 30, 0),
                           start_time=Time(9, 0, 0))
        self.a2 = Activity(name='Viking Axe Throw',
                           duration=Time(1, 0, 0),
                           start_time=Time(10, 0, 0))

        self.a3 = Activity(name='lunch',
                           duration=Time(1, 0, 0),
                           start_time=Time(12, 0, 0))
        self.a4 = Activity(name='talk',
                           duration=Time(1, 0, 0),
                           start_time=Time(16, 0, 0))
        self.activities = [
            self.a3, self.a4, self.a2, self.a1
        ]

    def test_eq(self):
        self.assertTrue(self.a1 == self.a1)

    def test_ne(self):
        self.assertTrue(self.a1 != self.a2)
        self.assertFalse(self.a1 != self.a1)

    def test_lt(self):
        self.assertFalse(self.a1 > self.a2)

    def test_gt(self):
        self.assertTrue(self.a2 > self.a1)

    def test_sort(self):
        activities = sorted(self.activities)
        expected = 'talk'
        actual = sorted(self.activities)[-1].name
        self.assertEqual(expected, actual)

    def test_overlaps_with(self):
        a1 = Activity(name='Buggy Driving',
                      duration=Time(0, 30, 0),
                      start_time=Time(9, 0, 0))

        a2 = Activity(name='Cheese Grating',
                      duration=Time(0, 30, 0),
                      start_time=Time(9, 15, 0))

        self.assertTrue(a1.overlaps_with(a2))

    def test_overlaps_with2(self):
        a1 = Activity(
            'Archery',
            duration=Time(0, 45, 0),
            start_time=Time(9, 0, 0))
        a2 = Activity(
            'lunch',
            duration=Time(1, 0, 0),
            start_time=Time(12, 0, 0)
        )
        # print(a1, a2)
        print(a1.overlaps_with(a2))

    def test_overlaps_by(self):
        a1 = Activity(name='Buggy Driving',
                      duration=Time(0, 30, 0),
                      start_time=Time(9, 0, 0))

        a2 = Activity(name='Cheese Grating',
                      duration=Time(0, 30, 0),
                      start_time=Time(9, 15, 0))

        actual = a1.overlaps_by(a2)
        expected = Time(0, 15, 0)
        self.assertEqual(expected, actual)


class ScheduleTests(unittest.TestCase):

    def setUp(self):
        self.activities = [
            Activity(name='Buggy Driving',
                     duration=Time(0, 30, 0),
                     start_time=Time(9, 0, 0)),
            Activity(name='Viking Axe Throw',
                     duration=Time(1, 0, 0),
                     start_time=Time(10, 0, 0)),
            Activity(name='lunch',
                     duration=Time(1, 0, 0),
                     start_time=Time(12, 0, 0)),
            Activity(name='talk',
                     duration=Time(1, 0, 0),
                     start_time=Time(16, 0, 0)),
        ]
        self.activities

    def test_add_to_schedule(self):
        new_activity = Activity(
            name='Cheese gnawing',
            start_time=Time(13, 0, 0),
            duration=Time(0, 30, 0)
        )
        s = Schedule(self.activities)
        # print(sorted(self.activities))
        s = s.add_to_schedule(new_activity)
        activity = s.get_activity_by_name('Cheese gnawing')
        self.assertEqual(activity.name, 'Cheese gnawing')

    def test_iter(self):
        s = Schedule(self.activities)
        passed = False
        for i in s:
            i
        passed = True
        self.assertTrue(passed)

    def test_get_activity_by_time(self):
        s = Schedule(self.activities)
        actual = s.get_activity_by_start_time(Time(12, 0, 0))
        expected = 'lunch'
        self.assertEqual(expected, actual.name)

    def test_contains(self):
        s = Schedule(self.activities)
        self.assertIn('lunch', s)

    def test_overlaps_with(self):
        s1 = Schedule(self.activities)
        s2 = Schedule(self.activities)
        self.assertTrue(s1.overlaps_with(s2))

    def test_overlaps_by(self):
        s1 = Schedule(self.activities)
        s2 = Schedule(self.activities)
        expected = Time(3, 30, 0).to_minutes()
        actual = s1.overlaps_by(s2)
        self.assertEqual(expected, actual)




class EnvTests(unittest.TestCase):

    def setUp(self):
        self.wd = r'D:\DigitalAwayDay\python'
        self.data_file = os.path.join(self.wd, 'data.txt')
        self.p = Parser(self.data_file)
        self.activities = self.p.read_data_file()
        self.lunch = Activity(
            name='lunch',
            start_time=Time(12, 0, 0),
            duration=Time(1, 0, 0)
        )
        self.talk = Activity(
            name='talk',
            start_time=Time(16, 0, 0),
            duration=Time(1, 0, 0)
        )

    def test_she(self):
        e = Env(self.activities, [self.lunch, self.talk])
        a1 = Activity(
            'Archery',
            duration=Time(0, 45, 0),
            # start_time=Time(0, 0, 0)
        )
        a2 = Activity(
            'Learning Magic Tricks',
            duration=Time(0, 40, 0),
            # start_time=Time(0, 0, 0)
        )
        r = e.step([a1, a2])
        self.assertEqual(0, r)

    def test_compute_reward(self):
        e = Env(self.activities, [self.lunch, self.talk])
        # a = {
        #     'Buggy Driving':
        #         {'duration': Time(0, 30, 0), 'start_time': Time(9, 30, 0)},
        #     'Viking Axe Throwing':
        #         {'duration': Time(1, 0, 0), 'start_time': Time(10, 0, 0)}
        # }
        expected = -30

        e.compute_reward()




class AgentTests(unittest.TestCase):

    def setUp(self):
        self.wd = r'D:\DigitalAwayDay\python'
        self.data_file = os.path.join(self.wd, 'data.txt')
        self.p = Parser(self.data_file)
        self.activities = self.p.read_data_file()
        self.lunch = Activity(
            name='lunch',
            start_time=Time(12, 0, 0),
            duration=Time(1, 0, 0)
        )
        self.talk = Activity(
            name='talk',
            start_time=Time(16, 0, 0),
            duration=Time(1, 0, 0)
        )

    def test(self):
        a = RandomAgent()
        print(a)


class AlgorithmTests(unittest.TestCase):

    def setUp(self):
        self.wd = r'D:\DigitalAwayDay\python'
        self.data_file = os.path.join(self.wd, 'data.txt')
        self.p = Parser(self.data_file)
        self.activities = self.p.read_data_file()
        self.lunch = Activity(
            name='lunch',
            start_time=Time(12, 0, 0),
            duration=Time(1, 0, 0)
        )
        self.talk = Activity(
            name='talk',
            start_time=Time(16, 0, 0),
            duration=Time(1, 0, 0)
        )

    def test_random_agent(self):

        def episode(agent, env):
            done = False
            reward = 0
            while not done:
                actions = agent.get_action(env)
                r, done = env.step(actions)
                reward += r
            return r

        niter = 10000
        agent = RandomAgent()
        rec = []
        best = None
        env = Env(self.activities, [self.lunch, self.talk])
        reward = episode(agent, env)
        # print(reward)
        # print(env.schedules[0])
        for i in range(niter):
            # maybe a reset method?
            new_env = env.reset()
            # new_env = Env(self.activities, [self.lunch, self.talk])
            new_reward = episode(agent, env)

            if new_reward > reward:
                env = new_env
            # rec.append(reward)

            if i % 100 == 0:
                print(i, reward)

        print('best reward ', reward)
        print('schedule 1\n', env.schedules[0])
        print('schedule 2\n ', env.schedules[1])
        print('\n')



