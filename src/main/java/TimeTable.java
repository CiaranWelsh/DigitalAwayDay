import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

import org.apache.commons.math3.distribution.EnumeratedIntegerDistribution;


public class TimeTable {

    Time dayStart = new Time(9, 0, 0);
    Time lunchStart = new Time(12, 0, 0);
    Time lunchEnd = new Time(13, 0, 0);
    Time afternoonStart = new Time(13, 0, 0);
    Time afternoonEnd = new Time(16, 0, 0);
    Time dayEnd = new Time(15, 0, 0);
    Time morningSess = lunchStart.diff(dayStart);
    Time afternoonSess = afternoonEnd.diff(afternoonStart);

    ArrayList<Activity> activities;

    // todo implement TimeTable so that it accepts an array as argument
    public TimeTable(ArrayList<Activity> activities) {
        this.activities = activities;
        this.activities = this.randomlyAssignActivitiesToStartTimes();
//        this.activities = Collections.sort(this.activities);
    }

    private void calculateScore() {
        ;
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
    private ArrayList<Integer> getValidMorningTimes() {
        int morningSessMin = this.morningSess.toMin();
        ArrayList<Integer> validMorningTimes = new ArrayList<>();
        for (int i = 0; i < morningSessMin; i += this.getShortestDuration()) {
            validMorningTimes.add(i);
        }
        return validMorningTimes;
    }

    /**
     * get list of valid starting times in multiples of shortest session
     *
     * @return
     */
    private ArrayList<Integer> getValidAfternoonTimes() {
        // get afternoon session available starting slots in multiples of shortest session
        int afternoonSessMin = this.afternoonSess.toMin();
        ArrayList<Integer> validAfternoonTimes = new ArrayList<>();
        for (int i = 0; i < afternoonSessMin; i += this.getShortestDuration()) {
            validAfternoonTimes.add(i);
        }
        return validAfternoonTimes;
    }

    /**
     * assemble valid morning and afternoon starting slots
     * into HashMap
     *
     * @return
     */
    public HashMap<String, ArrayList<Integer>> getValidStartTimes() {

        ArrayList<Integer> validMorningTimes = this.getValidMorningTimes();
        ArrayList<Integer> validAfternoonTimes = this.getValidAfternoonTimes();
        HashMap<String, ArrayList<Integer>> result = new HashMap<>();
        result.put("morning", validMorningTimes);
        result.put("afternoon", validAfternoonTimes);
        return result;
    }

    /**
     * randomly pick morning or afternoon with equal probability
     *
     * @return
     */
    private HashMap<String, Time> sampleStartTime() {
        HashMap<String, Time> result = new HashMap<>();

        String session;
        Time timeStart = new Time(0, 0, 0);
        int values[] = {0, 1};
        double probs[] = {0.5, 0.5};
        EnumeratedIntegerDistribution dist = new EnumeratedIntegerDistribution(values, probs);
        if (dist.sample() == 1) {
            session = "morning";
        } else {
            session = "afternoon";
        }
        if (session.equals("morning"))
            timeStart = new Time(9, 0, 0);
        else if (session.equals("afternoon"))
            timeStart = new Time(13, 0, 0);
        else
            try {
                throw new Exception("bad");
            } catch (Exception e) {
                e.printStackTrace();
            }
        result.put(session, timeStart);
        return result;
    }

    /**
     * Randomly assign activities to start times
     *
     * @return
     */
    public ArrayList<Activity> randomlyAssignActivitiesToStartTimes() {
        HashMap<String, ArrayList<Integer>> potentialStartTimes = this.getValidStartTimes();
        ArrayList<Activity> newActivities = new ArrayList<>();
        Time timeStart = new Time(0, 0, 0);
        HashMap<String, Time> activityTimeStart;
        int values[] = {0, 1};
        double probs[] = {0.5, 0.5};
        // iterate over number of activities
        for (int i = 0; i < activities.size(); i++) {

            activityTimeStart = this.sampleStartTime();
            String session = (String) activityTimeStart.keySet().toArray()[0];
            Time startTime = (Time) activityTimeStart.values().toArray()[0];

            // for each available time slot in chosen session, assign activity i
            ArrayList<Integer> allPotentialIndexes = new ArrayList<>();
            ArrayList<Double> probVec = new ArrayList<>();
            for (int j = 0; j < activities.size(); j++) {
                allPotentialIndexes.add(j);
                probVec.add(1.0 / potentialStartTimes.get(session).size());
            }
            // randomly pick an index
            EnumeratedIntegerDistribution dist2 = new EnumeratedIntegerDistribution(
                    allPotentialIndexes.stream().mapToInt(Integer::intValue).toArray(),
                    probVec.stream().mapToDouble(Double::doubleValue).toArray());

            // get start time from chosen session
            int idx = dist2.sample();
            Integer activityStartTimeInMinutesAfterStartTime = potentialStartTimes.get(session).get(idx);
            Time activityStartTime = startTime.add(new Time(0, activityStartTimeInMinutesAfterStartTime, 0));
            activities.get(i).startTime = activityStartTime;
            newActivities.add(activities.get(i));
            activities.remove(i);
        }
        return newActivities;
    }

    /**
     * get the earliest time available in activities
     *
     * @param activities
     * @return
     */
    public static Activity getEarliestTime(ArrayList<Activity> activities) {
        Activity activity = activities.get(0);
        if (activity.startTime.equals(null))
            try {
                throw new Exception("Cannot sort before schedules have been assigned");
            } catch (Exception e) {
                e.printStackTrace();
            }
        for (int i = 1; i < activities.size(); i++) {
            Activity newActivity = activities.get(i);
            if (newActivity.startTime.lt(activity.startTime)) {
                activity = newActivity;
            }
        }
        return activity;
    }

    /**
     * adds up total overlapping minutes
     * in start time assigments. Be careful to
     * not include the same time twice.
     * Include any time overlapping with forbidden slots.
     */
    public void computeScore() {

    }


    public int size() {
        return this.activities.size();
    }

}

