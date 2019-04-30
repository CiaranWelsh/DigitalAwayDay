import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
//import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

import static org.junit.Assert.assertEquals;

public class TimeTableTests {
    Path projectDir;
    Path dataFile;

    ArrayList<TimeTable> timeTables;

    @Before
    public void setUp() {
        this.projectDir = Paths.get(System.getProperty("user.dir"));
        this.dataFile = Paths.get(projectDir.toString(), "data.txt");
        if (!dataFile.toFile().exists())
            try {
                throw new FileDoesNotExistException();
            } catch (FileDoesNotExistException e) {
                e.printStackTrace();
            }
        Schedule schedule = null;
        try {
            schedule = new Schedule(this.dataFile, 2);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        this.timeTables = schedule.makeTimeTables();

    }

    @Test
    public void testGetValidStartTimes() {
        TimeTable timeTable = this.timeTables.get(0);
        HashMap<String, ArrayList<Integer>> valid = timeTable.getValidStartTimes();
        int actual = valid.get("morning").get(3);
        int expected = 45;
        assertEquals(expected, actual);
    }

    @Test
    public void testSize() {
        TimeTable timeTable = this.timeTables.get(0);
        int expected = 7;
        int actual = timeTable.size();
        assertEquals(expected, actual);
    }
    @Test
    public void testGetEarliestTime() {
        TimeTable timeTable = this.timeTables.get(0);
        Activity earliestTime = TimeTable.getEarliestTime(timeTable.activities);
        System.out.println(earliestTime.startTime);
    }


    @Test
    public void testRandomAssignment() {
        TimeTable timeTable = this.timeTables.get(0);
        Collections.sort(timeTable.activities);
        System.out.println(timeTable.activities);
//        System.out.println(timeTable.activities.size());
//        for (int i=0; i<timeTable.activities.size(); i++){
//            System.out.println(timeTable.activities.get(i));
//        }
//        timeTable.randomlyAssignActivitiesToStartTimes();


//        System.out.println(sortedActivities.get(0).startTime);
//        ArrayList<Activity> sortedActivities = timeTable.sort();

    }

}












