import junit.framework.TestCase;
import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

import java.time.Duration;

public class ActivityTests {

    @Before
    public void ActivityTests() {
        ;
    }

    @Test
    public void testActivityInstantiation(){
        String name = "Duck Hearding";
        int len = 60;
        Activity activity = new Activity(name, len);
        String expected = "Activity(name=\"Duck Hearding\", startTime=Time(hour=0, minutes=0, seconds=0))";
        String actual = activity.toString();
        assertEquals(expected, actual);

    }
    @Test
    public void test(){
        String name = "Duck Hearding";
        int len = 60;
        Activity activity1 = new Activity(name, len);
        Activity activity2 = new Activity(name, len);
//        System.out.println(activity1 > activity2);

    }



}
