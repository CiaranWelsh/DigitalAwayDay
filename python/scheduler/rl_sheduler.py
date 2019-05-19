import os, glob
from re import findall
import numpy as np
from random import choice
from itertools import combinations
from collections import OrderedDict
from copy import deepcopy

from .time import Time


class Parser:

    def __init__(self, data_file):
        self.data_file = data_file

    def read_data_file(self):
        with open(self.data_file) as f:
            lines = f.readlines()
        lines = [i.strip() for i in lines]
        l = []
        for i in lines:
            duration = findall('(\d*min)|(sprint)', i)[0]
            duration = list(duration)
            duration = [i for i in duration if i != ''][0]
            activity = i.replace(duration, '').strip()
            if duration == 'sprint':
                duration = '15min'
            duration = int(duration.replace('min', ''))
            l.append(Activity(
                name=activity,
                start_time=Time(0, 0, 0),
                duration=Time(0, duration, 0)
            ))

        return l


class Activity:

    def __init__(self, name, duration, start_time=None):
        self.name = name
        self.duration = duration
        self.start_time = start_time

        if not isinstance(self.duration, Time):
            raise TypeError

        if self.start_time is not None:
            if not isinstance(self.start_time, Time):
                raise TypeError

    def __str__(self):
        return f"Activity('{self.name}', {self.duration}, start_time={self.start_time})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.name == other.name and self.duration == other.duration and self.start_time == other.start_time:
            return True
        return False

    def __ne__(self, other):
        if self.name == other.name and self.duration == other.duration and self.start_time == other.start_time:
            return False
        return True

    def __lt__(self, other):
        if self.start_time < other.start_time:
            return True
        return False

    def __gt__(self, other):
        if self.start_time > other.start_time:
            return True
        return False

    def __ge__(self, other):

        if self.start_time >= other.start_time:
            return True
        return False

    def __le__(self, other):

        if self.start_time <= other.start_time:
            return True
        return False

    def __contains__(self, item):
        assert isinstance(item, Schedule)
        if self.name in item.keys():
            return True
        return False

    def overlaps_with(self, other):
        first = self

        if other < self:
            first = other
            second = self
        else:
            second = other
        first_end_time = first.start_time + first.duration
        if first_end_time > second.start_time:
            return True
        return False

    def overlaps_by(self, other):
        first = self
        if other < self:
            first = other
            second = self
        else:
            second = other
        first_end_time = first.start_time + first.duration
        if first_end_time > second.start_time:
            return first_end_time - second.start_time
        return Time(0, 0, 0)


