import org.junit.Test;
import static org.junit.Assert.*;

public class TimeTests {


    @Test
    public void testDiff(){
        Time time1 = new Time(9, 0, 0);
        Time time2 = new Time(10, 0, 0);
        Time diff = time1.minus(time2);
        Integer expected = -1;
        Integer actual = diff.hour;
        assertEquals(expected, actual);
    }

    @Test
    public void testAdd() {
        Time time1 = new Time(9, 0, 0);
        Time time2 = new Time(10, 0, 0);
        Time sum = time1.plus(time2);
        Integer expected = 19;
        Integer actual = sum.hour;
        assertEquals(expected, actual);
    }
    @Test
    public void testTooManyMinutes() {
        Time time1 = new Time(1, 65, 0);
        assertEquals(time1.hour, 2);
        assertEquals(time1.minutes, 5);
    }
    @Test
    public void testTooManySeconds() {
        Time time1 = new Time(1, 65, 94);
        assertEquals(time1.hour, 2);
        assertEquals(time1.minutes, 6);
        assertEquals(time1.seconds, 34);
    }

    @Test
    public void testToMin(){
        Time time1 = new Time(1, 65, 94);
        assertEquals(126, time1.toMin());
    }


}
