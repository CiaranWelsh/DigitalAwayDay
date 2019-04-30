import junit.framework.TestCase;
import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;
import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.lang.Exception;
import java.util.ArrayList;


public class ParserTests extends TestCase {

    Path projectDir;
    Path dataFile;

    @Before
    public void setUp() throws FileDoesNotExistException {
        projectDir = Paths.get(System.getProperty("user.dir"));
        dataFile = Paths.get(projectDir.toString(), "data.txt");
        if (!dataFile.toFile().exists())
            throw new FileDoesNotExistException();

//        this.projectDir = projectDir;

    }

    @Test
    public void test_length() throws IOException {
        Parser p = new Parser(this.dataFile);
        ArrayList<Activity> activities = p.readFile();
        int expected = 20;
        int actual = activities.size();
        assertEquals(expected, actual);

    }
}