class Schedule:
    """
    A dict like class
    Sorted activities

    """

    current = -1

    def __init__(self, activities=[]):
        if isinstance(activities, Activity):
            activities = [activities]

        if not isinstance(activities, list):
            raise TypeError("activities should be a list of Activity objects")

        self.activities = sorted(activities)

    def add_to_schedule(self, activity, inplace=False):
        """

        :return:
        """
        if not isinstance(activity, Activity):
            raise TypeError('Need an Activity object but got {}'.format(type(activity)))

        if inplace:
            self.activities.append(activity)
            self.activities = sorted(self.activities)
        else:
            activities = deepcopy(self.activities)
            activities.append(activity)
            activities = sorted(activities)
            return Schedule(activities)

    def remove_from_schedule(self, activity, inplace=False):
        """

        :return:
        """
        if not isinstance(activity, Activity):
            raise TypeError('Need an Activity object but got {}'.format(type(activity)))

        if inplace:
            idx = None
            for i in range(len(self.activities)):
                if self.activities[i] == activity:
                    idx = i
            if idx is not None:
                del self.activities[idx]
                self.activities = sorted(self.activities)
        else:
            idx = None
            activities = deepcopy(self.activities)
            for i in range(len(activities)):
                if activities[i] == activity:
                    idx = i
            if idx is not None:
                del activities[idx]
                activities = sorted(activities)
            return Schedule(activities)

    def get_activity_by_name(self, item):
        activity = None
        for i in self.activities:
            if i.name == item:
                activity = i
        if activity is None:
            raise KeyError(f'An activity called {item} is not present in the '
                           f'schedule')
        return activity

    def get_activity_by_start_time(self, start_time):
        activity = None
        for i in self.activities:
            if i.start_time == start_time:
                activity = i
        return activity

    def __len__(self):
        return len(self.activities)

    def __str__(self):
        s = ''
        for i in self.activities:
            s += f"{i.start_time} - {i.start_time + i.duration}: {i.name}\n"
        s = s.strip()
        return s

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.current += 1
            return self.activities[self.current]
        except IndexError:
            self.current = -1
            raise StopIteration

    def __contains__(self, item):
        if not isinstance(item, (Activity, str)):
            raise TypeError('Schedule can only contain Activity objects')
        if isinstance(item, Activity):
            item = item.name

        try:
            if self.get_activity_by_name(item):
                return True
        except KeyError:
            return False

    def get_activity_names(self):
        return [i.name for i in self]

    def overlaps_with(self, other):
        if not isinstance(other, Schedule):
            raise TypeError

        activity_names = self.get_activity_names()

        for i in activity_names:
            if i in other:
                x = self.get_activity_by_name(i)
                y = other.get_activity_by_name(i)
                if x.overlaps_with(y):
                    return True
        return False

    def overlaps_by(self, other):
        if not isinstance(other, Schedule):
            raise TypeError

        activity_names = self.get_activity_names()

        total_overlap = 0
        for i in activity_names:
            if i in other:
                x = self.get_activity_by_name(i)
                y = other.get_activity_by_name(i)
                if x.overlaps_with(y):
                    total_overlap += x.overlaps_by(y).to_minutes()
        return total_overlap

    def time_occupied(self, time):
        """
        If time is occupied by schedule return True
        :param time:
        :return:
        """
        for i in self:
            if time > i.start_time and time < i.start_time + i.duration:
                return True
        return False

    def get_used_time_slots(self):
        return [
            (i.start_time, i.start_time + i.duration) for i in self.activities
        ]

    def get_next_available_time(self, increment):
        time = Time(9, 0, 0)
        increment = Time(0, increment, 0)  # 15 minute increments as this is the smallest session
        used_time_slots = self.get_used_time_slots()

        def recursion(used_time_slots, time):
            for start, end in used_time_slots:
                done = False
                while not done:
                    if time.is_between(start, end):
                        time = time + increment
                    else:
                        done = True
                if time == end:
                    continue
                else:
                    return time

        time = recursion(used_time_slots, time)
        return time

    def slot_available(self, start_time, end_time):
        if start_time > end_time:
            raise ValueError('start time "{}" cannot be later than end time "{}"'.format(
                start_time, end_time
            ))
        available = True
        for i in self:
            if start_time >= i.start_time and start_time < i.start_time + i.duration:
                available = False
            if end_time > i.start_time and end_time < i.start_time + i.duration:
                available = False

        return available

    def get_unused_time(self, early=Time(9, 0, 0), late=Time(17, 0, 0)):
        """
        return the amount of unused time between early and late

        :param early:
        :param late:
        :return:
        """
        total_time = late - early
        total_used = Time(0, 0, 0)
        for i in self:
            total_used = total_used + i.duration
        if total_used > total_time:
            return Time(0, 0, 0)
        else:
            return total_time - total_used

    def get_earliest_time(self):
        pass


