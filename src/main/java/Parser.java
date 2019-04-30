import java.io.FileReader;
import java.io.IOException;
import java.time.Duration;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.nio.file.Path;

import static java.nio.file.Files.readAllLines;

public class Parser {

    private Path fileName;
    ArrayList<Activity> activities = new ArrayList<>();

    Parser(Path fileName) throws IOException {
        this.fileName = fileName;
//        this.activities = this.readFile();
    }

    public ArrayList<Activity> readFile() throws IOException {

        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(this.fileName.toString()));
            String line;

            while ((line = br.readLine()) != null) {
                String name = line.substring(0, line.lastIndexOf(" "));
                String duration = line.substring(line.lastIndexOf(" ") + 1);
                if (duration.equals("sprint")) {
                    duration = "15min";
                }
                duration = duration.substring(0, duration.length() - 3);
                Activity activity = new Activity(name, Integer.parseInt(duration));
                this.activities.add(activity);
            }

        } catch (IOException e) {

        } finally {
            br.close();
        }
        return this.activities;
    }
}
