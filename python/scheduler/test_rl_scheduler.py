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

    def test_is_between(self):
        t1 = Time(9, 0, 0)
        t2 = Time(10, 0, 0)
        t3 = Time(9, 30, 0)
        self.assertTrue(t3.is_between(t1, t2))

    def test_is_between2(self):
        t1 = Time(9, 0, 0)
        t2 = Time(10, 0, 0)
        t3 = Time(9, 30, 0)
        self.assertFalse(t2.is_between(t1, t3))


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

    def test_remove_from_schedule(self):
        new_activity = Activity(
            name='Cheese gnawing',
            start_time=Time(13, 0, 0),
            duration=Time(0, 30, 0)
        )
        s = Schedule(self.activities)

        s = s.add_to_schedule(new_activity)
        s = s.remove_from_schedule(new_activity)
        self.assertNotIn(new_activity, s)


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

    def test_time_occupied(self):
        s = Schedule(self.activities)
        t = Time(9, 15, 0)
        self.assertTrue(s.time_occupied(t))

    def test_time_occupied2(self):
        s = Schedule(self.activities)
        t = Time(9, 50, 0)
        self.assertFalse(s.time_occupied(t))

    def test_time_occupied3(self):
        s = Schedule(self.activities)
        t = Time(9, 30, 0)
        self.assertTrue(s.time_occupied(t))

    def test_get_next_available_time(self):
        s = Schedule(
            self.activities + [Activity(name='bandit rushing', start_time=Time(9, 30, 0), duration=Time(0, 30, 0))])
        time = Time(11, 0, 0)
        self.assertEqual(time, s.get_next_available_time())

    def test_slot_available1(self):
        s = Schedule(
            self.activities + [Activity(name='bandit rushing', start_time=Time(9, 30, 0), duration=Time(0, 30, 0))])
        start = Time(9, 0, 0)
        end = Time(9, 30, 0)
        self.assertFalse(s.slot_available(start, end))

    def test_slot_available2(self):
        s = Schedule(
            self.activities + [Activity(name='bandit rushing', start_time=Time(9, 30, 0), duration=Time(0, 30, 0))])
        start = Time(9, 15, 0)
        end = Time(9, 30, 0)
        self.assertFalse(s.slot_available(start, end))

    def test_slot_available3(self):
        s = Schedule(
            self.activities + [Activity(name='bandit rushing', start_time=Time(9, 30, 0), duration=Time(0, 30, 0))])
        start = Time(13, 0, 0)
        end = Time(13, 30, 0)
        print(s)
        self.assertTrue(s.slot_available(start, end))

    def test_slot_available4(self):
        s = Schedule(
            self.activities + [Activity(name='bandit rushing', start_time=Time(9, 30, 0), duration=Time(0, 30, 0))])
        start = Time(15, 45, 0)
        end = Time(16, 15, 0)
        self.assertFalse(s.slot_available(start, end))

    def test_slot_available5(self):
        """
        :return:
        """
        a1 = Activity('a1', start_time=Time(9, 0, 0), duration=Time(0, 45, 0))
        a2 = Activity('a2', start_time=Time(9, 45, 0), duration=Time(0, 40, 0))
        a3 = Activity('a3', start_time=Time(10, 25, 0), duration=Time(1, 0, 0))
        a4 = Activity('a4', start_time=Time(11, 25, 0), duration=Time(0, 15, 0))
        a5 = Activity('a5', start_time=Time(12, 0, 0), duration=Time(1, 0, 0))
        a6 = Activity('a6', start_time=Time(16, 0, 0), duration=Time(1, 0, 0))
        s = Schedule([a1, a2, a3, a4, a5, a6])
        self.assertFalse(s.slot_available(Time(11, 40, 0), Time(12, 10, 0)))

    def test_slot_available6(self):
        """
        :return:
        """
        a1 = Activity('a1', start_time=Time(9, 0, 0), duration=Time(1, 0, 0))
        a2 = Activity('a2', start_time=Time(10, 0, 0), duration=Time(0, 45, 0))
        a3 = Activity('a3', start_time=Time(10, 45, 0), duration=Time(0, 45, 0))
        a4 = Activity('a4', start_time=Time(11, 30, 0), duration=Time(0, 30, 0))
        a5 = Activity('a5', start_time=Time(12, 0, 0), duration=Time(1, 0, 0))
        a6 = Activity('a6', start_time=Time(16, 0, 0), duration=Time(1, 0, 0))
        s = Schedule([a1, a2, a3, a4, a5, a6])
        print(s)
        x = s.slot_available(Time(13, 0, 0), Time(16, 1, 0))
        print(x)

    def test_empty_space(self):
        s = Schedule(
            self.activities + [Activity(name='bandit rushing', start_time=Time(9, 30, 0), duration=Time(0, 30, 0))])
        expected = Time(4, 0, 0)
        self.assertEqual(expected, s.get_unused_time())

    def test_empty_space2(self):

        # get total unused time.
        # get total overused time.
        s = Schedule(self.activities)
        expected = Time(4, 30, 0)
        self.assertEqual(expected, s.get_unused_time())



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

    def test(self):
        # build several configurations of two or more teams and test the penalties for accuracy.
        pass

    def test_greatest_common_divisor(self):
        e = Env(self.activities, [self.lunch, self.talk])
        expected = 5
        actual = e.greatest_common_divisor
        self.assertEqual(expected, actual)


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
            step_count = 0
            while not done:
                step_count += 1
                # print('step count', step_count)
                actions = agent.get_action(env)
                # print('actions chosen', actions)
                # is the environment not updating after each iter?
                r, done = env.step(actions)

                # print(env.schedules[0], '\n')
                reward += r
            return r

        # is hte problem that I@m iteratig over self yet
        # self is not yet dontaining the new activity ???

        niter = 1
        agent = RandomAgent()
        rec = []
        best = None
        env = Env(self.activities, [self.lunch, self.talk])
        reward = episode(agent, env)
        # print(reward)
        print(env.schedules[0])
        # for i in range(niter):
        #     # maybe a reset method?
        #     new_env = env.reset()
        #     # new_env = Env(self.activities, [self.lunch, self.talk])
        #     new_reward = episode(agent, env)
        #
        #     if new_reward > reward:
        #         env = new_env
        #         reward = new_reward
        #     # rec.append(reward)
        #
        #     if i % 100 == 0:
        #         print(new_reward)
        #         print(i, reward)


        # print('best reward ', reward)
        # print('schedule 1\n', env.schedules[0])
        # print('schedule 2\n ', env.schedules[1])
        # print('\n')
