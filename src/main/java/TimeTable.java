import java.util.ArrayList;
import java.util.HashMap;

import org.apache.commons.math3.distribution.EnumeratedIntegerDistribution;


public class TimeTable {

    Time dayStart = new Time(9, 0, 0);
    Time lunchStart = new Time(12, 0, 0);
    Time lunchEnd = new Time(13, 0, 0);
    Time afternoonStart = new Time(13, 0, 0);
    Time afternoonEnd = new Time(16, 0, 0);
    Time dayEnd = new Time(15, 0, 0);
    Time morningSess = lunchStart.minus(dayStart);
    Time afternoonSess = afternoonEnd.minus(afternoonStart);

    ArrayList<Activity> activities;
    ArrayList<Time> potentialStartTimes;

    // todo plus lunch and final hour into every activity list
    // todo implement this as list of time objects

    public TimeTable(ArrayList<Activity> activities) {
        this.activities = activities;
        potentialStartTimes = this.getValidStartTimes();

        this.activities = this.randomlyAssignActivitiesToStartTimes();
//        this.addFinalActivity();
//        this.addLunchAsActivity();
//        Collections.sort(this.activities);
    }

    private void addLunchAsActivity() {
        Activity lunch = new Activity("lunch", 60);
        lunch.startTime = new Time(12, 0, 0);
        activities.add(lunch);
    }

    private void addFinalActivity() {
        Activity finalActivity = new Activity("lastActivity", 60);
        finalActivity.startTime = new Time(16, 0, 0);
        activities.add(finalActivity);
    }


    public void computeScore() {
        // need to iterate over 1 less than size of activities to get difference
        //
        int N = this.activities.size() - 1;
        int minutesOverlap = 0;
        Time endTimeOfCurrent;
        Time startTimeOfNext;
        for (int i = 0; i < N; i++) {
            //end time of current
            endTimeOfCurrent = this.activities.get(i).startTime.plus(this.activities.get(i).duration);
            startTimeOfNext = this.activities.get(i + 1).startTime;
//            System.out.println(String.format("end time of current= %s, start time of next=%s, minus=%s",
//                    endTimeOfCurrent.toString(), startTimeOfNext.toString(),
//                    endTimeOfCurrent.minus(startTimeOfNext).toString()));


//            minutesOverlap += this.activities.get(i+1).startTime.minus(
//                    this.activities.get(i).startTime).toMin();
        }

//        Activity k = activities.stream()
//                .reduce(new Time(0, 0, 0),
//                        (x, y) -> x.startTime.toMin() + y.startTime.toMin());
    }

    /**
     * Get the shortest duration in the list of activities
     *
     * @return
     */
    private Integer getShortestDuration() {
        Integer shortestDuration = 10000;
        for (int i = 0; i < this.activities.size(); i++) {
            if (this.activities.get(i).duration.toMin() < shortestDuration)
                shortestDuration = this.activities.get(i).duration.toMin();
        }
        return shortestDuration;
    }

    /**
     * get list of valid starting times in multiples of shortest session
     *
     * @return
     */
    private ArrayList<Time> getValidMorningTimes() {
        int morningSessMin = this.morningSess.toMin();
        ArrayList<Time> validMorningTimes = new ArrayList<>();
        for (int i = 0; i < morningSessMin; i += this.getShortestDuration()) {
            validMorningTimes.add(new Time(0, i, 0));
        }
        return validMorningTimes;
    }

    /**
     * get list of valid starting times in multiples of shortest session
     *
     * @return
     */
    private ArrayList<Time> getValidAfternoonTimes() {
        // get afternoon session available starting slots in multiples of shortest session
        int afternoonSessMin = this.afternoonSess.toMin();
        ArrayList<Time> validAfternoonTimes = new ArrayList<>();
        for (int i = 0; i < afternoonSessMin; i += this.getShortestDuration()) {
            validAfternoonTimes.add(new Time(0, i, 0));
        }
        return validAfternoonTimes;
    }

    /**
     * assemble valid morning and afternoon starting slots
     * into HashMap
     *
     * @return
     */
    public ArrayList<Time> getValidStartTimes() {
        HashMap<String, ArrayList<Time>> result = new HashMap<>();
        Time nineAM = new Time(9, 0, 0);
        Time onePM = new Time(13, 0, 0);

        ArrayList<Time> validMorningTimes = this.getValidMorningTimes();
        ArrayList<Time> validAfternoonTimes = this.getValidAfternoonTimes();

        for (int t = 0; t < validMorningTimes.size(); t++) {
            validMorningTimes.set(t, validMorningTimes.get(t).plus(nineAM));
            validAfternoonTimes.set(t, validAfternoonTimes.get(t).plus(onePM));
        }

        ArrayList<Time> validTimes = new ArrayList<>();
        for (Time t : validAfternoonTimes)
            validTimes.add(t);
        for (Time t : validMorningTimes)
            validTimes.add(t);
        return validTimes;
    }

    /**
     * init array for index and prob vector
     * iterate over number of activities
     *      populate initialized index array with indexes
     * @return
     */
    private Time randomlySampleTime() {
        ArrayList<Integer> allPotentialIndexes = new ArrayList<>();
        ArrayList<Double> probVec = new ArrayList<>();
        for (int j = 0; j < activities.size(); j++) {
            allPotentialIndexes.add(j);
            probVec.add(1.0 / potentialStartTimes.size());
        }
        // randomly pick an index. Note we need the index to remove and sample without replacement
        EnumeratedIntegerDistribution dist2 = new EnumeratedIntegerDistribution(
                allPotentialIndexes.stream().mapToInt(Integer::intValue).toArray(),
                probVec.stream().mapToDouble(Double::doubleValue).toArray());
        int idx = dist2.sample();
        Time timeAtIndex = potentialStartTimes.remove(idx);
        System.out.println(timeAtIndex);
        System.out.println();

        return timeAtIndex;
    }
//        System.out.println(String.format("idx is %d. len %d, %d",
//                idx, allPotentialIndexes.size()),
//
//                );
//        Time time = potentialStartTimes.get(idx);
//        potentialStartTimes.remove(time);
//        allPotentialIndexes.remove(idx);
//        System.out.println(allPotentialIndexes);
//        return time;
//    }

    /**
     *
     * @return
     */
    public int size() {
        return this.activities.size();
    }

    /**
     * Randomly assign activities to start times
     *
     * @return
     */
    public ArrayList<Activity> randomlyAssignActivitiesToStartTimes() {
//        System.out.println(String.format("How many activities do we have? %d", activities.size()));
//        System.out.println(String.format("What are the valid start times? %s", potentialStartTimes.toString()));
        ArrayList<Activity> newActivities = new ArrayList<>();
//        Time timeStart = new Time(0, 0, 0);
//        HashMap<String, Time> activityTimeStart;
        int values[] = {0, 1};
        double probs[] = {0.5, 0.5};
        for (Activity activity : activities) {
            activity.startTime = this.randomlySampleTime();
        }
        return activities;
    }
}

//        /**
//         * get the earliest time available in activities
//         *
//         * @param activities
//         * @return
//         */
//        public void getEarliestTime() {
//            Activity activity = activities.get(0);
//            if (activity.startTime.equals(null))
//                try {
//                    throw new Exception("Cannot sort before schedules have been assigned");
//                } catch (Exception e) {
//                    e.printStackTrace();
//                }
//            for (int i = 1; i < activities.size(); i++) {
//                Activity newActivity = activities.get(i);
//                if (newActivity.startTime.lt(activity.startTime)) {
//                    activity = newActivity;
//                }
//            }
////            return activity;
//        }
//    }
//}
//
//}

