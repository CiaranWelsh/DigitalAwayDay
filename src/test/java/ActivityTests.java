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
        String expected = "Activity(\"name\"=Duck Hearding, duration=PT1Hmin)";
        String actual = activity.toString();
        assertEquals(expected, actual);

    }



}
