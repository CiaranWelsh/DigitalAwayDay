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
    Time morningSess = lunchStart.diff(dayStart);
    Time afternoonSess = afternoonEnd.diff(afternoonStart);

    ArrayList<Activity> activities;

    // todo implement TimeTable so that it accepts an array as argument
    public TimeTable(ArrayList<Activity> activities) {
        this.activities = activities;
    }

    private void calculateScore() {
        ;
    }

    public Integer getShortestDuration() {
        // get the shortest duration in our list of activities
        Integer shortestDuration = 10000;
        for (int i = 0; i < this.activities.size(); i++) {
            if (this.activities.get(i).duration.toMin() < shortestDuration)
                shortestDuration = this.activities.get(i).duration.toMin();
        }
        return shortestDuration;
    }

    private ArrayList<Integer> getValidMorningTimes() {
        // get morning session available starting slots in multiples of shortest session
        int morningSessMin = this.morningSess.toMin();
        ArrayList<Integer> validMorningTimes = new ArrayList<>();
        for (int i = 0; i < morningSessMin; i += this.getShortestDuration()) {
            validMorningTimes.add(i);
        }
        return validMorningTimes;
    }

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
     * Find out what lowest duration is on the list
     * and produce an array of valid start times
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

    private String sampleMorningOrAfternoon() {
        int values[] = {0, 1};
        double probs[] = {0.5, 0.5};
        String session;
        EnumeratedIntegerDistribution dist = new EnumeratedIntegerDistribution(values, probs);
        if (dist.sample() == 1) {
            session = "morning";
        } else {
            session = "afternoon";
        }
        return session;
    }

    /**
     * Randomly select morning or afternoon
     * then randomly pick a number without replacement.
     *
     * @return
     */
    public void randomlyAssignActivitiesToStartTimes() {
        // place to store potential starting times
        HashMap<String, ArrayList<Integer>> potentialStartTimes = this.getValidStartTimes();
        // place to store assigned time table

        // start of session (morning or evening)
        Time timeStart = new Time(0, 0, 0);
        // placeholder for starting time of each activity that is assigned
        Time activityTimeStart;
        int values[] = {0, 1};
        double probs[] = {0.5, 0.5};
        // iterate over number of activities
        for (int i = 0; i < activities.size(); i++) {

            String session = this.sampleMorningOrAfternoon();
            if (session.equals("morning"))
                timeStart = new Time(9, 0, 0);
            else if (session.equals("afternoon"))
                timeStart = new Time(13, 0, 0);
            else
                try{
                    throw new Exception("bad");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            // for each available time slot in chosen session, assign activity i
            ArrayList<Integer> allPotentialIndexes = new ArrayList<>();
            ArrayList<Double> probVec = new ArrayList<>();
            for (Integer j = 0; j < activities.size(); j++) {
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

            potentialStartTimes.remove(idx);
            activityTimeStart = timeStart.add(new Time(0, activityStartTimeInMinutesAfterStartTime, 0));
            activities.get(idx).startTime = activityTimeStart;
        }
//        return activities;
    }

    public static Activity getEarliestTime(ArrayList<Activity> activities) {
        Activity activity = activities.get(0);
        if (activity.startTime.equals(null))
            try {
                throw new Exception("Cannot sort before schedules have been assigned");
            } catch (Exception e){
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


    public ArrayList<Activity> sort() {
        ArrayList<Activity> sorted = new ArrayList<>();
        Activity activity = this.activities.get(0);
        while (!this.activities.isEmpty()){
            Activity earliestActivity = TimeTable.getEarliestTime(this.activities);
            sorted.add(earliestActivity);
            this.activities.remove(earliestActivity);
        }
        return sorted;
    }

    /**
     * adds up total overlapping minutes
     * in start time assigments. Be careful to
     * not include the same time twice.
     * Include any time overlapping with forbidden slots.
     */
    public void computeScore() {

    }


    public int size(){
        return this.activities.size();
    }

}

