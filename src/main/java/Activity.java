import java.time.Duration;
import java.util.HashMap;

public class Activity implements Comparable<Activity> {

    String name;
    Time duration;
    String units = "min";
    Time startTime = new Time(0, 0, 0);

    Activity(String name, int duration) {
        this.name = name;
        this.duration = new Time(0, duration, 0);
    }

    @Override
    public String toString() {
        return "Activity(name=\"" + this.name + "\", startTime=" +
                this.startTime + ")";
    }

    @Override
    public int compareTo(Activity other) {
        if (this.startTime.toSeconds() == other.startTime.toSeconds())
        {
            return 0;
        } else if (this.startTime.toSeconds() > other.startTime.toSeconds())
        {
            return 1;
        } else if (this.startTime.toSeconds()< other.startTime.toSeconds())
        {
            return -1;
        }
        else {
            try {
                throw new Exception("well this shouldn't happen");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        // micky mouse return statement. Should never be reached
        return -1;
    }

}
