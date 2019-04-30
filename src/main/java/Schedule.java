import java.io.*;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;


public class Schedule {

    Path dataFile;
    int T;
    HashMap<Path, Object> fixedTimeSlots = new HashMap<>();
    ArrayList<Activity> activities;

    Time startTime = new Time(9, 0, 0);


    public Schedule(Path dataFile, int T) throws IOException, ClassNotFoundException {
        this.dataFile = dataFile;
        this.T = T;
        this.activities = this.readActivities();

    }

    /**
     * read activities from txt file
     * @return
     * @throws IOException
     */
    public ArrayList<Activity> readActivities() throws IOException {
        Parser p = new Parser(this.dataFile);
        return p.readFile();
    }

    /**
     * Split activities into T time tables
     * @return
     */
    public ArrayList<TimeTable> makeTimeTables() {
        ArrayList<ArrayList<Activity>> activitiesSet = new ArrayList<>();
        int i;
        while (!activities.isEmpty()) {

            for (i = 0; i <= T; i++) {
//                TimeTable timeTable = new TimeTable();
                if (activitiesSet.size() < T) {
                    activitiesSet.add(new ArrayList<>());
                }
                try {
                    Activity activity = activities.remove(0);
                    activitiesSet.get(i).add(activity);
                } catch (IndexOutOfBoundsException e) {
                    break;
                }
            }
        }
        ArrayList<TimeTable> timeTables = new ArrayList<>();
        for (i = 0; i < activitiesSet.size(); i++) {
            TimeTable timeTable = new TimeTable(activitiesSet.get(i));
            timeTables.add(timeTable);
        }
        return timeTables;
    }



}