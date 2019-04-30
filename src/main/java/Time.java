import java.util.ArrayList;

public class Time {

    int hour;
    int minutes;
    int seconds;


    public Time(int hour, int minutes, int seconds) {
        this.hour = hour;
        this.minutes = minutes;
        this.seconds = seconds;

        if (this.minutes >= 60) {
            this.hour += this.minutes / 60;
            this.minutes = this.minutes % 60;
        }
        if (this.seconds > 60) {
            this.minutes += this.seconds/ 60;
            this.seconds = this.seconds % 60;
        }

        if (this.hour > 23) {
            try {
                throw new Exception();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }


    }

    public String toString() {
        return String.format("Time(hour=%d, minutes=%d, seconds=%d)",
                this.hour, this.minutes, this.seconds);
    }

    public Time diff(Time that) {
        Integer h_diff = this.hour - that.hour;
        Integer m_diff = this.minutes - that.minutes;
        Integer s_diff = this.seconds - that.seconds;

        Time time = new Time(h_diff, m_diff, s_diff);
        return time;
    }

    public Time add(Time that){
        Integer h_plus = this.hour + that.hour;
        Integer m_plus = this.minutes + that.minutes;
        Integer s_plus = this.seconds + that.seconds;

        Time time = new Time(h_plus, m_plus, s_plus);
        return time;
    }

    public boolean lt(Time that) {
        boolean h = this.hour < that.hour;
        boolean m = this.minutes < that.minutes;
        boolean s = this.seconds < that.seconds;

        if (h & m & s) {
            return true;
        }
        return false;
    }

    public boolean gt(Time that) {
        boolean h = this.hour > that.hour;
        boolean m = this.minutes > that.minutes;
        boolean s = this.seconds > that.seconds;

        if (h & m & s) {
            return true;
        }
        return false;
    }

    public int toMin(){
        return this.hour*60 + this.minutes;
    }


}



