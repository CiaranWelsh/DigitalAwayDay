import java.time.Duration;
import java.util.HashMap;

public class Activity {

    String name;
    Time duration;
    String units = "min";
    Time startTime = new Time(0, 0, 0);

    Activity(String name, int duration){
        this.name = name;
        this.duration = new Time(0, duration, 0);
    }

    @Override
    public String toString(){
        return "Activity(name=\""+this.name+"\", startTime="+
                this.startTime+")";
    }

}
