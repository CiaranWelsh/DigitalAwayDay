import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;

public class ScheduleTests {
    Path projectDir;
    Path dataFile;

    @Before
    public void setUp() throws FileDoesNotExistException {
        this.projectDir = Paths.get(System.getProperty("user.dir"));
        this.dataFile = Paths.get(projectDir.toString(), "data.txt");
        if (!dataFile.toFile().exists())
            throw new FileDoesNotExistException();
    }

    @Test
    public void testActivityLength() throws IOException, ClassNotFoundException {
        Schedule schedule = new Schedule(this.dataFile, 2);
        int expected = 20;
        int actual = schedule.activities.size();
        assertEquals(expected, actual);

    }

    @Test
    public void makeTimeTables() throws IOException, ClassNotFoundException {
        Schedule schedule = new Schedule(this.dataFile, 2);
        ArrayList<TimeTable> timeTables = schedule.makeTimeTables();
        int expected = 2;
        int actual = timeTables.size();
        assertEquals(expected, actual);
    }


    @Test
    public void testFixedParameters() throws IOException, ClassNotFoundException {

//        Instant instant = new Instant(15.0);
        ;
//        HashMap<String, HashMap<Instant, Instant>> fixedTimeSlots = new HashMap<>();
//        fixedTimeSlots.put('before', HashMap<Instant(12:00)>)
//
//        Schedule schedule = new Schedule(this.dataFile, 2);

    }


}
