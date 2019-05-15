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
        System.out.println(schedule.activities.size());
        this.timeTables = schedule.makeTimeTables();

    }

    @Test
    public void testGetValidStartTimes() {
        TimeTable timeTable = this.timeTables.get(0);
        ArrayList<Time> valid = timeTable.getValidStartTimes();
        Time actual = valid.get(3);
        int expected = 45;
        assertEquals(expected, actual);
    }

    @Test
    public void testSize() {
        TimeTable timeTable = this.timeTables.get(0);
        int expected = 10;
        int actual = timeTable.size();
        assertEquals(expected, actual);
    }
//    @Test
//    public void testGetEarliestTime() {
//        TimeTable timeTable = this.timeTables.get(0);
//        Activity earliestTime = TimeTable.getEarliestTime(timeTable.activities);
//        System.out.println(earliestTime.startTime);
//    }


    @Test
    public void testRandomAssignment() {
        TimeTable timeTable1 = this.timeTables.get(0);
        TimeTable timeTable2 = this.timeTables.get(1);
        System.out.println(timeTable1.size());
        System.out.println(timeTable2.size());
        ;

    }

}