class Env:
    start_time = Time(9, 0, 0)
    end_time = Time(17, 0, 0)
    total_duration = end_time - start_time

    def __init__(self, activities, fixed_slots, n=2):
        self.activities = activities
        self.fixed_slots = fixed_slots
        if not isinstance(self.activities, list):
            raise TypeError

        if not isinstance(self.fixed_slots, list):
            raise TypeError

        # self.activities = self.activities + self.fixed_slots
        self._activities_copy = deepcopy(self.activities)
        self.n = n
        self.time_cursors = self._create_new_time_cursors()
        self.schedules = self._create_new_schedules()

    @property
    def greatest_common_divisor(self):
        """
        Use the smallest common factor of all activity durations
        as the time increment
        :return:
        """

        def gcd(a, b):
            """Return greatest common divisor using Euclid's Algorithm."""
            while b:
                a, b = b, a % b
            return a

        def lcmm(*args):
            """Return gcd of args."""
            from functools import reduce
            return reduce(gcd, args)

        return int(lcmm(*[i.duration.to_minutes() for i in self.activities]))

    def _create_new_time_cursors(self):
        return [Time(9, 0, 0)] * self.n

    def _create_new_schedules(self):
        return [Schedule(self.fixed_slots) for _ in range(self.n)]

    # def termination_criteria(self):

    def step(self, a):
        """
        modify array of activities
        modify list of available activities
        Move the time curser forwards by the appropriate amount
        calculate reward
        return next state

        Include lunch as a regular activity.
        Large negative reward for not having lunch at 12:00
        Also terminates the episode
        :return:
        """
        r = 0
        done = [False] * self.n

        for i in range(self.n):
            if self.time_cursors[i] > self.end_time:
                done[i] = True
                continue  # i is done, continue through for other n teams
            activity = a[i]

            if not self.schedules[i].slot_available(self.time_cursors[i], self.time_cursors[i] + activity.duration):
                self.time_cursors[i] = self.time_cursors[i] + Time(0, self.greatest_common_divisor, 0)
                continue  ## bad time has been chosen, continue

            activity.start_time = self.time_cursors[i]
            self.schedules[i] = self.schedules[i].add_to_schedule(activity)

            r = self.compute_reward(activity)
            self.time_cursors[i] = self.time_cursors[i] + activity.duration

        if all(done):
            done = True
            # print('time cursers, done is true', self.time_cursors)
        else:
            done = False

        return r, done

    def compute_reward(self, activity):
        """
        Large negative reward for same activity on at the same time

        3) IF lunch or talk not at 12 pr 1600 repectively, penalty
        1) when activity extends into lunch, talk or goes over, penalty
        2) when activity is on at the same time in two places, penalty
        :return:
        """
        r = 0
        # first deal with penalties for lunch and talk not being present at the correct time
        # p1 = self._penalty1(activity)
        # Now give penalty for when a talk goes over into lunch or talk
        over_used_penalty = self._overused_time_penalty(activity)
        unused_time_penalty = self._unused_time_penalty()

        # penalty for double booking
        overlap_penalty = self._overlaps_with_other_teams_penalty()

        # if all equal to 0, then add 1
        print(over_used_penalty, overlap_penalty, unused_time_penalty)
        if over_used_penalty == 0 and overlap_penalty == 0 and unused_time_penalty == 0:
            r += 1

        # r += p1
        r += over_used_penalty
        r += overlap_penalty
        r += unused_time_penalty

        return r

    def _overused_time_penalty(self, activity):
        r = 0
        lunch = Activity(name='lunch', start_time=Time(12, 0, 0), duration=Time(1, 0, 0))
        talk = Activity(name='talk', start_time=Time(16, 0, 0), duration=Time(1, 0, 0))
        if activity.overlaps_with(lunch):
            r -= activity.overlaps_by(lunch).to_minutes()

        if activity.overlaps_with(talk):
            r -= activity.overlaps_by(talk).to_minutes()

        activity_end = activity.start_time + activity.duration
        if activity_end > Time(17, 0, 0):
            extra = activity_end - Time(17, 0, 0)
            r -= extra.to_minutes()
        return r

    def _overlaps_with_other_teams_penalty(self):
        """
        penalty for activities that are on at the same time for multiple teams,
        returns the negative of the total amount of negative overlap
        :return:
        """
        r = 0
        combs = combinations(range(self.n), 2)
        for comb in combs:
            r -= self.schedules[comb[0]].overlaps_by(self.schedules[comb[1]])
        return r

    def _penalty4(self):
        for activity in self.activities:
            # count the number of schedules containing activity
            count = 0
            for schedule in self.schedules:
                if activity in schedule:
                    count += 1
            # if activity in both schedules, get the activity from both schedules
            if count > 1:
                schedule_activities = []
                for schedule in self.schedules:
                    # get the activity
                    schedule_activities.append(
                        schedule.get_activity_by_name(activity.name)
                    )
                    # but how does this generalise to the multiple
                    # Maybe its better to go back to combinations like in penalty3

    def _unused_time_penalty(self):
        """
        empty space penalty.
        :return:
        """
        total_unused_time = Time(0, 0, 0)
        for schedule in self.schedules:
            total_unused_time = total_unused_time + schedule.get_unused_time()
        return total_unused_time.to_minutes() * -1

    def valid_actions(self):
        l = []
        for i in range(self.n):
            l2 = []
            for activity in self.activities:
                if activity not in self.schedules[i]:
                    l2.append(activity)
            l.append(l2)
        return l

    def reset(self):
        self.activities = deepcopy(self._activities_copy)
        self.schedules = self._create_new_schedules()
        self.time_cursors = self._create_new_time_cursors()


class Agent:

    def __init__(self):
        pass

    def get_action(self, state, actions, n):
        """

        :param state: current schedule
        :param actions: all potential actions
        :param n: number of activities needed
        :return:
        """
        pass


class RandomAgent(Agent):

    def __init__(self):
        super().__init__()

    def get_action(self, env):
        if not isinstance(env, Env):
            raise TypeError
        n = env.n

        chosen = []
        for i in range(n):
            valid_actions = env.valid_actions()[i]

            chosen.append(choice(valid_actions))
        return chosen


if __name__ == '__main__':
    WD = r'D:\DigitalAwayDay\python'
    data_file = os.path.join(WD, 'data.txt')
