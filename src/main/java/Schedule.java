import java.io.*;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;


public class Schedule {

    Path dataFile;
    int T;
    ArrayList<Activity> activities;


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
        ArrayList<ArrayList<Activity>> newActivities = new ArrayList<>();
        int i;
        while (!this.activities.isEmpty()) {

            for (i = 0; i < T; i++) {
//                TimeTable timeTable = new TimeTable();
                if (newActivities.size() < T) {
                    newActivities.add(new ArrayList<>());
                }
                try {
                    Activity activity = this.activities.remove(0);
                    newActivities.get(i).add(activity);
                } catch (IndexOutOfBoundsException e) {
                    break;
                }
            }
        }
        ArrayList<TimeTable> timeTables = new ArrayList<>();
        for (i = 0; i < newActivities.size(); i++) {
            TimeTable timeTable = new TimeTable(newActivities.get(i));
            timeTables.add(timeTable);
        }
        return timeTables;
    }



}